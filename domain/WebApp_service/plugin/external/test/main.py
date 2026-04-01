from flask import Flask


class polyplay:
    def __init__(self) -> None:
        self.app: Flask = None

    def setup_me(self, app: Flask) -> None:
        self.app = app
        self.register_main_routes()

    def register_main_routes(self):
        @self.app.route("/unknown_test")
        def unknown_test():
            return "Tested by Developer"
