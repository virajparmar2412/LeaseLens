import json
from typing import Any


def dumps(data: Any) -> str:
    return json.dumps(data)


def loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    return json.loads(raw)
