from datetime import datetime


class dateconf:
    """ """

    DATE = datetime.now()


class date:
    """ """

    @staticmethod
    def get_date_as_now() -> str:
        str(dateconf.DATE.strftime("%d/%m/%Y-%H:%M:%S"))

    @staticmethod
    def get_date_as_ymd() -> str:
        """ """
        return str(dateconf.DATE.strftime("%Y-%m-%d"))

    @staticmethod
    def get_month() -> str | int:
        """ """
        month = dateconf.DATE.month
        if len(str(month)) == 1:
            return str(f"0{month}")

        return month

    @staticmethod
    def get_year() -> str:
        """ """
        return str(dateconf.DATE.year)
