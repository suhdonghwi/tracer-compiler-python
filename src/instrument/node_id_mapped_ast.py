import ast
from uuid import UUID, uuid1

NodeId = UUID


class NodeIdMappedAST:
    node_id_to_node: dict[NodeId, ast.AST] = {}
    node_to_node_id: dict[ast.AST, NodeId] = {}

    def __init__(self, input_ast: ast.Module):
        self.raw_ast = input_ast

        for node in ast.walk(self.raw_ast):
            node_id = uuid1()
            self.node_id_to_node[node_id] = node
            self.node_to_node_id[node] = node_id

    def get_node_id(self, node: ast.AST) -> NodeId:
        node_id = self.node_to_node_id.get(node)

        if node_id is None:
            raise ValueError("Node not found in mapped source files")

        return node_id

    def items(self):
        return self.node_id_to_node.items()
