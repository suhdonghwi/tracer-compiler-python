from pathlib import Path
from typing import Any
import json


from .metadata import load_metadata_files
from .trace_manager import FrameTrace, TraceManager
from .json_encoder import DataclassJSONEncoder


root_path = Path(__file__).parent.parent
metadata_file_strings = load_metadata_files(root_path)


trace = TraceManager()


def write_trace_output(frame_trace: FrameTrace):
    trace_output_json = (
        "{"
        '"metadata_list": [' + ",".join(metadata_file_strings) + "],"
        '"trace": ' + json.dumps(frame_trace, cls=DataclassJSONEncoder) + "}"
    )

    output_file_path = Path(__file__).parent / "trace_output.json"
    with open(output_file_path, "w") as f:
        f.write(trace_output_json)


def begin_module(node_id: str):
    trace.push_frame(node_id)


def end_module(node_id: str):
    frame_trace = trace.pop_frame(node_id)

    if trace.is_frame_stack_empty():
        write_trace_output(frame_trace)


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
