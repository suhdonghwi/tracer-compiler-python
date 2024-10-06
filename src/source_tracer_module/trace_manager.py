from dataclasses import dataclass
from typing import Union, Tuple

NodePos = Tuple[str, int, int]


@dataclass
class FrameTrace:
    node_pos: NodePos
    caller_node_pos: Union[NodePos, None]
    children: list["FrameTrace"]


class TraceManager:
    def __init__(self):
        self.node_stack: list[NodePos] = []
        self.frame_stack: list[FrameTrace] = []

    def push_node(self, node_pos: NodePos):
        self.node_stack.append(node_pos)

    def pop_node(self, node_pos: NodePos):
        while self.node_stack:
            top_node_id = self.node_stack.pop()

            if top_node_id == node_pos:
                return top_node_id
            else:
                # This case can happen if the expression is `sys.exit()`, for example.
                # We keep popping until we find the matching node.
                pass

        raise ValueError("Mismatched begin/end node")

    def push_frame(self, frame_node_pos: NodePos):
        caller_node_id = self.node_stack[-1] if self.node_stack else None

        self.push_node(frame_node_pos)
        self.frame_stack.append(FrameTrace(frame_node_pos, caller_node_id, []))

    def pop_frame(self, frame_node_pos: NodePos):
        if self.frame_stack[-1].node_pos != frame_node_pos:
            raise ValueError("Mismatched begin/end frame")

        self.pop_node(frame_node_pos)
        popped_frame_trace = self.frame_stack.pop()

        if len(self.frame_stack) > 0:
            self.frame_stack[-1].children.append(popped_frame_trace)

        return popped_frame_trace

    def is_frame_stack_empty(self):
        return len(self.frame_stack) == 0
