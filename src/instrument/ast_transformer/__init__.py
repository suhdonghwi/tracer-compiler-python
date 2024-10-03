import ast
from typing import Callable, overload

from .ast_utils import (
    is_invoking_expr,
    is_invoking_stmt,
    wrap_expr,
    wrap_statements,
)


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(
        self,
        target_ast: ast.Module,
        node_id_getter: Callable[[ast.AST], str],
    ):
        self.target_ast = target_ast
        self.node_id_getter = node_id_getter

    def transform(self) -> ast.Module:
        return ast.fix_missing_locations(self.visit(self.target_ast))

    @overload
    def visit(self, node: ast.expr) -> ast.expr: ...

    @overload
    def visit(self, node: ast.stmt) -> ast.stmt: ...

    @overload
    def visit(self, node: ast.Module) -> ast.Module: ...

    @overload
    def visit(self, node: ast.AST) -> ast.AST: ...

    def visit(self, node: ast.AST) -> ast.AST:
        node_id = self.node_id_getter(node)
        node_id_node = ast.Constant(value=node_id)

        if isinstance(node, ast.FunctionDef):
            transformed_body = list(map(self.visit, node.body))
            node.body = [
                wrap_statements(
                    transformed_body,
                    "begin_func",
                    "end_func",
                    node_id_node,
                )
            ]

            return node

        elif isinstance(node, ast.ClassDef):
            node.body = list(map(self.visit, node.body))
            return node

        elif isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load):
            return node

        elif isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            if node.value is not None:  # type: ignore
                node.value = self.visit(node.value)

            return wrap_statements([node], "begin_stmt", "end_stmt", node_id_node)

        self.generic_visit(node)

        if isinstance(node, ast.Slice):
            return node

        if isinstance(node, ast.Module):
            node.body = [
                wrap_statements(node.body, "begin_module", "end_module", node_id_node)
            ]
            return node

        elif isinstance(node, ast.stmt) and is_invoking_stmt(node):
            return wrap_statements([node], "begin_stmt", "end_stmt", node_id_node)

        elif isinstance(node, ast.expr) and is_invoking_expr(node):
            return wrap_expr(node, "begin_expr", "end_expr", node_id_node)

        return node
