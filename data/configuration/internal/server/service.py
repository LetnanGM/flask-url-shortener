from typing import Dict


class Service:
    SERVICE_TITLE: str = "Server FL"
    SERVICE_VERSION: str = "1.0.0"
    STATUS = "Healthy"
    ENDPOINTS: Dict[str, str] = {}

    def __call__(*args, **kwargs) -> None:
        Service.endpoints_load()

        return "Service Loaded!"

    @property
    def to_dict() -> None:
        if not Service.ENDPOINTS:
            Service.endpoints_load()

        return {
            "title": Service.SERVICE_TITLE,
            "version": Service.SERVICE_VERSION,
            "status": Service.STATUS,
            "endpoints": Service.ENDPOINTS,
        }

    @staticmethod
    def endpoints_load() -> Dict:
        import json

        with open("./endpoints.json", "r") as endp:
            Service.ENDPOINTS = json.load(endp)

        return Service.ENDPOINTS

    @staticmethod
    def endpoints_write() -> Dict:
        import json

        with open("./endpoints.json", "w") as endp:
            json.dump(Service.ENDPOINTS, endp, indent=4)
