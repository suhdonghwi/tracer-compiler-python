import ast

from id_mapped_source_file import IdMappedSourceFile
from instrumentation_transformer.ast_utils import (
    is_invoking_expr,
    make_marking_call,
    make_uuid_node,
    wrap_with_expr_begin_end,
    wrap_with_frame_begin_end,
)


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self, id_mapped_source_file: IdMappedSourceFile):
        self.id_mapped_source_file = id_mapped_source_file

    def transform(self):
        return ast.fix_missing_locations(self.visit(self.id_mapped_source_file.ast))

    def visit(self, node: ast.AST) -> ast.AST:
        node_id = self.id_mapped_source_file.get_node_id(node)
        node_id_node = make_uuid_node(node_id)

        if isinstance(node, ast.Module):
            self.generic_visit(node)
            wrapped_body = wrap_with_frame_begin_end(node.body, node_id_node)

            return ast.Module(body=[wrapped_body], type_ignores=[])

        elif isinstance(node, ast.FunctionDef):
            map(self.generic_visit, node.body)
            wrapped_body = wrap_with_frame_begin_end(node.body, node_id_node)

            return ast.FunctionDef(
                name=node.name,
                args=node.args,
                body=[wrapped_body],
                decorator_list=node.decorator_list,
                returns=node.returns,
                type_params=node.type_params if hasattr(node, "type_params") else [],  # type: ignore
            )

        elif isinstance(node, ast.stmt):
            self.generic_visit(node)
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
            self.generic_visit(node)
            return wrap_with_expr_begin_end(node, node_id_node)

        self.generic_visit(node)
        return node
