import random
import time
import sys

from typing import Union


class DelayManager:
    def __init__(
        self,
        min_sec: int = 10,
        max_sec: int = 90,
        skip_chance: Union[float, int] = 0.0,
        progressive: bool = False,
    ):
        self.min_sec = min_sec
        self.max_sec = max_sec

        self.skip_chance = skip_chance
        self.progressive = progressive
        self.counter: int = 0

    def set_range(self, min_sec: int, max_sec: int) -> None:
        self.min_sec = min_sec
        self.max_sec = max_sec
        print(f"[DELAY] Range updated! -> {self.min_sec}-{self.max_sec} second.")

    def set_skip_chance(self, chance: float) -> None:
        self.skip_chance = chance
        print(f"[DELAY] Skip chance set to {self.skip_chance * 100:.0f}%")

    def wait(self) -> None:
        self.counter += 1

        if random.random() < self.skip_chance:
            print("[DELAY] Skipped!")
            return

        scale = 1 + (self.counter * 0.1) if self.progressive else 1
        value = int(random.randint(self.min_sec, self.max_sec) * scale)

        self._countdown(value)

    def _countdown(self, value: int) -> None:
        for i in range(value, 0, -1):
            sys.stdout.write(f"\r[DELAY] Waiting {i} second..")
            sys.stdout.flush()
            time.sleep(1)
        print("[DELAY] Done!")
