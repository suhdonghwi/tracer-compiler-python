import ast
from pathlib import Path

from utils.file_processing import relative_walk_up

def make_tracer_module_import_node(
    importer_path: Path, import_target_path: Path
):
    identifier = import_target_path.with_suffix('').name

    relative_path = relative_walk_up(import_target_path, importer_path.parent)
    relative_path_parts = relative_path.parts

    parent_dir_count = sum(1 for part in relative_path_parts if part == "..")
    level = parent_dir_count + 1

    return ast.ImportFrom(
        names=[ast.alias(name=identifier, asname=None)],
        level=level,
    )


