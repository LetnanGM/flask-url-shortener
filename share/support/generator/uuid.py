import uuid
import secrets
import string
import random


class vmodel:
    uuid = uuid
    secret = secrets


class uid:
    @staticmethod
    def token_char(length: int = 6) -> str:
        return "".join(
            [
                str(random.choice(string.ascii_letters + string.digits))
                for _ in range(length)
            ]
        )

    @staticmethod
    def token_uuid() -> str:
        return str(vmodel.uuid.uuid4())

    @staticmethod
    def token_hex_safe() -> str:
        return str(vmodel.uuid.uuid4().hex())

    @staticmethod
    def token_hex_random() -> str:
        return vmodel.secret.token_hex()

    @staticmethod
    def token_urlsafe() -> str:
        return vmodel.secret.token_urlsafe()

    @staticmethod
    def token_bytes() -> str:
        return vmodel.secret.token_bytes()
