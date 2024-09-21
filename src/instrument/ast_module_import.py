import ast
from pathlib import Path

from utils.file_processing import relative_walk_up


def make_relative_import_stmts(importer_path: Path, import_target_path: Path):
    # 1. Import os and sys
    import_os_sys = ast.Import(
        names=[ast.alias(name="os", asname=None), ast.alias(name="sys", asname=None)]
    )

    # 2. Calculate relative path for the `sys.path.append` part
    relative_path = relative_walk_up(import_target_path, importer_path.parent)
    relative_path_parts = relative_path.parts

    # Create a list of ".." for joining with os.path
    up_levels = [
        ast.Constant(value="..") for part in relative_path_parts if part == ".."
    ]

    # sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ...))
    sys_path_append = ast.Expr(
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id="sys", ctx=ast.Load()),
                    attr="path",
                    ctx=ast.Load(),
                ),
                attr="append",
                ctx=ast.Load(),
            ),
            args=[
                ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="os", ctx=ast.Load()),
                        attr="path.join",
                        ctx=ast.Load(),
                    ),
                    args=[
                        ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="os", ctx=ast.Load()),
                                attr="path.dirname",
                                ctx=ast.Load(),
                            ),
                            args=[ast.Name(id="__file__", ctx=ast.Load())],
                            keywords=[],
                        ),
                        *up_levels,  # Add the ".." components dynamically
                    ],
                    keywords=[],
                )
            ],
            keywords=[],
        )
    )

    # 3. Import __tracer__
    import_tracer = ast.Import(names=[ast.alias(name="__tracer__", asname=None)])

    # Return a list of statements
    return [import_os_sys, sys_path_append, import_tracer]
