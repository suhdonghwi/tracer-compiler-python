import ast
from typing import Callable

from .ast_transformer import (
    InstrumentationTransformer,
    InstrumentTargetNode,
    SourceLocation,
)
from .initialization_code import make_initialization_code
from .offset_calculator import OffsetCalculator


def instrument_code(
    source_code: str,
    file_id: str,
) -> str:
    raw_ast = ast.parse(source_code)
    source_location_getter = make_source_location_getter(source_code, file_id)

    instrumented_ast = InstrumentationTransformer(
        raw_ast, source_location_getter
    ).transform()

    runtime_module_import_code = make_initialization_code()

    instrumented_code = (
        runtime_module_import_code + "\n" + ast.unparse(instrumented_ast)
    )

    return instrumented_code


def make_source_location_getter(
    source_code: str,
    source_file_id: str,
) -> Callable[[InstrumentTargetNode], SourceLocation]:
    offset_calculator = OffsetCalculator(source_code)

    def get_source_location(node: InstrumentTargetNode) -> SourceLocation:
        if isinstance(node, ast.Module):
            return (
                source_file_id,
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
                source_file_id,
                begin_offset,
                end_offset,
            )

    return get_source_location
