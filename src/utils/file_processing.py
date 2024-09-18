import shutil
from pathlib import Path


def get_files_inside_directory(directory_path: Path) -> list[Path]:
    return [path for path in directory_path.rglob("*") if path.is_file()]


def clear_directory(directory_path: Path):
    if directory_path.exists() and directory_path.is_dir():
        shutil.rmtree(directory_path)
    directory_path.mkdir(parents=True, exist_ok=True)


def write_to_ensured_path(destination_path: Path, content: str):
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with open(destination_path, "w", encoding="utf-8") as output_file:
        output_file.write(content)
