import ast
import json
from pathlib import Path
from typing import Any

from .node_id_mapping import NodeIdMapping


def make_tracer_metadata_json(
    original_code: str, path: Path, node_id_mapping: NodeIdMapping
):
    node_mappings: dict[str, Any] = {}

    lines = original_code.splitlines(keepends=True)
    cumulative_line_lengths = [0]

    for line in lines:
        cumulative_line_lengths.append(cumulative_line_lengths[-1] + len(line))

    for node_id, node in node_id_mapping.items():
        if isinstance(node, ast.Module):
            node_mappings[str(node_id)] = {
                "begin_offset": 0,
                "end_offset": len(original_code),
            }

        elif isinstance(node, (ast.stmt, ast.expr)):
            if node.end_lineno is None or node.end_col_offset is None:
                raise ValueError(
                    "Node is missing end line or end column offset information"
                )

            begin_offset = cumulative_line_lengths[node.lineno - 1] + node.col_offset
            end_offset = (
                cumulative_line_lengths[node.end_lineno - 1] + node.end_col_offset
            )

            node_mappings[str(node_id)] = {
                "begin_offset": begin_offset,
                "end_offset": end_offset,
            }

    tracer_metadata = {
        "original_code": original_code,
        "path": path.as_posix(),
        "node_mappings": node_mappings,
    }

    return json.dumps(tracer_metadata, indent=2)
