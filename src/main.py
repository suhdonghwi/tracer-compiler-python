import shutil
import sys
from pathlib import Path

from instrument import instrument_code
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


def copy_tracer_module(output_directory_path: Path) -> Path:
    source_tracer_module_path = Path(__file__).parent / "source_tracer_module"
    dest_tracer_module_path = output_directory_path / "__tracer__"

    shutil.copytree(source_tracer_module_path, dest_tracer_module_path)

    return dest_tracer_module_path


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
    tracer_module_path = copy_tracer_module(output_directory_path)

    for source_path, destination_path in source_dest_pairs:
        if source_path.suffix != ".py":
            continue

        print(f"Processing {source_path}")

        source_code = source_path.read_text()
        instrumented_code, metadata_json = instrument_code(
            source_code,
            source_path,
            destination_path,
            source_path.as_posix(),
            tracer_module_path,
        )

        write_to_ensured_path(destination_path, instrumented_code)
        write_to_ensured_path(
            destination_path.with_suffix(".tracer-metadata.json"), metadata_json
        )
