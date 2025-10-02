import time
from typing import Any, Dict, List, Optional


class ResearchNotes:
    def __init__(self):
        self._notes: List[Dict[str, Any]] = []

    def save_note(self, content: str, tags: List[str], source_url: Optional[str] = None) -> Dict[str, Any]:
        note = {
            "id": len(self._notes) + 1,
            "content": content,
            "tags": tags,
            "source_url": source_url,
            "created_at": time.time(),
        }
        self._notes.append(note)
        return note

    def list_notes(self) -> List[Dict[str, Any]]:
        return list(self._notes)


