import ast
import json
from pathlib import Path
from typing import Any

from .node_id_mapping import NodeIdMapping


def make_tracer_metadata_json(
    original_code: str,
    path: Path,
    node_id_mapping: NodeIdMapping
):
    node_mappings: dict[str, Any] = {}

    for node_id, node in node_id_mapping.items():
        if isinstance(node, ast.Module):
            node_mappings[str(node_id)] = {
                "begin_offset": 0,
                "end_offset": len(original_code),
            }

        elif isinstance(node, (ast.stmt, ast.expr)):
            if node.end_col_offset is None:
                raise ValueError("Node has no end_col_offset")

            node_mappings[str(node_id)] = {
                "begin_offset": node.col_offset,
                "end_offset": node.end_col_offset,
            }

    tracer_metadata = {
        "original_code": original_code,
        "path": path.as_posix(),
        "node_mappings": node_mappings,
    }

    return json.dumps(tracer_metadata, indent=2)
