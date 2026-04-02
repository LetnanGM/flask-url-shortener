from typing import Dict
from functools import wraps
from flask import Flask, request, jsonify, redirect, url_for, session, make_response
from application.bootstrap import init_MS

SESSIONS: Dict[str, str] = {}

class IAuth:
    def __init__(self):
        self._ms = init_MS()
        
    @staticmethod
    def is_session_authenticated(user_session: str) -> bool:
        """ """
        return True if user_session in session else False
    
    @staticmethod
    def is_authenticated_as_what(username: str): 
        """ """
        return True if username in session else False
    
    def is_admin(self, username: str) -> bool:
        if not self.is_authenticated_as_what(username=username):
            return False
        
        user_id = self._ms.where_is_userid(username=username)
        if self._ms.take_info_user(user_id).privilege is not "admin":
            return False
        
        return True
    
def require_auth(privilege: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = IAuth.is_session_authenticated(request.cookies.get("session"))
            if not resp:
                return "Unauthorzied", 401
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
            
            
class Auth:
    def __init__(self) -> None:
        self._app = None
        self._priv = init_MS()

    def setup_me(self, app: Flask):
        """ """
        self._app = app
        self.main_service_routes()

    def main_service_routes(self):
        @self._app.route("/api/auth/login", methods=["POST"])
        def login():
            """
            >>> endpoint: /api/auth/login
            >>> method: ONLY POST
            >>> return: can be dict if error else redirect into dashboard if user else admin.
            
            login must be have json data, and have column / query "username" and "password".
            """
            from share.support.generator.uuid import uid
            redirect_url = {
                "user": redirect(url_for("dashboard")),
                "admin": redirect(url_for("admin")),
                "owner": redirect(url_for("admin"))
            }
            
            data = request.get_json()
            status, response = self._priv.verify_user(
                data["username"], data["password"]
            )
            
            if not status and not response:
                return {
                    "status": False,
                    "reason": "unknown server error."
                }

            user_id = self._priv.where_is_userid(data["username"])
            privilege = self._priv.take_info_user(user_id)
            
            builded_session = uid.token_uuid()
            SESSIONS[builded_session] = user_id
            
            response = make_response(redirect(url_for(redirect_url[privilege.lower()])), 200)
            response.set_cookie("session_id", builded_session, httponly=True, samesite="Lax")
            
            return response

        @self._app.route("/api/auth/register", methods=["POST"])
        def register():
            """
            >>> endpoint: api/auth/register
            >>> method: ONLY POST
            >>> return: dict, with value :
            >>>    {
            >>>        "status": boolean,
            >>>        "reason": reason, must string,
            >>>        "data": data from private function.
            >>>    }
                
            register new account into database and privilege default is 'user'.
            """
            data = request.get_json()
            status, response = self._priv.add_new_user(
                "user", data["name"], data["email"], data["username"], data["password"]
            )

            return jsonify({"status": status, "reason": response, "data": {}})

        @self._app.route("/api/auth/forgot_password", methods=["GET", "POST"])
        def forgot_password():
            return jsonify({"status": False, "reason": "service currently not have change password."})