import ast
from typing import Tuple

from source_file import SourceFile

from .node_id_mapped_ast import NodeId, NodeIdMappedAST


def make_location_map(source_file: SourceFile, node_id_mapped_ast: NodeIdMappedAST):
    node_id_to_range: dict[NodeId, Tuple[int, int]] = {}

    for node_id, node in node_id_mapped_ast.items():
        if isinstance(node, ast.Module):
            node_id_to_range[node_id] = (0, len(source_file.content))
        elif isinstance(node, (ast.stmt, ast.expr)):
            if node.end_col_offset is None:
                raise ValueError("Node has no end_col_offset")

            node_id_to_range[node_id] = (node.col_offset, node.end_col_offset)

    node_id_to_range_json_dict = {
        str(node_id): (start, end) for node_id, (start, end) in node_id_to_range.items()
    }

    return node_id_to_range_json_dict
