from data.configuration.internal import ServerConfig
from share.support.ui.webapp.server import FlaskServer
from application.bootstrap import webapp_plugin
import os

BASE = os.path.abspath(os.path.join(os.getcwd(), "domain/WebApp_service"))


class server:
    @staticmethod
    def deploy() -> None:
        internal, external = webapp_plugin()
        internal.load_all()
        external.load_all()
        # print(f"internal:external > {intern_resp}:{extern_resp}")

        config: ServerConfig = ServerConfig(
            template_folder=BASE + "\\frontend",
            static_folder=BASE + "\\static",
            debug=False,
        )

        instance = FlaskServer(config=config)
        instance.run()
