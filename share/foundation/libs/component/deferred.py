class Deferred:
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self._instance = None

    def _load(self):
        if self._instance is None:
            self._instance = self.app.spawn(self.name)
        return self._instance

    def __getattr__(self, item):
        return getattr(self._load(), item)
