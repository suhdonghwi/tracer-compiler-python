import ast
import os
import sys

from instrumentation_transformer import InstrumentationTransformer
from location_map import make_location_map_json
from node_id_mapped_ast import NodeIdMappedAST
from source_file import SourceFile


def get_py_files_inside_directory(directory_path: str) -> list[str]:
    paths: list[str] = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                paths.append(path)

    return paths


def construct_import_from_node(
    start_path: str, import_target_path: str, name_to_import: str
):
    relative_path = os.path.relpath(import_target_path, os.path.dirname(start_path))
    relative_path_parts = relative_path.split(os.sep)

    parent_dir_count = relative_path_parts.count("..")

    level = parent_dir_count + 1
    module_name = ".".join(relative_path_parts[parent_dir_count:]).rsplit(".py", 1)[0]

    return ast.ImportFrom(
        module=module_name,
        names=[ast.alias(name=name_to_import, asname=None)],
        level=level,
    )


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    tracer_module_path = sys.argv[3]

    source_file = SourceFile.from_path(input_path)

    raw_ast = ast.parse(source_file.content)
    node_id_mapped_ast = NodeIdMappedAST(raw_ast)
    transformed_ast = InstrumentationTransformer(node_id_mapped_ast).transform()

    location_map_json = make_location_map_json(source_file, node_id_mapped_ast)

    constructed_import_from_node = construct_import_from_node(
        output_path, tracer_module_path, "__tracer__"
    )
    print(ast.unparse(constructed_import_from_node))
