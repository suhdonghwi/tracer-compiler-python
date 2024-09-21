import ast
from pathlib import Path

from .ast_transformer import InstrumentationTransformer
from .module_import_code import make_relative_import_code
from .node_id_mapping import NodeIdMapping
from .tracer_metadata import make_tracer_metadata_json


def instrument_code(
    source_code: str,
    source_path: Path,
    destination_path: Path,
    tracer_module_path: Path,
):
    raw_ast = ast.parse(source_code)
    node_id_mapping = NodeIdMapping(raw_ast)

    instrumented_ast = InstrumentationTransformer(
        raw_ast,
        lambda node: str(node_id_mapping.get_node_id(node)),
    ).transform()

    tracer_module_import_code = make_relative_import_code(
        importer_path=destination_path, import_target_path=tracer_module_path
    )

    instrumented_code = tracer_module_import_code + "\n" + ast.unparse(instrumented_ast)
    metadata_json = make_tracer_metadata_json(source_code, source_path, node_id_mapping)

    return instrumented_code, metadata_json
