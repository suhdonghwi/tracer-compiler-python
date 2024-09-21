from pathlib import Path
import json
from typing import Any
from uuid import uuid1
from dataclasses import dataclass

cwd = Path(__file__).parent
metadata_files = cwd.rglob("*.tracer-metadata.json")


@dataclass
class FileInfo:
    path: str
    original_code: str


@dataclass
class NodeInfo:
    file_uuid: str
    begin_offset: int
    end_offset: int


file_mappings = {}
node_mappings = {}

for metadata_file_path in metadata_files:
    metadata = json.load(metadata_file_path.open())

    file_uuid = str(uuid1())
    file_mappings[file_uuid] = FileInfo(metadata["path"], metadata["original_code"])

    for node_id, node_metadata in metadata["node_mappings"].items():
        node_mappings[node_id] = NodeInfo(
            file_uuid, node_metadata["begin_offset"], node_metadata["end_offset"]
        )


def begin_frame(uuid: str):
    pass


def end_frame(uuid: str):
    pass


def begin_stmt(uuid: str):
    pass


def end_stmt(uuid: str):
    pass


def begin_expr(uuid: str):
    return uuid


def end_expr(uuid: str, value: Any):
    return value
