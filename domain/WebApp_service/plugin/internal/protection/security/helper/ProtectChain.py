# ProtectionChain.py
import importlib
import inspect
from typing import Callable, List
from flask import abort, current_app
from ...utils.logging.childLogger import chainring_logger


class ProtectionError(Exception):
    """Raised when a protection handler rejects the request."""

    pass


class ProtectionChain:
    """
    ProtectionChain holds ordered protection handlers. Each handler
    receives (flask_request) and should return True (allow) or False (deny)
    OR raise ProtectionError / abort(403) with a reason.
    """

    def __init__(self):
        self.handlers: List[Callable] = []

    def add(self, func: Callable):
        """Add a handler (callable(request) -> bool)"""
        if not callable(func):
            raise TypeError("handler must be callable")
        self.handlers.append(func)
        chainring_logger.debug(
            f"ProtectionChain: added handler {getattr(func,'__name__',repr(func))}"
        )
        return self

    def run(self, req):
        """
        Run handlers in order. If any returns False or raises, stop and abort.
        """
        for fn in self.handlers:
            try:
                result = fn(req)
            except ProtectionError as pe:
                chainring_logger.info(
                    f"ProtectionChain: handler {fn.__name__} rejected request: {pe}"
                )
                abort(403, description=str(pe))
            except Exception as exc:
                chainring_logger.exception(
                    f"ProtectionChain: handler {fn.__name__} crashed: {exc}"
                )
                abort(500, description="Protection subsystem error")
            else:
                # allow if True / truthy
                if not result:
                    chainring_logger.info(
                        f"ProtectionChain: handler {fn.__name__} returned False -> deny"
                    )
                    abort(403, description=f"Blocked by {fn.__name__}")

    # ---------- Convenience: auto-load handlers from module names ----------
    def load_from_module(self, module_path: str, prefer_names: List[str] = None) -> int:
        """
        Attempt to import module and find callable handler(s) inside.
        prefer_names: list of function/method names to look for in order.
        Returns number of handlers added.
        """
        added = 0
        try:
            mod = importlib.import_module(module_path)
        except Exception as e:
            chainring_logger.debug(f"ProtectionChain: cannot import {module_path}: {e}")
            return 0

        # candidate names that represent a validation function
        candidates = prefer_names or [
            "validate",
            "validate_request",
            "validate_csrf",
            "allow_request",
            "check",
            "before_request",
            "run",
        ]

        # 1. module-level functions
        for name in candidates:
            fn = getattr(mod, name, None)
            if fn and callable(fn):
                self.add(fn)
                added += 1

        # 2. classes inside module: try to instantiate and use known method names
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            # skip imported classes from elsewhere
            if obj.__module__ != mod.__name__:
                continue
            # try typical instance method names
            instance_method_names = [
                "validate",
                "validate_request",
                "allow_request",
                "check",
            ]
            try:
                inst = None
                for mname in instance_method_names:
                    if hasattr(obj, mname):
                        # create instance if it can be constructed with no args or with app arg
                        try:
                            inst = obj()
                        except TypeError:
                            # try passing current_app if available
                            try:
                                inst = obj(current_app)
                            except Exception:
                                inst = None
                        if inst:
                            method = getattr(inst, mname)
                            if callable(method):
                                # wrap bound method to accept request only
                                self.add(lambda req, _method=method: _method(req))
                                added += 1
                                break
            except Exception as e:
                chainring_logger.debug(
                    f"ProtectionChain: error instantiating {obj}: {e}"
                )
                continue

        return added
