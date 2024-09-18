import ast
import os
import shutil
import sys
from pathlib import Path
from typing import Tuple

from instrumentation_transformer import InstrumentationTransformer
from location_map import make_location_map
from node_id_mapped_ast import NodeIdMappedAST
from source_file import SourceFile


def get_py_files_inside_directory(directory_path: Path) -> list[Path]:
    return [file_path for file_path in directory_path.rglob("*.py")]


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


def write_instrumented_code(output_path: Path, instrumented_code: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(instrumented_code)


def clear_output_directory(output_directory: Path):
    if output_directory.exists() and output_directory.is_dir():
        shutil.rmtree(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py <input_path> <output_directory>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    source_dest_pairs: list[Tuple[Path, Path]] = []

    if input_path.is_file():
        source_dest_pairs = [(input_path, output_path / input_path.name)]
    elif input_path.is_dir():
        source_dest_pairs = [
            (
                py_file_path,
                output_path / py_file_path.relative_to(input_path),
            )
            for py_file_path in get_py_files_inside_directory(input_path)
        ]

    if len(source_dest_pairs) == 0:
        print("No source files found")
        sys.exit(1)

    clear_output_directory(output_path)

    for source_file_path, output_path in source_dest_pairs:
        source_file = SourceFile.from_path(source_file_path)

        instrumented_code, location_map = process_source_file(source_file)
        if instrumented_code:
            write_instrumented_code(output_path, instrumented_code)
        else:
            print(f"Failed to process file: {source_file.path}")
