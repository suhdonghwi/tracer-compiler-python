import ast

from id_mapped_source_file import NodeId


def make_id_node(node_id: NodeId) -> ast.Constant:
    return ast.Constant(value=str(node_id))


def make_marking_call(method_name: str, *args: ast.AST) -> ast.Call:
    return ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="__tracer__", ctx=ast.Load()),
            attr=method_name,
            ctx=ast.Load(),
        ),
        args=list(args),
        keywords=[],
    )


def wrap_with_frame_begin_end(body: list[ast.stmt], parent_node_id: NodeId) -> ast.Try:
    id_node = make_id_node(parent_node_id)

    return ast.Try(
        body=[ast.Expr(make_marking_call("begin_frame", id_node))] + body,
        handlers=[],
        orelse=[],
        finalbody=[ast.Expr(make_marking_call("end_frame", id_node))],
    )


def wrap_with_expr_begin_end(node: ast.expr, node_id: NodeId) -> ast.Call:
    begin_call = make_marking_call("begin_expr", make_id_node(node_id))
    end_call = make_marking_call("end_expr", begin_call, node)
    return end_call


NON_INVOCATING_EXPR_TYPES = (
    ast.Lambda,
    ast.IfExp,
    ast.Dict,
    ast.Set,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
    ast.Await,
    ast.Yield,
    ast.YieldFrom,
    ast.FormattedValue,
    ast.JoinedStr,
    ast.Constant,
    ast.Starred,
    ast.Name,
    ast.List,
    ast.Tuple,
)


def is_invocating_expr(node: ast.expr) -> bool:
    return not isinstance(node, NON_INVOCATING_EXPR_TYPES)
