from typing import Tuple, Dict, Union, List, Any
from types import EllipsisType
from pydantic import BaseModel, field_validator
from argon2 import hash_password, verify_password

from application.bootstrap import init_db
from share.support.generator.uuid import uid
from share.shared.handler import validate_parameter
from data.configuration.external.privilege.privilege import FILE_USER_DATABASE


class credentials(BaseModel):
    privilege: str
    name: str
    email: str
    username: str
    password: Union[str, bytes]
    
    @field_validator("privilege")
    def is_privilege_exists(cls, privilege: str): 
        privileges: List[str] = ["admin", "owner", "user"]
        if privilege in privileges:
            return privilege
        
        return "user"

    @field_validator("password")
    def password_hash(cls, password: str | bytes):
        """
        hash password for protection from stealer.
        """
        return str(
            hash_password(
                password=password if isinstance(password, bytes) else password.encode()
            ).decode()
        )

    @property
    def to_json(self):
        return {
            "privilege": self.privilege,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "password": self.password,
        }


class privilege:
    def __init__(self) -> None:
        """
        privilege management and user server management.
        """
        self._db = init_db(FILE_USER_DATABASE)
        self._load()

    def _load(self):
        self._db.load_db()

    @validate_parameter({"hashed_pw": bytes, "raw_password": bytes})
    def verify_pw(self, hashed_pw: bytes, raw_password: bytes) -> bool:
        """
        comparasion password server generated from argon2.

        Params:
            hashed_pw: your hashed password server generated.
            raw_password: raw password or literal password, plaintext.

        Return:
            if it right password, it will return True.
        """
        hashed_password = None
        if isinstance(hashed_pw, bytes):
            hashed_password = hashed_pw
        else:
            hashed_password = hashed_pw.encode()

        return verify_password(
            hash=hashed_password,
            password=(
                raw_password
                if isinstance(raw_password, bytes)
                else raw_password.encode()
            ),
        )

    @validate_parameter({"username": str, "password": str})
    def verify_user(self, username: str, password: str) -> Tuple[bool, str]:
        """ """
        database = self._db.read_values
        for user_id, cred in database.items():
            if cred.get("username") == username:
                return self.verify_pw(hashed_pw=cred.get("password").encode(), raw_password=password.encode()), "User Verified",

        return False, "User are not in our record."

    @validate_parameter({"username": str, "password": str})
    def add_new_user(
        self, privilege: str, name: str, email: str, username: str, password: str
    ) -> Tuple[bool, str]:
        """
        build new credentials user and registering to database.

        Params:
            username: plaintext user name.
            password: plaintext or raw password.

        Return:
            Double return, first boolean for status and last is string for reason.
        """
        cred = credentials(privilege=privilege, name=name, email=email, username=username, password=password)
        data = cred.to_json

        response = self._db.create_element(
            name_element=uid.token_uuid(), data_value=data
        )
        if response:
            return True, "user successfully added"

        return False, "user can't be add!!"

    @validate_parameter({"user_id": str, "data": Dict[str, str]})
    def update_user(self, user_id: str, data: Dict[str, str]) -> Tuple[bool, str]:
        """
        update credentials user, if user forgot password or username.

        Params:
            user_id: user account id.
            data: data must be dict and fielded like in bottom:
        >>>        {
        >>>            "username": "old or new username here",
        >>>            "password": "old or new password here",
        >>>        }

        Return:
            double return, first boolean for status and last is string for reason.
        """
        cred = credentials(**data)
        data = cred.to_json

        self._db.update_element(name_element=user_id, new_data=data)
        return True, "user credentials successfully updated!"

    @validate_parameter({"user_id": str})
    def delete_user(self, user_id: str) -> bool:
        """
        remove user credentials
        """
        return self._db.delete_element(name_element=user_id)
    
    @validate_parameter({"user_id": str})
    def take_info_user(self, user_id: str) -> Dict[str, str]:
        """ """
        data = self._db.read_values[user_id]
        return credentials(**data)

    def query(self, condition: EllipsisType | None = ..., response: EllipsisType | None = ...) -> Any:
        """ """
        return self._db.read_values
    
    def where_is_userid(self, username: str) -> str:
        """ """
        for user_id, value in self.query():
            if username == value["username"]:
                return user_id
        
        return False
    
    def len_all_user(self) -> int:
        return len(self._db.read_values)