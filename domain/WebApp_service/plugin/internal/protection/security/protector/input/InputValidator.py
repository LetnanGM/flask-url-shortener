from flask import request
from ....data.configuration.sys.SecurityConfig import SecurityConfig
from ....utils.logging.childLogger import iv_logger
import bleach
import html
import re


class InputValidator:
    """Validates and sanitizes user input"""

    @staticmethod
    def detect_sql_injection(data: str) -> bool:
        """Detect SQL injection attempts"""
        data_lower = data.lower()
        for pattern in SecurityConfig.SQL_INJECTION_PATTERNS:
            if re.search(pattern, data_lower, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def detect_xss(data: str) -> bool:
        """Detect XSS attempts"""
        for pattern in SecurityConfig.XSS_PATTERNS:
            if re.search(pattern, data, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def detect_path_traversal(data: str) -> bool:
        """Detect path traversal attempts"""
        for pattern in SecurityConfig.PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, data, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def detect_command_injection(data: str) -> bool:
        """Detect command injection attempts"""
        for pattern in SecurityConfig.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, data):
                return True
        return False

    @staticmethod
    def sanitize_input(data: str) -> str:
        """Sanitize user input"""
        # HTML escape
        data = html.escape(data)

        # Remove potentially dangerous characters
        data = bleach.clean(data, tags=[], strip=True)

        return data

    @staticmethod
    def validate_input(data: str, input_type: str = "text") -> tuple[bool, str]:
        """
        Comprehensive input validation
        Returns: (is_valid, sanitized_data)
        """
        if not data:
            return True, ""

        # Check for various injection attempts
        if InputValidator.detect_sql_injection(data):
            iv_logger.vsilent(
                f"SQL Injection attempt detected: {data[:100]}",
                extra={"ip": request.remote_addr},
            )
            return False, ""

        if InputValidator.detect_xss(data):
            iv_logger.vsilent(
                f"XSS attempt detected: {data[:100]}", extra={"ip": request.remote_addr}
            )
            return False, ""

        if InputValidator.detect_path_traversal(data):
            iv_logger.vsilent(
                f"Path traversal attempt detected: {data[:100]}",
                extra={"ip": request.remote_addr},
            )
            return False, ""

        if InputValidator.detect_command_injection(data):
            iv_logger.vsilent(
                f"Command injection attempt detected: {data[:100]}",
                extra={"ip": request.remote_addr},
            )
            return False, ""

        # Sanitize input
        sanitized = InputValidator.sanitize_input(data)

        return True, sanitized
