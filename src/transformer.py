import ast
from typing import Callable


def make_marking_call(method_name: str, node_id: int, *args: ast.AST) -> ast.Call:
    return ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="__tracer__", ctx=ast.Load()),
            attr=method_name,
            ctx=ast.Load(),
        ),
        args=[ast.Constant(value=node_id)] + list(args),
        keywords=[],
    )


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self, ast: ast.AST, node_id_getter: Callable[[ast.AST], int]):
        self.target_ast = ast
        self.node_id_getter = node_id_getter

    def transform(self):
        return self.visit(self.target_ast)

    def visit(self, node: ast.AST) -> ast.AST:
        if isinstance(node, ast.Module):
            node_id = self.node_id_getter(node)

            body = [ast.Expr(make_marking_call("begin_frame", node_id))] + node.body
            final_body = [ast.Expr(make_marking_call("end_frame", node_id))]

            return ast.Try(
                body=body,
                handlers=[],
                orelse=[],
                finalbody=final_body,
            )

        return super().visit(node)
