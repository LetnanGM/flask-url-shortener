from flask import Flask, request, jsonify
from application.bootstrap import init_MS


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
            data = request.get_json()
            status, response = self._priv.verify_user(
                data["username"], data["password"]
            )

            return jsonify({"status": status, "reason": response, "data": {}})

        @self._app.route("/api/auth/register", methods=["POST"])
        def register():
            data = request.get_json()
            status, response = self._priv.add_new_user(
                data["name"], data["email"], data["username"], data["password"]
            )

            return jsonify({"status": status, "reason": response, "data": {}})

        @self._app.route("/api/auth/forgot_password", methods=["GET", "POST"])
        def forgot_password():
            return {"service currently not have change password."}
