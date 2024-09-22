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


node_stack: list[NodeInfo] = []


def begin_frame(uuid: str):
    if node_stack:
        last_node = node_stack[-1]
        file_info = file_mappings[last_node.file_uuid]

        print(
            f"My caller is '{file_info.original_code[last_node.begin_offset:last_node.end_offset]}'"
        )
    pass


def end_frame(uuid: str):
    pass


def begin_stmt(uuid: str):
    node = node_mappings[uuid]
    node_stack.append(node)


def end_stmt(uuid: str):
    if node_stack[-1] != node_mappings[uuid]:
        raise ValueError("Mismatched begin/end stmt")

    node_stack.pop()


def begin_expr(uuid: str):
    node = node_mappings[uuid]
    node_stack.append(node)

    return uuid


def end_expr(uuid: str, value: Any):
    if node_stack[-1] != node_mappings[uuid]:
        raise ValueError("Mismatched begin/end stmt")

    node_stack.pop()

    return value
