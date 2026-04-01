from flask import Flask
from typing import Union, Type, Callable
from queue import Queue
from share.shared.logger.server_logger import ServerLogger
import inspect


class var:
    BP: Queue = Queue(maxsize=20)
    APP: Flask = None


class bpm:
    def __init__(self):
        pass

    def _load_with_app(self, object_type: type) -> bool:
        """ """
        object_type(app=var.APP)
        return True

    def _load_as_blank(self, object_type: type) -> bool:
        """ """
        object_type()
        return True

    def validatingTypeArguments(self, object_type: Type | Callable) -> None:
        """
        validating argument type from object_type, like class and function.

        Params:
            object_type: object instance.

        Return:
            Nonetype
        """
        if hasattr(object_type, "app") and isinstance(object_type, type):
            self._load_with_app(object_type)

        elif isinstance(object_type, Callable):
            sig = inspect.signature(object_type)
            if "app" in sig.parameters:
                self._load_with_app(object_type)
            else:
                self._load_as_blank(object_type)
        else:
            raise TypeError("'object_type' are not valid!")

    @staticmethod
    def register_queue(blueprint_or_classes: Union[type, str]) -> bool:
        """ """
        var.BP.put(blueprint_or_classes)


class BlueprintManager:
    """Manages blueprint registration"""

    def __init__(self, app: Flask, logger: ServerLogger):
        self.app = app
        self.logger = logger
        var.APP = app

    def register_blueprints(self) -> None:
        """Register all blueprints"""
        bp_object = bpm()

        try:
            while not var.BP.empty():
                instance = var.BP.get()
                self.logger.info(f"Load object '{instance}'..")
                bp_object.validatingTypeArguments(object_type=instance)

            self.logger.info("All service blueprint registered.")
        except Exception as e:
            self.logger.error(f"Failed to register blueprints: {e}")
            raise
