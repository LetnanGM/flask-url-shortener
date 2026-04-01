from .system import client as cl


class termutil:
    def __init__(self):
        self.client: str = cl.OperatingSystem

    @property
    def clean_output(self) -> None:
        import os

        os.system("cls") if self.client == "Windows" else os.system("clear")

    def exit_(sigterm, sigint) -> None:
        print("+=> Exiting!")
        exit(0)
