from pathlib import Path
from typing import Any

from .models import NodeInfo
from .metadata import load_metadata_files

root_path = Path(__file__).parent.parent
file_mappings, node_mappings = load_metadata_files(root_path)

node_stack: list[NodeInfo] = []
trace_result = []


def begin_frame(uuid: str):
    node = node_mappings[uuid]
    caller_node = node_stack[-1] if node_stack else None

    trace_result.append({"type": "frame_call", "callee": node, "caller": caller_node})


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
