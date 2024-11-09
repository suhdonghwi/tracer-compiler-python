import ast

from .ast_transformer import (
    InstrumentationTransformer,
    InstrumentTargetNode,
    NodeLocation,
)
from .module_import_code import make_runtime_module_import_code
from .offset_calculator import OffsetCalculator


def instrument_code(
    source_code: str,
    file_id: str,
):
    raw_ast = ast.parse(source_code)
    node_location_getter = make_node_location_getter(source_code, file_id)

    instrumented_ast = InstrumentationTransformer(
        raw_ast,
        node_location_getter,
    ).transform()

    runtime_module_import_code = make_runtime_module_import_code()

    instrumented_code = (
        runtime_module_import_code + "\n" + ast.unparse(instrumented_ast)
    )

    return instrumented_code


def make_node_location_getter(source_code: str, file_id: str):
    offset_calculator = OffsetCalculator(source_code)

    def get_node_location(node: InstrumentTargetNode) -> NodeLocation:
        if isinstance(node, ast.Module):
            return (
                file_id,
                0,
                len(source_code),
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
                begin_offset,
                end_offset,
            )

    return get_node_location
