from pathlib import Path
from typing import Any

from .serialize import serialize_trace
from .trace_manager import FrameTrace, TraceManager

root_path = Path(__file__).parent.parent
trace = TraceManager()


def write_output(trace: FrameTrace):
    serialized_trace = serialize_trace(trace)

    output_file_path = Path(__file__).parent / "trace.json"
    with open(output_file_path, "w") as f:
        f.write(serialized_trace)


def begin_module(node_id: str):
    trace.push_frame(node_id)


def end_module(node_id: str):
    frame_trace = trace.pop_frame(node_id)

    if trace.is_frame_stack_empty():
        write_output(frame_trace)


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
