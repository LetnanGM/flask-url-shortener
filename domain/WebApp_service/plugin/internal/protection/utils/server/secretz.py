import secrets
import dotenv
import os
from typing import Tuple, Any


class secretz:
    dotenv.load_dotenv()

    def generate_new_token_urlsafe(max_byte: int = 128) -> str:
        """generate new token urlsafe"""
        return secrets.token_urlsafe(nbytes=max_byte)

    def set_to_dotenv(
        variable_name: str,
        value_of_variable: str,
        dotenv_path: str = ".env",
    ) -> Tuple[bool, str]:
        """set the token or key into dotenv"""
        if not os.path.isfile(path=dotenv_path):
            os.touch

        dotenv.set_key(
            dotenv_path=dotenv_path,
            key_to_set=variable_name,
            value_to_set=value_of_variable,
        )

        return True, "Successfully"

    def get_an_key(key: str) -> Any:
        """gettings value of your name key in args"""
        if not key:
            return None

        return os.getenv(key=key)


def get_secret_key_server():
    key = secretz.get_an_key(key="secret_key")
    if key is None:
        secretz.set_to_dotenv(
            variable_name="secret_key",
            value_of_variable=secretz.generate_new_token_urlsafe(),
        )
        get_secret_key_server()

    return secretz.get_an_key() if not key else key
