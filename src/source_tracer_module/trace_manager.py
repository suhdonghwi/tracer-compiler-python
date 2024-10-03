from .models import NodeInfo


class TraceManager:
    def __init__(self):
        self.node_stack = []

    def push_node(self, node: NodeInfo):
        self.node_stack.append(node)

    def pop_node(self, node: NodeInfo):
        if self.node_stack[-1] != node:
            raise ValueError("Mismatched begin/end stmt")

        self.node_stack.pop()
