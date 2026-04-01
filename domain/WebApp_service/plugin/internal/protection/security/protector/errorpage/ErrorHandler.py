from flask import Flask


class ErrorHandler:
    def __init__(self, app: Flask) -> None:
        self.app = app

        self.error_routes()

    def path_render(self, namefile: str) -> str:
        return f"pages/error/{namefile}"

    def error_routes(self) -> None:
        @self.app.errorhandler(404)
        def error_page_not_found(e):
            return "page not found", 404

        @self.app.errorhandler(403)
        def error_forbiden_permission(e):
            return "forbiden: your'e not have permission to access it", 403

        @self.app.errorhandler(400)
        def bad_request_page(e):
            return "bad request dude, repair your header or method post", 400

        @self.app.errorhandler(500)
        def internal_server_error(e):
            return "internal server error, report this to developer", 500
