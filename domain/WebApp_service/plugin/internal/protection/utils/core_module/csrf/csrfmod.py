from flask import session, request

import secrets
import hmac
import hashlib

from datetime import datetime
from .csrf_private_dataclass import CSRFPriv
from .csrf_validate import CSRFValidator
from .csrf_conf import CSRFConf, TokenMetadata, CSRFLogger


class GEN:
    @staticmethod
    def combine_token(token: str, signature: str | bytes) -> bytes | str:
        combined_token = f"{token}.{signature}"
        return combined_token

    @staticmethod
    def generate_token_with_binding(
        secret_key: str, ip: str, user_agent: str
    ) -> str | bytes:
        """
        Generate CSRF Token with IP and UA (User-Agent) binding.
        """
        base_token = secrets.token_urlsafe(CSRFConf.BASE_TOKEN_NUMBER)

        binding_data = f"{ip}|{user_agent}|{base_token}"
        secretz_key = secret_key.encode() if isinstance(secret_key, str) else secret_key

        signature = hmac.new(
            key=secretz_key, msg=binding_data.encode(), digestmod=hashlib.sha256
        ).hexdigest()[:16]

        return GEN.combine_token(token=base_token, signature=signature)

    @staticmethod
    def generate_csrf_token(output: str = "session") -> str:
        """Generate a new CSRF token (backward compatibility)"""

        data = secrets.token_urlsafe(128)

        match output:
            case "session":
                if "csrf_token" not in session:
                    session["csrf_token"] = data

                return session["csrf_token"]
            case "raw":
                return data
            case _:
                return session["csrf_token"]


class CSRFHelper(CSRFPriv):
    def __init__(self, app_secret_key: str) -> None:
        self.secret_key = app_secret_key

    def _generate_token_with_binding(self, ip: str, user_agent: str) -> str:
        """
        Generate CSRF token with IP and UA binding.

        """
        combined_token = GEN.generate_token_with_binding(
            secret_key=self.secret_key, ip=ip, user_agent=user_agent
        )

        # Store metadata
        CSRFPriv.token_metadata[combined_token] = TokenMetadata(
            token=combined_token,
            created_at=datetime.now(),
            ip=ip,
            user_agent=user_agent,
        )

        return combined_token

    def generate_smart_token(self) -> str:
        """Generate smart CSRF token with binding"""
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent", "")

        # Check if current token needs rotation
        current_token = session.get("csrf_token")
        if current_token and not self._should_rotate_token(current_token):
            return current_token

        # Generate new token with binding
        new_token = self._generate_token_with_binding(ip, user_agent)
        session["csrf_token"] = new_token

        CSRFLogger.vsilent(
            f"🔐 New CSRF token generated for IP: {ip}",
            extra={"ip": ip, "token": new_token[:16] + "..."},
        )

        return new_token

    def _verify_token_binding(self, token: str, ip: str, user_agent: str) -> bool:
        """Verify token binding to IP and UA"""
        if "." not in token:
            return False

        base_token, provided_signature = token.rsplit(".", 1)

        # Recreate signature
        binding_data = f"{ip}|{user_agent}|{base_token}"
        expected_signature = hmac.new(
            (
                self.secret_key.encode()
                if isinstance(self.secret_key, str)
                else self.secret_key
            ),
            binding_data.encode(),
            hashlib.sha256,
        ).hexdigest()[:16]

        return hmac.compare_digest(expected_signature, provided_signature)

    def _should_rotate_token(self, token: str) -> bool:
        """Decide if token should be rotated"""
        if token not in self.token_metadata:
            return True

        metadata = self.token_metadata[token]

        # Rotate if expired
        if CSRFValidator()._is_token_expired(token):
            return True

        # Rotate if used many times
        if metadata.usage_count > 20:
            return True

        # Rotate if compromised
        if metadata.is_compromised:
            return True

        return False

    def get_csrf_token(self) -> tuple:
        method = {
            "headers": lambda: request.headers["X-CSRF-Token"],
            "form": lambda: request.form["csrf_token"],
            "json_body": lambda: request.json["csrf_token"],
            "cookie": lambda: request.cookies.get("csrf_token"),
        }

        for name, func in method.items():
            token = func()
            if token:
                return name, token
