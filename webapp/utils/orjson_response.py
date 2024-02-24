import uuid
from typing import Any

import orjson
from fastapi.responses import ORJSONResponse as BaseORJSONResponse


def orjson_serializer(obj: Any) -> Any:
    if isinstance(obj, uuid.UUID):
        return str(obj)
    return obj


class ORJSONResponse(BaseORJSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, default=orjson_serializer)
