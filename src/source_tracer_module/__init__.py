from pathlib import Path
from typing import Any


from .metadata import load_metadata_files
from .trace_manager import TraceManager

root_path = Path(__file__).parent.parent
file_mappings, node_mappings = load_metadata_files(root_path)


trace = TraceManager()


def begin_frame(uuid: str):
    node = node_mappings[uuid]
    caller_node = node_stack[-1] if node_stack else None

    trace_result.append({"type": "frame_call", "callee": node, "caller": caller_node})


def end_frame(uuid: str):
    pass


def begin_stmt(uuid: str):
    node = node_mappings[uuid]

    trace.push_node(node)


def end_stmt(uuid: str):
    node = node_mappings[uuid]

    trace.pop_node(node)


def begin_expr(uuid: str):
    node = node_mappings[uuid]

    trace.push_node(node)

    return uuid


def end_expr(uuid: str, value: Any):
    node = node_mappings[uuid]

    trace.pop_node(node)

    return value
