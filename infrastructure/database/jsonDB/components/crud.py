

class OperateC:
    @property
    def read_values(self):
        return self._db

    def create_element(self, name_element, data_value):
        if not isinstance(data_value, dict):
            raise TypeError("'data' must be dict!")

        if not isinstance(name_element, str):
            raise TypeError("'name_element' must be str.")

        if name_element in self._db:
            return False  # optional: biar gak overwrite diam-diam

        self._db[name_element] = data_value
        self.reload_db()
        return True

    def update_element(self, name_element, new_data):
        if name_element in self._db:
            self._db[name_element] = new_data
            self.reload_db()
            return True
        return False

    def delete_element(self, name_element):
        if name_element in self._db:
            del self._db[name_element]
            self.reload_db()
            return True
        return False
