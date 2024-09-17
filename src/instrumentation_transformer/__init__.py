import ast

from id_mapped_source_file import IdMappedSourceFile
from instrumentation_transformer.ast_utils import (
    make_id_node,
    make_marking_call,
    wrap_with_frame_begin_end,
    wrap_with_expr_begin_end,
    is_invocating_expr,
)


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self, id_mapped_source_file: IdMappedSourceFile):
        self.id_mapped_source_file = id_mapped_source_file

    def transform(self):
        return ast.fix_missing_locations(self.visit(self.id_mapped_source_file.ast))

    def visit(self, node: ast.AST) -> ast.AST:
        self.generic_visit(node)
        node_id = self.id_mapped_source_file.get_node_id(node)

        if isinstance(node, ast.Module):
            wrapped_body = wrap_with_frame_begin_end(node.body, node_id)

            node = ast.Module(body=[wrapped_body], type_ignores=[])

        if isinstance(node, ast.FunctionDef):
            wrapped_body = wrap_with_frame_begin_end(node.body, node_id)

            node = ast.FunctionDef(
                name=node.name,
                args=node.args,
                body=[wrapped_body],
                decorator_list=node.decorator_list,
                returns=node.returns,
                type_params=[],
            )

        if isinstance(node, ast.stmt):
            id_node = make_id_node(node_id)

            node = ast.Try(
                body=[
                    ast.Expr(make_marking_call("begin_stmt", id_node)),
                    node,
                ],
                handlers=[],
                orelse=[],
                finalbody=[ast.Expr(make_marking_call("end_stmt", id_node))],
            )

        if isinstance(node, ast.expr) and is_invocating_expr(node):
            node = wrap_with_expr_begin_end(node, node_id)

        return node
