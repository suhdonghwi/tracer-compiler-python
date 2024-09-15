import ast
from typing import TypeVar


class InstrumentationTransformer(ast.NodeTransformer):
    def visit_Module(self, node: ast.Module):
        return ast.Try(
            body=node.body,
            handlers=[],
            orelse=[],
            finalbody=[ast.Expr(value=ast.Constant(value=42))],
        )

    Node = TypeVar("Node", bound=ast.AST)

    def visit(self, node: Node) -> Node:
        return node
