from dataclasses import dataclass
from typing import Tuple

Span = Tuple[int, int]
NodeLoc = Tuple[str, Span]


@dataclass
class FrameTrace:
    node_loc: NodeLoc
    children: list[tuple[Span, "FrameTrace"]]


class TraceManager:
    def __init__(self):
        self.node_stack: list[NodeLoc] = []
        self.frame_stack: list[FrameTrace] = []

    def push_node(self, node_loc: NodeLoc):
        self.node_stack.append(node_loc)

    def pop_node(self, node_pos: NodeLoc):
        while self.node_stack:
            top_node_id = self.node_stack.pop()

            if top_node_id == node_pos:
                return top_node_id
            else:
                # This case can happen if the expression is `sys.exit()`, for example.
                # Keep popping until we find the matching node.
                pass

        raise ValueError("Mismatched begin/end node")

    def push_frame(self, frame_node_loc: NodeLoc):
        self.frame_stack.append(FrameTrace(frame_node_loc, []))

    def pop_frame(self, frame_node_loc: NodeLoc):
        if self.frame_stack[-1].node_loc != frame_node_loc:
            raise ValueError("Mismatched begin/end frame")

        popped_frame_trace = self.frame_stack.pop()

        if self.frame_stack:
            if caller_node_loc := self.node_stack[-1]:
                self.frame_stack[-1].children.append(
                    (caller_node_loc[1], popped_frame_trace)
                )

        return popped_frame_trace

    def is_frame_stack_empty(self):
        return len(self.frame_stack) == 0
