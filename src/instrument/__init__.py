import ast
from pathlib import Path

from .node_id_mapping import NodeIdMapping
from .ast_transformer import InstrumentationTransformer
from .tracer_metadata import make_tracer_metadata_json


def instrument_code(
    code: str,
    source_path: Path,
    destination_path: Path,
    tracer_module_path: Path,
):
    raw_ast = ast.parse(code)
    node_id_mapping = NodeIdMapping(raw_ast)

    instrumented_ast = InstrumentationTransformer(
        raw_ast,
        lambda node: str(node_id_mapping.get_node_id(node)),
    ).transform()

    instrumented_ast.body = [
        make_tracer_module_import_node(
            destination_path, tracer_module_path, "__tracer__"
        )
    ] + instrumented_ast.body

    instrumented_code = ast.unparse(instrumented_ast)
    metadata_json = make_tracer_metadata_json(code, source_path, node_id_mapping)

    return instrumented_code, metadata_json


def make_tracer_module_import_node(
    importer_path: Path, import_target_path: Path, identifier: str
):
    relative_path = relative_walk_up(import_target_path, importer_path.parent)
    relative_path_parts = relative_path.parts

    parent_dir_count = sum(1 for part in relative_path_parts if part == "..")

    level = parent_dir_count + 1
    module_name = ".".join(relative_path_parts[parent_dir_count:]).rsplit(".py", 1)[0]

    return ast.ImportFrom(
        module=module_name,
        names=[ast.alias(name=identifier, asname=None)],
        level=level,
    )


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
