import ast
from pathlib import Path
from uuid import uuid1

from .ast_transformer import (
    InstrumentationTransformer,
    InstrumentTargetNode,
    NodeLocation,
)
from .module_import_code import make_relative_import_code
from .offset_calculator import OffsetCalculator
from .tracer_metadata import make_tracer_metadata_json


def instrument_code(
    source_code: str,
    source_path: Path,
    destination_path: Path,
    tracer_module_path: Path,
):
    file_id = str(uuid1())

    raw_ast = ast.parse(source_code)
    node_location_getter = make_node_location_getter(source_code, file_id)

    instrumented_ast = InstrumentationTransformer(
        raw_ast,
        node_location_getter,
    ).transform()

    tracer_module_import_code = make_relative_import_code(
        importer_path=destination_path, import_target_path=tracer_module_path
    )

    instrumented_code = tracer_module_import_code + "\n" + ast.unparse(instrumented_ast)
    metadata_json = make_tracer_metadata_json(
        file_id=file_id, original_code=source_code, path=source_path
    )

    return instrumented_code, metadata_json


def make_node_location_getter(source_code: str, file_id: str):
    offset_calculator = OffsetCalculator(source_code)

    def get_node_location(node: InstrumentTargetNode) -> NodeLocation:
        if isinstance(node, ast.Module):
            return (
                file_id,
                (
                    0,
                    len(source_code),
                ),
            )
        else:
            if node.end_lineno is None or node.end_col_offset is None:
                raise ValueError(
                    "Node is missing end line or end column offset information"
                )

            begin_offset, end_offset = offset_calculator.get_offsets(
                node.lineno, node.col_offset, node.end_lineno, node.end_col_offset
            )

            return (
                file_id,
                (
                    begin_offset,
                    end_offset,
                ),
            )

    return get_node_location
