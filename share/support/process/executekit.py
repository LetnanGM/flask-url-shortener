from .manager import process


class execute:
    def __init__(self) -> None:
        self.proc = process()

    def on_background(self, func_or_classes: callable | type, *args, **kwargs):
        """
        input value in label or index for executing pattern.
        """
        import multiprocessing

        def execute(obj: callable, *args, **kwargs) -> multiprocessing.Process:
            p = multiprocessing.Process(
                target=obj, args=args, kwargs=kwargs, daemon=True
            )
            p.start()

            self.proc.add_new_process(pid=p.pid, process_name=obj.__name__)

        if not func_or_classes:
            raise TypeError("object func_or_classes cannot empty!")

        return execute(obj=func_or_classes, *args, **kwargs)
