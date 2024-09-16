import ast
from uuid import uuid1, UUID

from source_file import SourceFile

NodeId = UUID


class IdMappedSourceFile:
    node_id_to_node: dict[NodeId, ast.AST] = {}
    node_to_node_id: dict[ast.AST, NodeId] = {}

    def __init__(self, source_file: SourceFile):
        self.original_source_file = source_file
        self.ast = ast.parse(source_file.content)

        for node in ast.walk(self.ast):
            node_id = uuid1()
            self.node_id_to_node[node_id] = node
            self.node_to_node_id[node] = node_id

    def get_node_id(self, node: ast.AST) -> NodeId:
        node_id = self.node_to_node_id.get(node)

        if node_id is None:
            raise ValueError("Node not found in mapped source files")

        return node_id
