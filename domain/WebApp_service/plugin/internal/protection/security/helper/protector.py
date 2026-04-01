# inside protect.py (or wherever setup_security is defined)
from .ProtectChain import ProtectionChain
from ...utils.logging.childLogger import chainring_logger
from flask import request


def setup_securitychain(app):
    """
    Initialize protection chain and register before_request hook.
    This will auto-load common protection subprotects under
    '.subprotect.*' — adjust list to suit your files.
    """
    chain = ProtectionChain()

    # list subprotects to attempt to load (adjust names to your package)
    subprotects = [
        "domain.WebApp_service.plugin.internal.protection.security.protector.csrf.CSRF_protection",
        "domain.WebApp_service.plugin.internal.protection.security.protector.input.InputValidator",
        "domain.WebApp_service.plugin.internal.protection.security.protector.ratelimit.RateLimiter",
        "domain.WebApp_service.plugin.internal.protection.security.protector.obsec.Obsecurity",
    ]

    for mod in subprotects:
        added = chain.load_from_module(mod)
        chainring_logger.debug(f"setup_security: loaded {added} handlers from {mod}")

    # fallback: if you want to always run some inline checks, add them here
    # chain.add(lambda req: True)  # example

    # register global hook
    @app.before_request
    def _global_protect():
        # optionally skip static or health-check endpoints
        path = request.path or ""
        if path.startswith("/static") or path.startswith("/health"):
            return None

        # only run protections for unsafe methods; safe GETs skip
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            return chain.run(request)

    # Also add after_request to attach headers or cookies if needed (optional)
    return chain
