import shutil
from pathlib import Path


def get_files_inside_directory(directory_path: Path) -> list[Path]:
    return [
        path
        for path in directory_path.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    ]


def clear_directory(directory_path: Path):
    if directory_path.exists() and directory_path.is_dir():
        shutil.rmtree(directory_path)
    directory_path.mkdir(parents=True, exist_ok=True)


def write_to_ensured_path(destination_path: Path, content: str):
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with open(destination_path, "w", encoding="utf-8") as output_file:
        output_file.write(content)


# pathlib relative_to method does not support walk_up option under Python 3.12
def relative_walk_up(path: Path, base: Path) -> Path:
    common_path = Path(*base.parts)
    while common_path not in path.parents and len(common_path.parts) > 0:
        common_path = common_path.parent

    if common_path == Path("/"):
        raise ValueError(f"Cannot find a relative path from {path} to {base}")

    # Number of `..` required to reach the common path
    up_steps = len(base.parts) - len(common_path.parts)

    # Calculate the relative path from the common base
    relative_path = Path(*[".."] * up_steps) / path.relative_to(common_path)

    return relative_path
