from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from share.shared.logger.print import Logger
from share.support.time.date import date

from pydantic import BaseModel

CSRFLogger = Logger(
    log_file=f"assets/logs/Protector/CSRF/CSRF-{date.get_date_as_ymd()}.log"
)


@dataclass
class CSRFConf:
    """Simple configuration data"""

    BASE_TOKEN_NUMBER: int = 32


class CSRFViolation(BaseModel):
    """Track CSRF violation attempts"""

    timestamp: datetime
    ip: str
    endpoint: str
    referer: str
    origin: str
    user_agent: str
    token_provided: bool
    token_valid: bool
    severity: int = 1

    @property
    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "ip": self.ip,
            "endpoint": self.endpoint,
            "referer": self.referer,
            "origin": self.origin,
            "user_agent": self.user_agent,
            "token_provided": self.token_provided,
            "token_valid": self.token_valid,
            "severity": self.severity,
        }

class TokenMetadata(BaseModel):
    """Metadata for advanced token tracking"""

    token: str = None
    created_at: datetime = None
    ip: str = None
    user_agent: str = None
    usage_count: int = 0
    last_used: Optional[datetime] = None
    is_compromised: bool = False

    @property
    def to_dict(self):
        return {
            "token": self.token,
            "created_at": self.created_at,
            "ip": self.ip,
            "user_agent": self.user_agent,
            "usage_count": self.usage_count,
            "last_used": self.last_used,
            "is_compromised": self.is_compromised
        }