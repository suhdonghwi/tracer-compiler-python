import json
from pathlib import Path


def make_source_file_metadata_json(file_id: str, source_code: str, path: Path):
    metadata = {
        "file_id": file_id,
        "content": source_code,
        "path": path.as_posix(),
    }

    return json.dumps(metadata, indent=2)
