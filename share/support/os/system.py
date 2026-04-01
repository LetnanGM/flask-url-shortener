import os
from dataclasses import dataclass


@dataclass(frozen=True)
class client:
    import platform

    OperatingSystem = platform.uname()[0]
    Architecture = platform.architecture()
    Processor = platform.processor()
    PythonVer = platform.python_version()
    Machine = platform.machine()
    System = platform.system()
    USER = (
        os.getenv("USERNAME", "username")
        if OperatingSystem == "Windows"
        else os.getlogin()
    )
