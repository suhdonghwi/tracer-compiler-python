from pathlib import Path
from typing import Any

from .serialize import serialize_trace
from .trace_manager import FrameTrace, TraceManager, NodePos

root_path = Path(__file__).parent.parent
trace = TraceManager()


def write_output(trace: FrameTrace):
    serialized_trace = serialize_trace(trace)

    output_file_path = Path(__file__).parent / "trace.json"
    with open(output_file_path, "w") as f:
        f.write(serialized_trace)


def begin_module(node_pos: NodePos):
    trace.push_frame(node_pos)


def end_module(node_pos: NodePos):
    frame_trace = trace.pop_frame(node_pos)

    if trace.is_frame_stack_empty():
        write_output(frame_trace)


def begin_func(node_pos: NodePos):
    trace.push_frame(node_pos)


def end_func(node_pos: NodePos):
    trace.pop_frame(node_pos)


def begin_stmt(node_pos: NodePos):
    trace.push_node(node_pos)


def end_stmt(node_pos: NodePos):
    trace.pop_node(node_pos)


def begin_expr(node_pos: NodePos):
    trace.push_node(node_pos)

    return node_pos


def end_expr(node_pos: NodePos, value: Any):
    trace.pop_node(node_pos)

    return value
