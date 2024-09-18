import ast
import os
import sys
from pathlib import Path
from instrument import instrument_source_file

from utils.file_processing import (
    clear_directory,
    get_files_inside_directory,
    write_to_ensured_path,
)
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


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py <input_path> <output_directory>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_directory_path = Path(sys.argv[2])

    source_dest_pairs = []

    if input_path.is_file():
        source_dest_pairs = [(input_path, output_directory_path / input_path.name)]
    elif input_path.is_dir():
        files_inside_input_directory = get_files_inside_directory(input_path)
        source_dest_pairs = [
            (
                file_path,
                output_directory_path / file_path.relative_to(input_path),
            )
            for file_path in files_inside_input_directory
        ]

    if len(source_dest_pairs) == 0:
        print("No source files found")
        sys.exit(1)

    clear_directory(output_directory_path)

    for source_file_path, destination_path in source_dest_pairs:
        if source_file_path.suffix != ".py":
            continue

        source_file = SourceFile.from_path(source_file_path)
        instrumented_code, location_map = instrument_source_file(source_file)

        write_to_ensured_path(destination_path, instrumented_code)
