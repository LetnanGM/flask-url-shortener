from ..parent import AppError


class InvalidArgs(AppError):
    """if user or developer's input different value or datatype, use this for warn invalidargs"""

    code = "APP-001"
    category = "GENERAL"


class NameAliasAlreadyInUse(AppError):
    """name alias already in use"""

    code = "APP-010"
    category = "GENERAL"
