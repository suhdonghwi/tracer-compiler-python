from pathlib import Path
from uuid import uuid1
import json

from .models import FileInfo, NodeInfo


def load_metadata_files(root_path: Path):
    metadata_files = root_path.rglob("*.tracer-metadata.json")

    file_mappings: dict[str, FileInfo] = {}
    node_mappings: dict[str, NodeInfo] = {}

    for metadata_file_path in metadata_files:
        metadata = json.load(metadata_file_path.open())

        file_uuid = str(uuid1())
        file_mappings[file_uuid] = FileInfo(metadata["path"], metadata["original_code"])

        for node_id, node_metadata in metadata["node_mappings"].items():
            node_mappings[node_id] = NodeInfo(
                file_uuid, node_metadata["begin_offset"], node_metadata["end_offset"]
            )

    return file_mappings, node_mappings
