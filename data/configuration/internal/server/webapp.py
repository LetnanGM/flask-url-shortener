from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any


@dataclass
class ServerConfig:
    """Server configuration with validation"""

    protocol: str = "http"
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False
    static_folder: str = None  # configure here
    template_folder: str = None  # configure here
    max_content_length: int = 16 * 1024 * 1024  # 16MB

    def __post_init__(self):
        """Validate configuration after initialization"""
        self._validate_host()
        self._validate_port()
        self._validate_folders()

    def _validate_host(self) -> None:
        """Validate host IP format"""
        if not self._is_valid_ip(self.host) and self.host != "0.0.0.0":
            raise ValueError(f"Invalid host IP: {self.host}")

    def _validate_port(self) -> None:
        """Validate port number"""
        if not isinstance(self.port, int) or not (1 <= self.port <= 65535):
            raise ValueError(f"Port must be between 1-65535, got: {self.port}")

    def _validate_folders(self) -> None:
        """Ensure required folders exist"""
        for folder in [self.static_folder, self.template_folder]:
            Path(folder).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        """Check if string is valid IPv4 address"""
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except (ValueError, TypeError):
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "host": self.host,
            "port": self.port,
            "debug": self.debug,
            "static_folder": self.static_folder,
            "template_folder": self.template_folder,
            "max_content_length": self.max_content_length,
        }
