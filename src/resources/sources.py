from typing import Any, Dict


class SourceLibrary:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def add_source(self, url: str, metadata: Dict[str, Any]) -> None:
        self._store[url] = metadata

    def get_source(self, url: str) -> Dict[str, Any]:
        return self._store.get(url, {})

    def all_sources(self):
        return list(self._store.values())


