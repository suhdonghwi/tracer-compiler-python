from dataclasses import dataclass
from typing import Union


@dataclass
class FrameTrace:
    frame_node_id: str
    caller_node_id: Union[str, None]
    children: list["FrameTrace"]


class TraceManager:
    def __init__(self):
        self.node_id_stack: list[str] = []
        self.frame_trace_stack: list[FrameTrace] = []

    def push_node(self, node_id: str):
        self.node_id_stack.append(node_id)

    def pop_node(self, node_id: str):
        if self.node_id_stack[-1] != node_id:
            raise ValueError("Mismatched begin/end stmt")

        self.node_id_stack.pop()

    def push_frame(self, frame_node_id: str):
        caller_node_id = self.node_id_stack[-1] if self.node_id_stack else None

        self.frame_trace_stack.append(FrameTrace(frame_node_id, caller_node_id, []))

    def pop_frame(self, frame_node_id: str):
        if self.frame_trace_stack[-1].frame_node_id != frame_node_id:
            raise ValueError("Mismatched begin/end frame")

        popped_frame_trace = self.frame_trace_stack.pop()

        if len(self.frame_trace_stack) > 0:
            self.frame_trace_stack[-1].children.append(popped_frame_trace)

        return popped_frame_trace

    def is_frame_stack_empty(self):
        return len(self.frame_trace_stack) == 0
