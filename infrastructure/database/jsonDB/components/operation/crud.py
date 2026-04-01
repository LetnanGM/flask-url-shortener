from typing import Dict, Any
from .. import vmodel


class operation:
    @property
    def read_values(self) -> Dict[str, Any]:
        """
        database value from variable model as TEMPORARY_DATABASE.
        saving database value in memory as variable.

        Return:
            dictionary with first child string and Any in last.
        """
        return vmodel.TEMPORARY_DATABASE

    def create_element(self, name_element: str, data_value: Dict[str, Any]) -> bool:
        """
        creating new element to database.

        Params:
            name_element: ident or name element.
            data_value: valuable data.

        Return:
            true if data successfully
        """
        if not isinstance(data_value, dict):
            raise TypeError("'data' must be dict!")

        if not isinstance(name_element, str):
            raise TypeError("'name_element' must be str.")

        assert data_value != ""
        assert name_element != ""

        vmodel.TEMPORARY_DATABASE[name_element] = data_value

        if name_element in vmodel.TEMPORARY_DATABASE.keys():
            return True

    def update_element(self, name_element: str, new_data: Dict[str, Any]) -> bool:
        """ """
        if not isinstance(name_element, str):
            raise TypeError("'name_element' must be str")

        if not isinstance(new_data, dict):
            raise TypeError("'new_data' must be dict.")

        if name_element in vmodel.TEMPORARY_DATABASE.keys():
            vmodel.TEMPORARY_DATABASE[name_element] = new_data
            return True

        return False

    def delete_element(self, name_element: str) -> bool:
        if name_element in vmodel.TEMPORARY_DATABASE.keys():
            del vmodel.TEMPORARY_DATABASE[name_element]
            return True

        return False
