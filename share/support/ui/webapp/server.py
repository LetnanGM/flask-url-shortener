from flask import Flask
from .blueprint.blueprint import BlueprintManager
from .route.routes import RouteManager
from share.contract.serverapp import ServerApp


class FlaskServer(ServerApp):
    def __init__(self, config: dict) -> None:
        super().__init__(config=config)
        self.app = Flask(
            import_name=__name__,
            static_folder=self.config.static_folder,
            template_folder=self.config.template_folder,
        )

        self._configure_app()
        self._setup()

    def _configure_app(self) -> None:
        """Configure Flask application settings"""
        self.app.config["MAX_CONTENT_LENGTH"] = self.config.max_content_length
        self.app.config["SECRET_KEY"] = "your-secret-key-here"  # Change in production

        # Additional configurations
        self.app.config["JSON_SORT_KEYS"] = False
        self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

        super()._configure_app()

    def _setup(self):
        super()._setup()
        bpm = BlueprintManager(app=self.app, logger=self.logger)
        rm = RouteManager(app=self.app, logger=self.logger)

        bpm.register_blueprints()
        rm.register_routes()

        self.logger.info("Server setup completed.")

    def run(self):
        try:
            super().run()

            self.app.run(
                host=self.config.host,
                port=self.config.port,
                debug=self.config.debug,
                use_reloader=self.config.debug,
            )

        except Exception as e:
            self.logger.error("FlaskServer > " + e)
