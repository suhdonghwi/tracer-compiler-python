import ast

from id_mapped_source_file import IdMappedSourceFile, NodeId


def make_marking_call(method_name: str, node_id: NodeId, *args: ast.AST) -> ast.Call:
    return ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="__tracer__", ctx=ast.Load()),
            attr=method_name,
            ctx=ast.Load(),
        ),
        args=[ast.Constant(value=str(node_id))] + list(args),
        keywords=[],
    )


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self, id_mapped_source_file: IdMappedSourceFile):
        self.id_mapped_source_file = id_mapped_source_file

    def transform(self):
        return self.visit(self.id_mapped_source_file.ast)

    def visit(self, node: ast.AST) -> ast.AST:
        if isinstance(node, ast.Module):
            node_id = self.id_mapped_source_file.get_node_id(node)

            body = [ast.Expr(make_marking_call("begin_frame", node_id))] + node.body
            final_body = [ast.Expr(make_marking_call("end_frame", node_id))]

            return ast.Try(
                body=body,
                handlers=[],
                orelse=[],
                finalbody=final_body,
            )

        return super().visit(node)
