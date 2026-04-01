from share.shared.logger.print import Logger
from share.support.ui.webapp.blueprint.blueprint import bpm
from data.configuration.internal.server.security import SECURITY_ALTAR

bp_manager = bpm()
log = Logger()


class internal:
    @staticmethod
    def load_all() -> bool:
        from .internal import Security, guardian

        if SECURITY_ALTAR:
            bp_manager.register_queue(Security.setup)
            log.debug("'SecurityMiddleware' internal package registered!")

        # @Guardian_Crash must be always Online for making report crash app
        bp_manager.register_queue(guardian.setup)
        log.debug("'Guardian_Crash' internal package registered!")

        return True


class external:
    def extract_setup_me() -> None:
        """ """
        import os
        import importlib

        path = os.path.abspath(
            os.path.join(os.getcwd(), "domain\\WebApp_service\\plugin\\external")
        )
        plugin_external = os.listdir(path)

        if not plugin_external:
            return False

        for plugin in plugin_external:
            plugin_path = path + f"\\{plugin}"
            log.debug(f"Trying load '{plugin}'..")
            if os.path.isdir(plugin_path):
                try:
                    module_name = f"domain.WebApp_service.plugin.external.{plugin}.main"
                    module = importlib.import_module(module_name)
                    log.debug(
                        f"[{plugin}]: detected object module '{module.__name__}', finding 'setup_me'.."
                    )

                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if isinstance(obj, type):
                            if hasattr(obj, "setup_me"):
                                log.debug(
                                    f"[{plugin}]:{obj.__name__}: setup_me finded! object registered into Queue."
                                )
                                instance = obj()
                                bp_manager.register_queue(instance.setup_me)
                            else:
                                log.debug(
                                    f"[{plugin}]:{obj.__name__}: object doesn't have 'setup_me' function, skiped!"
                                )
                        else:
                            continue
                except Exception as e:
                    print(f"[ERROR:PLUGIN]: > '{plugin}' have error '{e}'.")
            else:
                print(f"[ERROR]: Cannot find folder plugin '{plugin}'")

    def load_all():
        external.extract_setup_me()
        return True
