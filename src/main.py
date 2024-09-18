import ast
import os
import sys
from pathlib import Path

from file_processing import clear_directory, get_source_dest_pairs, write_to_path
from instrumentation_transformer import InstrumentationTransformer
from location_map import make_location_map
from node_id_mapped_ast import NodeIdMappedAST
from source_file import SourceFile


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


def process_source_file(source_file: SourceFile):
    raw_ast = ast.parse(source_file.content)
    node_id_mapped_ast = NodeIdMappedAST(raw_ast)

    instrumented_ast = InstrumentationTransformer(node_id_mapped_ast).transform()
    instrumented_code = ast.unparse(instrumented_ast)

    location_map = make_location_map(source_file, node_id_mapped_ast)

    return instrumented_code, location_map


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py <input_path> <output_directory>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_directory_path = Path(sys.argv[2])

    if not output_directory_path.exists():
        output_directory_path.mkdir(parents=True, exist_ok=True)

    source_dest_pairs = get_source_dest_pairs(input_path, output_directory_path)

    if len(source_dest_pairs) == 0:
        print("No source files found")
        sys.exit(1)

    clear_directory(output_directory_path)

    for source_file_path, destination_path in source_dest_pairs:
        source_file = SourceFile.from_path(source_file_path)
        instrumented_code, location_map = process_source_file(source_file)

        write_to_path(destination_path, instrumented_code)
