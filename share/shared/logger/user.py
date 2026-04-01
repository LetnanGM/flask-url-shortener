from dataclasses import dataclass


@dataclass
class logger:
    verbose: int = 1


@dataclass
class client:
    logger = logger


class _client:
    def __call__(self, *args, **kwds):
        from data.configuration.internal.system import CLIENT_CONFIG
        from share.support.file import File

        instance = File(CLIENT_CONFIG).Read()
        data = instance.json
        return client(**data)
