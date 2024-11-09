import json
from pathlib import Path


def make_tracer_metadata_json(file_id: str, original_code: str, path: Path):
    tracer_metadata = {
        "file_id": file_id,
        "original_code": original_code,
        "path": path.as_posix(),
    }

    return json.dumps(tracer_metadata, indent=2)
