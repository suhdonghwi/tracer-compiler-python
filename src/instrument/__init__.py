import ast
from pathlib import Path

from .node_id_mapped_ast import NodeIdMappedAST
from .ast_transformer import InstrumentationTransformer
from .tracer_metadata import make_tracer_metadata_json


def instrument_code(
    code: str,
    source_file_path: Path,
    destination_path: Path,
    tracer_module_path: Path,
):
    raw_ast = ast.parse(code)
    node_id_mapped_ast = NodeIdMappedAST(raw_ast)

    instrumented_ast = InstrumentationTransformer(
        raw_ast,
        lambda node: str(node_id_mapped_ast.get_node_id(node)),
    ).transform()

    instrumented_ast.body.insert(
        0,
        construct_import_from_node(destination_path, tracer_module_path, "__tracer__"),
    )

    instrumented_code = ast.unparse(instrumented_ast)
    metadata_json = make_tracer_metadata_json(
        source_file_path, code, node_id_mapped_ast
    )

    return instrumented_code, metadata_json


def construct_import_from_node(
    start_path: Path, import_target_path: Path, name_to_import: str
):
    print(start_path)
    print(import_target_path)
    start_path = start_path.parent
    relative_path = relpath(import_target_path, start_path)
    relative_path_parts = relative_path.parts

    parent_dir_count = sum(1 for part in relative_path_parts if part == "..")

    level = parent_dir_count + 1
    module_name = ".".join(relative_path_parts[parent_dir_count:]).rsplit(".py", 1)[0]

    return ast.ImportFrom(
        module=module_name,
        names=[ast.alias(name=name_to_import, asname=None)],
        level=level,
    )


def relpath(path_to: Path, path_from: Path):
    path_to = Path(path_to).resolve()
    path_from = Path(path_from).resolve()

    try:
        for p in (*reversed(path_from.parents), path_from):
            head, tail = p, path_to.relative_to(p)
    except ValueError:  # Stop when the paths diverge.
        pass
    return Path("../" * (len(path_from.parents) - len(head.parents))).joinpath(tail)
