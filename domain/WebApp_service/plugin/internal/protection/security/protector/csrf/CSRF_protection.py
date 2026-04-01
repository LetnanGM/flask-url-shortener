from flask import Flask, session, request, abort
from ....utils.crypto.encryption import safe_str_cmp

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from ....data.configuration.sys.SecurityConfig import SecurityConfig
from ....utils.validator.header.hvalidator import Header
from ....utils.core_module.csrf import (
    CSRFHelper,
    CSRFDetect,
    CSRFPriv,
    CSRFLogger,
    CSRFViolation,
)

class utils:
    def is_safe_method():
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        
        return False
    
    def client_ip() -> str | None:
        return request.remote_addr
    
    def build_dict(self, **kwargs) -> dict:
        """
        From arguments or parameter function to dict.
        """
        return kwargs


class CSRFProtection(CSRFPriv):
    """
    Advanced CSRF Protection with intelligent threat detection.

    Features:
    - Token rotation and expiration
    - Double-submit cookie pattern
    - Origin/Referer validation
    - Per-request token binding
    - Attack pattern detection
    - Token reuse detection
    - Suspicious behavior tracking
    - Automatic token compromise detection

    Developed by SoloDev - Syafiq
    """

    def __init__(
        self,
        app: Flask,
        exempt_endpoints: Optional[List[str]] = SecurityConfig.CSRF_EXEMPT_ENDPOINTS,
        trusted_origins: Optional[List[str]] = SecurityConfig.TRUSTED_ORIGIN,
    ):
        self.util = utils()
        self.mod = CSRFHelper(app_secret_key=app.secret_key)
        self.detect = CSRFDetect()

        self.app = app
        self.exempt_endpoints = exempt_endpoints or []
        self.trusted_origins = set(trusted_origins or [])

        # Initialize protection
        self._setup_csrf_protection()

    def _record_violation(
        self, severity: int, token_provided: bool, token_valid: bool, reason: str
    ):
        """Record CSRF violation for analysis"""
        ip = self.util.client_ip()
        data = self.util.build_dict(
            timestamp=datetime.now(),
            ip=ip,
            endpoint=request.endpoint or "unknown",
            referer=request.headers.get("Referer", ""),
            origin=request.headers.get("Origin", ""),
            user_agent=request.headers.get("User-Agent", ""),
            token_provided=token_provided,
            token_valid=token_valid,
            severity=severity,
        )

        violation = CSRFViolation(**data)

        self.violations.append(violation)
        self.csrf_attack_patterns[ip].append(datetime.now())
        self.suspicious_ips[ip] += severity

        # Keep only recent violations
        if len(self.violations) > 1000:
            self.violations = self.violations[-1000:]

        CSRFLogger.warn(
            f"🛡️  CSRF Violation: {reason}",
            extra={
                "ip": ip,
                "endpoint": request.endpoint,
                "severity": severity,
                "reason": reason,
            },
        )

    def validate_csrf_token(self, token: str) -> Tuple[bool, str]:
        """
        Enhanced CSRF token validation.
        Returns: (is_valid, reason)
        """
        ip = request.remote_addr
        user_agent = request.headers.get("User-Agent", "")

        # Check if IP is blocked
        if self._is_ip_blocked(ip):
            self._record_violation(
                3, True, False, "IP blocked due to previous violations"
            )
            return False, "IP blocked"

        # Check if token exists in session
        if "csrf_token" not in session:
            self._record_violation(2, False, False, "No token in session")
            return False, "No token in session"

        session_token = session["csrf_token"]

        # Check if token is compromised
        if token in self.compromised_tokens:
            self._record_violation(3, True, False, "Token marked as compromised")
            return False, "Token compromised"

        # Check token expiration
        if self._is_token_expired(token):
            self._record_violation(1, True, False, "Token expired")
            return False, "Token expired"

        # Verify token binding
        if not self.mod._verify_token_binding(token, ip, user_agent):
            self._record_violation(2, True, False, "Token binding verification failed")
            return False, "Token binding failed"

        # Compare tokens
        is_valid = safe_str_cmp(session_token, token)

        if not is_valid:
            self._record_violation(2, True, False, "Token mismatch")

            # Detect attack pattern
            if self.detect.csrf_attack_pattern(ip):
                return False, "Attack pattern detected"

            return False, "Invalid token"

        # Update token metadata
        if token in self.token_metadata:
            metadata = self.token_metadata[token]
            metadata.usage_count += 1
            metadata.last_used = datetime.now()

            # Detect token reuse attack
            if self.detect.token_reuse_attack(token, ip):
                self._record_violation(2, True, True, "Suspicious token reuse")
                return False, "Suspicious token usage"

        return True, "Valid"

    def _setup_csrf_protection(self) -> None:
        """Setup CSRF protection middleware"""

        @self.app.before_request
        def check_csrf():
            # Skip for exempt endpoints
            for exempt_endpoint_path in self.exempt_endpoints:
                if exempt_endpoint_path in request.path:
                    return

            # Skip for safe methods
            if self.util.is_safe_method(): return

            ip = self.util.client_ip()

            # Check if IP is blocked
            if self._is_ip_blocked(ip):
                CSRFLogger.warn(
                    f"🚫 Blocked request from IP: {ip}",
                    extra={"ip": ip, "endpoint": request.endpoint},
                )
                abort(403, "Access denied due to security violations")

            # Validate Origin/Referer
            origin_valid, origin_msg = Header(
                request_host=request.host,
                method=request.method,
                origin=request.origin,
                referer=request.referrer,
            )._validate_origin_referer()

            if not origin_valid:
                self._record_violation(2, False, False, origin_msg)
                abort(403, "Invalid Origin or Referer")

            token_source, token = self.mod.get_csrf_token()

            if not token:
                self._record_violation(2, False, False, "No CSRF token provided")
                abort(403, "CSRF token missing")

            # Validate token
            is_valid, reason = self.validate_csrf_token(token)

            if not is_valid:
                CSRFLogger.warn(
                    f"❌ CSRF validation failed: {reason}",
                    extra={
                        "ip": ip,
                        "endpoint": request.endpoint,
                        "reason": reason,
                        "token_source": token_source,
                    },
                )
                abort(403, f"CSRF validation failed: {reason}")

            CSRFLogger.vsilent(
                "✅ CSRF validation passed",
                extra={
                    "ip": ip,
                    "endpoint": request.endpoint,
                    "token_source": token_source,
                },
            )

        @self.app.after_request
        def set_csrf_cookie(response):
            """Set CSRF token in cookie"""
            token = self.mod.generate_smart_token()

            # Secure cookie settings
            response.set_cookie(
                "csrf_token",
                token,
                httponly=False,  # Needs to be readable by JavaScript
                secure=request.is_secure,  # HTTPS only in production
                samesite="Strict",  # Prevent CSRF via cookie
            )

            return response

        @self.app.after_request
        def set_csrf_headers(response):
            """Set CSRF token in response header"""
            token = session.get("csrf_token", "")
            if token:
                response.headers["X-CSRF-Token"] = token

            # Additional security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"

            return response

    def get_security_statistics(self) -> Dict:
        """Get CSRF security statistics"""
        now = datetime.now()

        # Recent violations (last hour)
        recent_violations = [
            v for v in self.violations if now - v.timestamp < timedelta(hours=1)
        ]

        # Active attacks (last 5 minutes)
        active_attacks = {
            ip: len(attempts)
            for ip, attempts in self.csrf_attack_patterns.items()
            if attempts and now - attempts[-1] < timedelta(minutes=5)
        }

        return {
            "total_violations": len(self.violations),
            "recent_violations": len(recent_violations),
            "suspicious_ips": len(self.suspicious_ips),
            "blocked_ips": len(self.blocked_ips),
            "compromised_tokens": len(self.compromised_tokens),
            "active_attacks": len(active_attacks),
            "active_tokens": len(self.token_metadata),
        }

    def cleanup_old_data(self):
        """Cleanup old tracking data"""
        now = datetime.now()

        # Clean old violations (keep 24 hours)
        self.violations = [
            v for v in self.violations if now - v.timestamp < timedelta(hours=24)
        ]

        # Clean expired tokens
        expired_tokens = [
            token
            for token, metadata in self.token_metadata.items()
            if now - metadata.created_at > timedelta(hours=self.TOKEN_EXPIRY_HOURS * 2)
        ]
        for token in expired_tokens:
            del self.token_metadata[token]
            self.compromised_tokens.discard(token)

        # Clean old attack patterns
        for ip in list(self.csrf_attack_patterns.keys()):
            self.csrf_attack_patterns[ip] = [
                ts
                for ts in self.csrf_attack_patterns[ip]
                if now - ts < timedelta(hours=1)
            ]
            if not self.csrf_attack_patterns[ip]:
                del self.csrf_attack_patterns[ip]

        CSRFLogger.vsilent("🧹 Cleaned up old CSRF protection data")

    def add_trusted_origin(self, origin: str):
        """Add a trusted origin for CORS scenarios"""
        self.trusted_origins.add(origin)
        CSRFLogger.vsilent(f"➕ Added trusted origin: {origin}")
