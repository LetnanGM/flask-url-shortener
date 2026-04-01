from data.configuration.internal.server.service import Service
from share.shared.logger.server_logger import ServerLogger
from flask import Flask, render_template, jsonify


class RouteManager:
    """Manages route registration for the Flask app"""

    def __init__(self, app: Flask, logger: ServerLogger):
        self.app = app
        self.logger = logger
        Service()

    def register_routes(self) -> None:
        """Register all application routes"""
        self._register_main_routes()
        self.logger.info("All routes registered successfully")

    def _register_main_routes(self) -> None:
        """Register main application routes"""

        @self.app.route("/")
        def index():
            """Main landing page"""
            return render_template("index.html"), 200

        @self.app.route("/health")
        def health_check():
            """Health check endpoint"""
            return (
                jsonify({"status": Service.STATUS, "service": Service.SERVICE_TITLE}),
                200,
            )

        @self.app.route("/api/v1/info")
        def api_info():
            """API information endpoint"""
            return (
                jsonify(
                    {"version": Service.SERVICE_VERSION, "endpoints": Service.ENDPOINTS}
                ),
                200,
            )
