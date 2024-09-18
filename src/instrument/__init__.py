import ast

from source_file import SourceFile

from .node_id_mapped_ast import NodeIdMappedAST
from .ast_transformer import InstrumentationTransformer
from .location_map import make_location_map


def instrument_source_file(source_file: SourceFile):
    raw_ast = ast.parse(source_file.content)
    node_id_mapped_ast = NodeIdMappedAST(raw_ast)

    instrumented_ast = InstrumentationTransformer(
        raw_ast, lambda node: str(node_id_mapped_ast.get_node_id(node))
    ).transform()
    instrumented_code = ast.unparse(instrumented_ast)

    location_map = make_location_map(source_file, node_id_mapped_ast)

    return instrumented_code, location_map
