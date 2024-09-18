import shutil
from pathlib import Path
from typing import Tuple


def get_py_files_inside_directory(directory_path: Path) -> list[Path]:
    return [file_path for file_path in directory_path.rglob("*.py")]


def get_source_dest_pairs(
    input_path: Path, output_directory_path: Path
) -> list[Tuple[Path, Path]]:
    source_dest_pairs: list[Tuple[Path, Path]] = []

    if input_path.is_file():
        source_dest_pairs = [(input_path, output_directory_path / input_path.name)]
    elif input_path.is_dir():
        source_dest_pairs = [
            (
                py_file_path,
                output_directory_path / py_file_path.relative_to(input_path),
            )
            for py_file_path in get_py_files_inside_directory(input_path)
        ]

    return source_dest_pairs


def clear_directory(directory: Path):
    if directory.exists() and directory.is_dir():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)


def write_to_path(destination_path: Path, content: str):
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with open(destination_path, "w", encoding="utf-8") as output_file:
        output_file.write(content)
