import sys
from pathlib import Path
from uuid import uuid1

from instrument import instrument_code
from tracer_metadata import make_tracer_metadata_json
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
        filtered_files = [
            file_path
            for file_path in files_inside_input_directory
            if "__pycache__" not in file_path.parts
        ]

        source_dest_pairs = [
            (
                file_path,
                output_directory_path / file_path.relative_to(input_path),
            )
            for file_path in filtered_files
        ]

    return source_dest_pairs


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py <input_path> <output_directory>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_directory_path = Path(sys.argv[2])

    source_dest_pairs = get_source_dest_pairs(input_path, output_directory_path)

    if not source_dest_pairs:
        print("No source files found")
        sys.exit(1)

    print(f"Found {len(source_dest_pairs)} source files")

    clear_directory(output_directory_path)

    for source_path, destination_path in source_dest_pairs:
        if source_path.suffix != ".py":
            continue

        print(f"Processing {source_path}")

        source_code = source_path.read_text()
        file_id = str(uuid1())

        instrumented_code = instrument_code(
            source_code,
            file_id,
        )

        metadata_json = make_tracer_metadata_json(
            file_id=file_id, original_code=source_code, path=source_path
        )

        write_to_ensured_path(destination_path, instrumented_code)
        write_to_ensured_path(
            destination_path.with_suffix(".tracer_metadata.json"), metadata_json
        )
