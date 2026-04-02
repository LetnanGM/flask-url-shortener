"""
-----------------------------
Integrated with Highend-dev base.

Developer : LetnanGM
Version   : 1.3.0
Type      : Base Project
-----------------------------

Service   : URLShortener
Type      : URL Shortener as a Service (USaaS)
Version   : 1.2.0
Author    : LetnanGM
Github    : @LetnanGM
"""

from typing import Dict, Tuple, Any
from .components.register import COperate
from share.contract.database import Storage
from share.shared.handler.decorator import validate_parameter
from data.configuration.external.url_shortener.config import CLIENT_DATABASE


class ShortenService(COperate):
    def __init__(self, storage: Storage):
        super().__init__()
        self._db: Storage = storage(CLIENT_DATABASE)
        self._load()

    def _load(self):
        self._db.load_db()
        
    @property
    def read_values(self):
        return self._db.read_values

    @validate_parameter({"pack_id": str})
    def get_element(self, pack_id: str) -> Dict[str, str]:
        """ """
        if pack_id in self._db.read_values.keys():
            return self._db.read_values[pack_id]

        return {}

    @validate_parameter({"shorten_id": str})
    def find_Packid_With_Shorten_ID(self, shorten_id: str) -> str | bool:
        for pack_id, values in self._db.read_values.items():
            if values.get("alias") == shorten_id:
                return pack_id

    @validate_parameter({"pack_id": str})
    def get_redirect(self, pack_id: str) -> str:
        """ """
        response = self.get_element(pack_id=pack_id)

        return response["longUrl"]

    @validate_parameter({"pack_id": str, "userId": str})
    def add_click(self, pack_id: str, userId: str) -> bool:
        """ """
        data = self.get_element(pack_id)
        assert data is not None

        data_userid = str(data.get("userId"))
        if userId == data_userid:
            click = data.get("clicks")
            click += 1
            data["clicks"] = click
            self._db.update_element(pack_id, data)
            return True
        
        return False

    @validate_parameter({"pack_id": str, "userId": str})
    def add_visitor(self, pack_id: str, userId: str) -> bool:
        """ """
        data = self.get_element(pack_id)
        assert data is not None

        data_userid = data.get("userId")
        if userId == data_userid:
            visitor = data.get("visitor")
            visitor += 1
            data["visitor"] = visitor
            self._db.update_element(pack_id, data)
            return True
        return False

    # QUERY LAYER
    def where(self, pack_id: str) -> Tuple[dict, int]:
        position: int = 0
        for i, value in self._db.read_values.items():
            position += 1
            if i == pack_id:
                return value, position

    def where_x(self, condition: Any) -> Any:
        for i, value in self._db.read_values.items():
            if condition:
                return value

    def len_all_what(self, object: str = "shortenedurl") -> int:
        """
        object must be 'shortenedurl', 'click', 'visitor', 'user'.
        """ 
        
        match object:
            case "shortenedurl":
                return len(self.read_values)
            case "click":
                temp = []
                value = 0
                for object_1, object_2 in self.read_values.items():
                    temp.append(object_2.get("clicks"))
                
                for click in temp:
                    value += click
                    
                del temp
                return value
            
            case "visitor":
                temp = []
                value = 0
                for object_1, object_2 in self.read_values.items():
                    temp.append(object_2.get("visitor"))
                
                for visitor in temp:
                    value += visitor
                    
                del temp
                return value
            
            case "user":
                from application.bootstrap import init_MS
                return init_MS().len_all_user()
            case _:
                raise ValueError("Unknown object and object doesn't identified.")
