from flask import session, request, abort
from functools import wraps
from typing import List, Optional, Callable
from ...utils.logging.childLogger import protector_logger


def require_auth(allowed_roles: Optional[List[str]] = None):
    """
    Decorator for routes requiring authentication and authorization

    Usage:
        @app.route('/admin')
        @require_auth(allowed_roles=['admin'])
        def admin_page():
            return "Admin panel"
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
            if "user_id" not in session:
                protector_logger.warning(
                    f"Unauthorized access attempt to {request.path}",
                    extra={"ip": request.remote_addr},
                )
                abort(401, description="Authentication required")

            # Check user role if specified
            if allowed_roles:
                user_role = session.get("user_role")
                if user_role not in allowed_roles:
                    protector_logger.warning(
                        f"Forbidden access attempt to {request.path} by user role: {user_role}",
                        extra={"ip": request.remote_addr},
                    )
                    abort(403, description="Insufficient permissions")

            return f(*args, **kwargs)

        return decorated_function

    return decorator
