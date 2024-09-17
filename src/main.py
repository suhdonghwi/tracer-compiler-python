import ast
import json
import os
import sys
from typing import Tuple

from instrumentation_transformer import InstrumentationTransformer
from node_id_mapped_ast import NodeId, NodeIdMappedAST
from source_file import SourceFile


def get_py_files_inside_directory(directory_path: str) -> list[str]:
    paths: list[str] = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                paths.append(path)

    return paths


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

    return json.dumps({
        "path": source_file.path,
        "content": source_file.content,
        "node_id_to_range": node_id_to_range_json_dict,
    })


if __name__ == "__main__":
    input_path = sys.argv[1]
    source_file_paths = []

    if os.path.isdir(input_path):
        source_file_paths = get_py_files_inside_directory(input_path)
    elif os.path.isfile(input_path):
        source_file_paths = [input_path]

    source_files = [
        SourceFile.from_path(source_file_path) for source_file_path in source_file_paths
    ]

    if len(source_files) == 0:
        print("no source files found")
        sys.exit(1)

    print(len(source_files), "source files found")
    location_maps: list[str] = []

    for source_file in source_files:
        raw_ast = ast.parse(source_file.content)
        node_id_mapped_ast = NodeIdMappedAST(raw_ast)
        transformed_ast = InstrumentationTransformer(node_id_mapped_ast).transform()

        location_map = make_location_map(source_file, node_id_mapped_ast)
        location_maps.append(location_map)

    print(location_maps)
        # print(source_file.path)
