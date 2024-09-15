import ast
from linearized_ast import LinearizedAST


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self, ast: ast.AST):
        self.target_ast = ast
        self.linearized_ast = LinearizedAST(ast)

    def transform(self):
        return self.visit(self.target_ast)

    def visit(self, node: ast.AST) -> ast.AST:
        if isinstance(node, ast.Module):
            node_index = self.linearized_ast.index_of(node)

            return ast.Try(
                body=[ast.Expr(value=ast.Constant(value=node_index))] + node.body,
                handlers=[],
                orelse=[],
                finalbody=[ast.Expr(value=ast.Constant(value=node_index))],
            )

        return super().visit(node)
