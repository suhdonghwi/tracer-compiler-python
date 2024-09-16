import ast
from linearized_ast import LinearizedAST


def make_marking_call(method_name: str, index: int, *args: ast.AST) -> ast.Call:
    return ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="__tracer__", ctx=ast.Load()),
            attr=method_name,
            ctx=ast.Load(),
        ),
        args=[ast.Constant(value=index)] + list(args),
        keywords=[],
    )


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self, ast: ast.AST):
        self.target_ast = ast
        self.linearized_ast = LinearizedAST(ast)

    def transform(self):
        return self.visit(self.target_ast)

    def visit(self, node: ast.AST) -> ast.AST:
        if isinstance(node, ast.Module):
            node_index = self.linearized_ast.index_of(node)

            body = [
                ast.Expr(make_marking_call("begin_frame", node_index))
            ] + node.body

            final_body = [ast.Expr(make_marking_call("end_frame", node_index))]

            return ast.Try(
                body=body,
                handlers=[],
                orelse=[],
                finalbody=final_body,
            )

        return super().visit(node)
