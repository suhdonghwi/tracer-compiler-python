from pathlib import Path
from typing import Any
import json


from .metadata import load_metadata_files
from .trace_manager import TraceManager
from .json_encoder import DataclassJSONEncoder


root_path = Path(__file__).parent.parent
metadata_file_strings = load_metadata_files(root_path)


trace = TraceManager()


def begin_module(node_id: str):
    trace.push_frame(node_id)


def end_module(node_id: str):
    frame_trace = trace.pop_frame(node_id)

    if trace.is_frame_stack_empty():
        print(json.dumps(frame_trace, cls=DataclassJSONEncoder, indent=2))


def begin_func(node_id: str):
    trace.push_frame(node_id)


def end_func(node_id: str):
    trace.pop_frame(node_id)


def begin_stmt(node_id: str):
    trace.push_node(node_id)


def end_stmt(node_id: str):
    trace.pop_node(node_id)


def begin_expr(node_id: str):
    trace.push_node(node_id)

    return node_id


def end_expr(node_id: str, value: Any):
    trace.pop_node(node_id)

    return value
