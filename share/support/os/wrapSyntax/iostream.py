from typing import Any


class InputResponse:
    def __init__(self, response: Any) -> None:
        self.response = response

    def __call__(self) -> Any:
        return self.response if self.response else None

    @property
    def to_str(self) -> str:
        return str(self.response)

    @property
    def to_int(self) -> int:
        return int(self.response)

    @property
    def to_list(self) -> list:
        return list(self.response)

    @property
    def to_dict(self) -> dict:
        return dict(self.response)


class wrapSyntax:
    def ask(prompt: str = "") -> InputResponse:
        """
        The prompt string, if given, is printed to standard output without a
        trailing newline before reading input.

        If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), raise EOFError.
        On *nix systems, readline is used if available.
        """
        return InputResponse(response=input(prompt))

    def writeln(text: Any) -> Any:
        import sys

        sys.stdout.write(text)
        sys.stdout.flush()

    def stream_writeln(text: Any, time_elapsed: int = 0.9) -> Any:
        """
        write stream text into console.
        if user hits EOF (*nix: Ctrl-d, windows: Ctrl-Z+Return).
        raise EOFError.
        """
        import sys
        import time

        for c in text + "\n":
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(time_elapsed)
