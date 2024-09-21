import sys
from pathlib import Path

from instrument import instrument_source_file
from source_file import SourceFile
from utils.file_processing import (
    clear_directory,
    get_files_inside_directory,
    write_to_ensured_path,
)


def get_source_dest_pairs(input_path: Path, output_directory_path: Path):
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

    return source_dest_pairs


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py <input_path> <output_directory>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_directory_path = Path(sys.argv[2])

    source_dest_pairs = get_source_dest_pairs(input_path, output_directory_path)

    if len(source_dest_pairs) == 0:
        print("No source files found")
        sys.exit(1)

    print(f"Found {len(source_dest_pairs)} source files")
    clear_directory(output_directory_path)

    for source_file_path, destination_path in source_dest_pairs:
        print(f"Processing {source_file_path}")
        if source_file_path.suffix != ".py":
            continue

        source_file = SourceFile.from_path(source_file_path)
        instrumented_code, metadata_json = instrument_source_file(source_file)

        write_to_ensured_path(destination_path, instrumented_code)
        write_to_ensured_path(
            destination_path.with_suffix(".tracer-metadata.json"), metadata_json
        )
