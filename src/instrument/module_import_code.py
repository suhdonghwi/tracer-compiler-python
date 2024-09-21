from pathlib import Path

from utils.file_processing import relative_walk_up


def make_relative_import_code(importer_path: Path, import_target_path: Path):
    relative_path = relative_walk_up(import_target_path, importer_path.parent)
    relative_path_parts = relative_path.parts

    up_levels = sum(1 for part in relative_path_parts if part == "..")

    import_code = ""
    import_code += "import sys, os\n"
    import_code += (
        "sys.path.append(os.path.join(os.path.dirname(__file__), {}))\n".format(
            ", ".join(["'..'"] * up_levels)
        )
    )
    import_code += "import {}".format(import_target_path.with_suffix("").name)

    return import_code
