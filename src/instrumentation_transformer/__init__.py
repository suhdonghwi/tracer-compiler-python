import ast
import typing

from instrumentation_transformer.ast_utils import (
    is_invoking_expr,
    is_invoking_stmt,
    make_marking_call,
    make_uuid_node,
    wrap_with_expr_begin_end,
    wrap_with_frame_begin_end,
)
from node_id_mapped_ast import NodeIdMappedAST


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self, node_id_mapped_ast: NodeIdMappedAST):
        self.node_id_mapped_ast = node_id_mapped_ast

    def transform(self):
        return ast.fix_missing_locations(self.visit(self.node_id_mapped_ast.raw_ast))

    def visit(self, node: ast.AST) -> ast.AST:
        node_id = self.node_id_mapped_ast.get_node_id(node)
        node_id_node = make_uuid_node(node_id)

        if isinstance(node, ast.FunctionDef):
            transformed_body = typing.cast(
                list[ast.stmt], list(map(self.visit, node.body))
            )
            wrapped_body = wrap_with_frame_begin_end(transformed_body, node_id_node)

            return ast.FunctionDef(
                name=node.name,
                args=node.args,
                body=[wrapped_body],
                decorator_list=node.decorator_list,
                returns=node.returns,
                type_params=node.type_params if hasattr(node, "type_params") else [],  # type: ignore
            )

        self.generic_visit(node)

        if isinstance(node, ast.Module):
            wrapped_body = wrap_with_frame_begin_end(node.body, node_id_node)

            return ast.Module(body=[wrapped_body], type_ignores=[])

        elif isinstance(node, ast.stmt) and is_invoking_stmt(node):
            return ast.Try(
                body=[
                    ast.Expr(make_marking_call("begin_stmt", node_id_node)),
                    node,
                ],
                handlers=[],
                orelse=[],
                finalbody=[ast.Expr(make_marking_call("end_stmt", node_id_node))],
            )

        elif isinstance(node, ast.expr) and is_invoking_expr(node):
            return wrap_with_expr_begin_end(node, node_id_node)

        return node
