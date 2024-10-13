from dataclasses import dataclass
from typing import Tuple, Any

Span = Tuple[int, int]
NodeLoc = Tuple[str, Span]


@dataclass
class Trace:
    location: NodeLoc


@dataclass
class FrameTrace(Trace):
    children: list[tuple[Span, Trace]]


class TraceManager:
    def __init__(self):
        self.node_stack: list[NodeLoc] = []
        self.frame_stack: list[Any] = []

    def push_node(self, node_loc: NodeLoc):
        self.node_stack.append(node_loc)

    def pop_node(self, node_loc: NodeLoc):
        while self.node_stack:
            top_node_loc = self.node_stack.pop()

            if top_node_loc == node_loc:
                return top_node_loc
            else:
                # This case can happen if the expression is `sys.exit()`, for example.
                # Keep popping until we find the matching node.
                pass

        raise ValueError("Mismatched begin/end node")

    def push_frame(self, frame_node_loc: NodeLoc):
        self.frame_stack.append("start_frame")
        self.frame_stack.append(frame_node_loc)

    def pop_frame(self, frame_node_loc: NodeLoc):
        caller_node_span = self.node_stack[-1][1] if self.node_stack else None

        self.frame_stack.append("end_frame")
        self.frame_stack.append(frame_node_loc)
        self.frame_stack.append(caller_node_span)

    def is_frame_stack_empty(self):
        return len(self.node_stack) == 0
