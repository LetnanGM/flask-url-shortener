from typing import Dict
from share.support import uid, date
from share.shared.handler.decorator import validate_parameter
from data.configuration.internal.server.webapp import ServerConfig


class COperate:
    def __init__(self) -> None:
        self._BASE_URL = None

    @validate_parameter({"real_url": str})
    def create(self, user_id: str, real_url: str) -> Dict[str, str]:
        """ """
        pack_id: str = uid.token_uuid()
        alias = uid.token_char()
        data: Dict[str, str] = {
            "id": pack_id,
            "userId": user_id,
            "alias": alias,
            "title": "uknown",
            "longUrl": real_url,
            "shortUrl": None,
            "clicks": 0,
            "visitor": 0,
            "created": date.get_date_as_ymd(),
            "status": "active",
            "expiry": None,
        }

        response = self._db.create_element(name_element=pack_id, data_value=data)
        if response:
            return {"status": True, "data": data}

    @validate_parameter({"pack_id": str, "data_value": Dict[str, str]})
    def update(self, pack_id: str, data_value: Dict[str, str]) -> bool:
        """ """

        data = self._db.read_values()
        if pack_id not in data.keys():
            return False

        response = self._db.update_element(name_element=pack_id, new_data=data_value)
        if response:
            return response

        return response

    @validate_parameter({"pack_id": str})
    def delete(self, pack_id: str) -> bool:
        """ """
        response = self._db.delete_element(name_element=pack_id)
        if not response:
            return response
        return response
