from flask import Flask, request, jsonify, redirect, url_for, make_response
from application.bootstrap import init_MS, init_SESSION
            
class Auth:
    def __init__(self) -> None:
        self._app = None
        self._priv = init_MS()
        self._session = init_SESSION()

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
            
            login must be have json data, and have column / query "email" and "password".
            """
            redirect_url = {
                "user": redirect(url_for("dashboard_page")),
                "admin": redirect(url_for("admin_page")),
                "owner": redirect(url_for("admin_page"))
            }
            
            data = request.get_json()            
            email = data["email"]
            password = data["password"]
            
            status, response = self._priv.verify_user(email, password)
            
            if not status and not response:
                return {
                    "status": False,
                    "reason": "unknown server error."
                }

            user_id = self._priv.where_is_userid(email)
            if not user_id:
                return {
                    "status": False,
                    "reason": "email or password are wrong!"
                }
                
            privilege = self._priv.take_info_user(user_id).privilege
            
            status, session_id = self._session.add_session(user_id)
            
            response = make_response(redirect_url[privilege.lower()], 200)
            response.set_cookie("session_id", session_id, httponly=True, samesite="Lax")
            
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