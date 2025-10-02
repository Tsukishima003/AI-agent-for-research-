from typing import Iterable, Mapping


def validate_required_fields(params: Mapping, required_fields: Iterable[str]) -> None:
    missing = [f for f in required_fields if f not in params or params[f] in (None, "")]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")


