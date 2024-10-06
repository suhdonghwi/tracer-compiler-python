from typing import cast

try:
    import orjson as json

    orjson_available = True
except ImportError:
    import json
    from .json_encoder import DataclassJSONEncoder

    orjson_available = False

from .trace_manager import FrameTrace


def serialize_trace(trace: FrameTrace):
    trace_json = cast(
        str,
        json.dumps(trace).decode("utf-8")  # type: ignore
        if orjson_available
        else json.dumps(trace, cls=DataclassJSONEncoder),  # type: ignore
    )

    return trace_json
