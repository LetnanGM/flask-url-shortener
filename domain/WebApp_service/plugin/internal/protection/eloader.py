"""
Flask Security Middleware
Protects against OWASP Top 10 vulnerabilities with comprehensive logging
"""

from .security.protector import CSRFProtection, InputValidator, RateLimiter

from .security.helper.SecurityMiddleware import SecurityMiddleware
from .security.loader import loader_security

from .utils.server.secretz import get_secret_key_server
from .utils.logging.childLogger import protector_logger
from datetime import timedelta
from flask import Flask


class Security:
    __PLUGIN_NAME__ = "Thunder Security"
    __VERSION__ = "1.0.0"
    __DEVELOPER__ = "LetnanGM"

    @staticmethod
    def setup(app: Flask) -> SecurityMiddleware:
        """
        Initialize security middleware for Flask app

        Usage:
            from security_middleware import setup_security

            app = Flask(__name__)
            app.secret_key = 'your-secret-key-here'
            security = setup_security(app)
        """

        # Set secure session configuration
        app.config.update(
            SESSION_COOKIE_SECURE=True,  # Only send cookie over HTTPS
            SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access to session cookie
            SESSION_COOKIE_SAMESITE="Lax",  # CSRF protection
            PERMANENT_SESSION_LIFETIME=timedelta(hours=1),  # Session timeout
        )

        app.secret_key = get_secret_key_server()

        # Initialize security middleware
        loader_security(app=app)
        security = SecurityMiddleware(app=app)

        return security


# Export main components
__all__ = [
    "SecurityMiddleware",
    "Security",
    "RateLimiter",
    "InputValidator",
    "CSRFProtection",
    "protector_logger",
]
