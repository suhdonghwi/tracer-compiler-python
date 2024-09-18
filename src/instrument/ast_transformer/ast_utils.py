import ast


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


def wrap_with_stmt_begin_end(node: ast.stmt, *args: ast.AST) -> ast.Try:
    return ast.Try(
        body=[ast.Expr(make_marking_call("begin_stmt", *args)), node],
        handlers=[],
        orelse=[],
        finalbody=[ast.Expr(make_marking_call("end_stmt", *args))],
    )


def wrap_with_expr_begin_end(node: ast.expr, arg: ast.AST) -> ast.Call:
    begin_call = make_marking_call("begin_expr", arg)
    end_call = make_marking_call("end_expr", begin_call, node)
    return end_call


# Invoking expression types are expression types that, when evaluated, may result in a function call,
# even if all their subexpressions are `ast.Constant`.

# We maintain a list of non-invoking expression types, rather than invoking expression types,
# because future Python versions may add new types of AST nodes.
# It is safer to assume that new nodes are invoking expressions, because otherwise we may miss some nodes that should be wrapped.
NON_INVOKING_EXPR_TYPES = (
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


def is_invoking_expr(node: ast.expr) -> bool:
    return not isinstance(node, NON_INVOKING_EXPR_TYPES)


# Invoking statement types are statement types that, when executed, may result in either of the following:
# - Breaking out of the current frame or loop
# - Importing a module
# - Executing a function
# - Raising an exception
# even if all their substatements are `ast.Pass` and all their subexpressions are `ast.Constant`.

# We maintain a list of non-invoking statement types, rather than invoking statement types,
# for the same reason as for invoking expressions.
NON_INVOKING_STMT_TYPES = (
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.If,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.Global,
    ast.Nonlocal,
    ast.Pass,
    # ast.Match,
    # ast.TypeAlias,
    # ast.TryStar,
)


def is_invoking_stmt(node: ast.stmt) -> bool:
    return not isinstance(node, NON_INVOKING_STMT_TYPES)
