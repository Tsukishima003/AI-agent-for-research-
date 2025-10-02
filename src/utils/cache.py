import time
from typing import Any, Dict, Tuple


class TTLCache:
    def __init__(self, ttl_seconds: float = 600.0):
        self._store: Dict[str, Tuple[float, Any]] = {}
        self._ttl = ttl_seconds

    def get(self, key: str):
        item = self._store.get(key)
        if not item:
            return None
        ts, value = item
        if time.time() - ts > self._ttl:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any):
        self._store[key] = (time.time(), value)


