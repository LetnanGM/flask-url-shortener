from typing import Dict, Union
from multiprocessing import Process


class pvmodel:
    dictpid: Dict[Union[callable, str], int] = {}


class process:
    def __init__(self) -> None:
        pass

    def get_name_process_by_pid(self, pid: int) -> str:
        import psutil

        process = psutil.Process(pid=pid)
        return process.name()

    def shutdown(self, pid: str, process: Process | None = ...) -> bool:
        """ """

        if not process:
            import psutil

            process2 = psutil.Process(pid=pid)
            process2.terminate()
            del pvmodel.dictpid[pid]
            return True

        process.terminate()
        del pvmodel.dictpid[pid]
        return True

    def add_new_process(self, pid: int, process_name: str | None = ...) -> bool:
        name = None
        if not process_name:
            name = self.get_name_process_by_pid(pid=pid)
        else:
            name = process_name

        pvmodel.dictpid[pid] = name
