import ast
import json
from typing import Tuple
from uuid import UUID, uuid1

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

    def dumps(self):
        node_id_to_range: dict[NodeId, Tuple[int, int]] = {}

        for node_id, node in self.node_id_to_node.items():
            if isinstance(node, ast.Module):
                node_id_to_range[node_id] = (
                    0,
                    len(self.original_source_file.content),
                )

            if isinstance(node, (ast.stmt, ast.expr)):
                if node.end_col_offset is None:
                    raise ValueError("Node has no end_col_offset")

                node_id_to_range[node_id] = (node.col_offset, node.end_col_offset)

        node_id_to_range_json_dict = {
            str(node_id): (start, end)
            for node_id, (start, end) in node_id_to_range.items()
        }

        data = {
            "path": self.original_source_file.path,
            "content": self.original_source_file.content,
            "node_id_to_range": node_id_to_range_json_dict,
        }

        return json.dumps(data, indent=2)
