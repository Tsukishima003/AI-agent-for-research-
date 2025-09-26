import asyncio
import time


class AsyncRateLimiter:
    def __init__(self, rps: float):
        self.min_interval = 1.0 / max(rps, 0.001)
        self._last_time = 0.0
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            to_wait = self.min_interval - (now - self._last_time)
            if to_wait > 0:
                await asyncio.sleep(to_wait)
            self._last_time = time.monotonic()


