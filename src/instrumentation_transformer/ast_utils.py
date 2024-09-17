import ast
from uuid import UUID


def make_uuid_node(uuid: UUID) -> ast.Constant:
    return ast.Constant(value=str(uuid))


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


def wrap_with_frame_begin_end(body: list[ast.stmt], *args: ast.AST) -> ast.Try:
    return ast.Try(
        body=[ast.Expr(make_marking_call("begin_frame", *args))] + body,
        handlers=[],
        orelse=[],
        finalbody=[ast.Expr(make_marking_call("end_frame", *args))],
    )


def wrap_with_expr_begin_end(node: ast.expr, arg: ast.AST) -> ast.Call:
    begin_call = make_marking_call("begin_expr", arg)
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