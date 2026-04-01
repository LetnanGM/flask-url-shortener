from ....data.configuration.sys.SecurityConfig import SecurityConfig
from ....utils.logging.childLogger import CSRFLogger
from share.support.parser.url import URLParse as URLHelper
from typing import Tuple


class Header:
    def __init__(
        self, request_host: str, method: str, origin: str, referer: str
    ) -> None:
        self.request_host = request_host
        self.method = method
        self.origin = origin
        self.referer = referer

    def method_validator(self, method: str) -> str:
        """
        validating method state request.
        """
        if len(method) == 0 or not method:
            raise ValueError("argument 'method' are empty!")

        if method in SecurityConfig.STATE_METHODS_REQ:
            return method

    def origin_validator(self, origin: str) -> Tuple[bool, str]:
        if not origin:
            return False, "Missing Origin headers"

        origin_host = URLHelper(url=origin).netloc.split(":")[0]
        request_host = self.request_host.split(":")[0]

        if origin_host != request_host and origin not in SecurityConfig.TRUSTED_ORIGIN:
            return False, f"Invalid Origin: {origin}"

        return True, "Valid"

    def referrer_validator(self, referrer: str) -> Tuple[bool, str]:
        if not referrer:
            return False, "Missing Referref headers"

        request_host = self.request_host.split(":")[0]
        referrer_host = URLHelper(url=referrer).netloc.split(":")[0]

        if (
            referrer_host != request_host
            and referrer not in SecurityConfig.TRUSTED_ORIGIN
        ):
            return False, f"Invalid Referrer: {referrer}"

        return True, "Valid"

    def _validate_origin_referer(self) -> Tuple[bool, str]:
        """Validate Origin and Referer headers"""

        # For state-changing methods, require Origin or Referer
        if self.method_validator(method=self.method):
            resp_origin = self.origin_validator(origin=self.origin)
            resp_referrer = self.referrer_validator(referrer=self.referer)

            CSRFLogger.vsilent(resp_origin)
            CSRFLogger.vsilent(resp_referrer)

            if resp_origin and resp_referrer:
                return True, "Valid"

        return False, "[validate_origin_referer] we have some error in here."
