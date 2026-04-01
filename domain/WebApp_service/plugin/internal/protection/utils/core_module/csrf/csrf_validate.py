from datetime import datetime, timedelta
from .csrf_conf import TokenMetadata
from .csrf_private_dataclass import CSRFPriv


class CSRFValidator(CSRFPriv, TokenMetadata):
    def __init__(self) -> None:
        super().__init__()

    def _is_token_expired(self, token: str) -> bool:
        """Check if token has expired"""
        if token not in self.token_metadata:
            return True

        metadata = self.token_metadata[token]
        age = datetime.now() - metadata.created_at

        return age > timedelta(hours=self.TOKEN_EXPIRY_HOURS)

    def _is_ip_blocked(self, ip: str) -> bool:
        """Check if IP is blocked due to CSRF violations"""
        if ip in self.blocked_ips:
            if datetime.now() < self.blocked_ips[ip]:
                return True
            else:
                del self.blocked_ips[ip]
        return False
