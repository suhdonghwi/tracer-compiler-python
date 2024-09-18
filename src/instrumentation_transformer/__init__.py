import ast
from typing import overload

from instrumentation_transformer.ast_utils import (
    is_invoking_expr,
    is_invoking_stmt,
    make_uuid_node,
    wrap_with_expr_begin_end,
    wrap_with_frame_begin_end,
    wrap_with_stmt_begin_end,
)
from node_id_mapped_ast import NodeIdMappedAST


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self, node_id_mapped_ast: NodeIdMappedAST):
        self.node_id_mapped_ast = node_id_mapped_ast

    def transform(self):
        return ast.fix_missing_locations(self.visit(self.node_id_mapped_ast.raw_ast))

    @overload
    def visit(self, node: ast.expr) -> ast.expr:
        ...

    @overload
    def visit(self, node: ast.stmt) -> ast.stmt:
        ...

    @overload
    def visit(self, node: ast.Module) -> ast.Module:
        ...

    @overload
    def visit(self, node: ast.AST) -> ast.AST:
        ...

    def visit(self, node: ast.AST) -> ast.AST:
        node_id = self.node_id_mapped_ast.get_node_id(node)
        node_id_node = make_uuid_node(node_id)

        if isinstance(node, ast.FunctionDef):
            node.body = list(map(self.visit, node.body))
            return node

        elif isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load):
            return node

        elif isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            if node.value is not None:  # type: ignore
                node.value = self.visit(node.value)

            return wrap_with_stmt_begin_end(node, node_id_node)

        self.generic_visit(node)

        if isinstance(node, ast.Module):
            node.body = [wrap_with_frame_begin_end(node.body, node_id_node)]
            return node

        elif isinstance(node, ast.stmt) and is_invoking_stmt(node):
            return wrap_with_stmt_begin_end(node, node_id_node)

        elif isinstance(node, ast.expr) and is_invoking_expr(node):
            return wrap_with_expr_begin_end(node, node_id_node)

        return node
