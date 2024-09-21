import ast
from pathlib import Path

from .ast_module_import import make_relative_import_stmts
from .ast_transformer import InstrumentationTransformer
from .node_id_mapping import NodeIdMapping
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

    instrumented_ast.body = (
        make_relative_import_stmts(
            importer_path=destination_path, import_target_path=tracer_module_path
        )
        + instrumented_ast.body
    )

    instrumented_code = ast.unparse(instrumented_ast)
    metadata_json = make_tracer_metadata_json(code, source_path, node_id_mapping)

    return instrumented_code, metadata_json
