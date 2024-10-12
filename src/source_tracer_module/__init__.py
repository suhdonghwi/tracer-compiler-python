from pathlib import Path
from typing import Any

from .serialize import serialize_trace
from .trace_manager import FrameTrace, TraceManager, NodeLoc

root_path = Path(__file__).parent.parent
trace = TraceManager()


def write_output(trace: FrameTrace):
    serialized_trace = serialize_trace(trace)

    output_file_path = Path(__file__).parent / "trace.json"
    with open(output_file_path, "w") as f:
        f.write(serialized_trace)


def begin_module(node_loc: NodeLoc):
    trace.push_frame(node_loc)


def end_module(node_loc: NodeLoc):
    frame_trace = trace.pop_frame(node_loc)

    if trace.is_frame_stack_empty():
        write_output(frame_trace)


def begin_func(node_loc: NodeLoc):
    trace.push_frame(node_loc)


def end_func(node_loc: NodeLoc):
    trace.pop_frame(node_loc)


def begin_stmt(node_loc: NodeLoc):
    trace.push_node(node_loc)


def end_stmt(node_loc: NodeLoc):
    trace.pop_node(node_loc)


def begin_expr(node_loc: NodeLoc):
    trace.push_node(node_loc)

    return node_loc


def end_expr(node_loc: NodeLoc, value: Any):
    trace.pop_node(node_loc)

    return value
