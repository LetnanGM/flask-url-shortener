"""
detection for CSRF Vulnerability and hackers exploit
"""

from .csrf_private_dataclass import CSRFPriv
from .csrf_conf import CSRFLogger
from datetime import datetime, timedelta


class CSRFDetect(CSRFPriv):
    def __init__(self) -> None:
        super().__init__()

    def token_reuse_attack(self, token: str, ip: str) -> bool:
        """Detect suspicious token reuse patterns"""
        if token not in self.token_metadata:
            return False

        metadata = self.token_metadata[token]

        # Token used from different IP = potential compromise
        if metadata.ip != ip:
            CSRFLogger.warn(
                "🚨 Token reuse from different IP detected!",
                extra={
                    "token": token[:16] + "...",
                    "original_ip": metadata.ip,
                    "current_ip": ip,
                },
            )
            self.compromised_tokens.add(token)
            metadata.is_compromised = True
            return True

        # Excessive token reuse
        if metadata.usage_count > self.MAX_TOKEN_USAGE:
            CSRFLogger.warn(
                f"⚠️  Excessive token reuse detected: {metadata.usage_count} uses",
                extra={"token": token[:16] + "...", "ip": ip},
            )
            return True

        # Rapid token usage (potential bot)
        if metadata.last_used:
            time_since_last = datetime.now() - metadata.last_used
            if time_since_last.total_seconds() < 0.1:  # Less than 100ms
                CSRFLogger.warn(
                    "⚠️  Rapid token reuse detected (potential bot)",
                    extra={"token": token[:16] + "...", "ip": ip},
                )
                return True

        return False

    def csrf_attack_pattern(self, ip: str) -> bool:
        """Detect CSRF attack patterns from IP"""
        now = datetime.now()

        # Clean old attempts
        self.csrf_attack_patterns[ip] = [
            ts
            for ts in self.csrf_attack_patterns[ip]
            if now - ts < timedelta(minutes=5)
        ]

        # Multiple failures in short time = attack
        if len(self.csrf_attack_patterns[ip]) >= 5:
            CSRFLogger.warn(
                f"🚨 CSRF ATTACK PATTERN detected from IP: {ip}",
                extra={"ip": ip, "attempts": len(self.csrf_attack_patterns[ip])},
            )

            # Block IP temporarily
            self.blocked_ips[ip] = now + timedelta(minutes=30)
            return True

        return False
