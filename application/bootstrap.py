# MAKE CONNECTION HERE
from typing import Tuple, Callable
from domain.ManagementService import require_auth

__all__ = ["require_auth"]

def webapp_plugin() -> Tuple[Callable, Callable]:
    from domain.WebApp_service.plugin.plugin import internal, external

    return internal, external


def init_MS():
    """
    User Management Service
    """
    from domain.ManagementService import privilege

    return privilege()

def init_SESSION():
    from domain.ManagementService import MSession
    return MSession()

def init_db(path_db: str) -> type:
    from infrastructure.database.jsonDB.jsondb import JsonDB

    return JsonDB(path_db)


def init_shortener():
    from domain.shortenerService.service import ShortenService

    return ShortenService(storage=init_db)
