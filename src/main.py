import sys
import ast

from transformer import InstrumentationTransformer


if __name__ == "__main__":
    input_file = open(sys.argv[1], "r")
    input_content = input_file.read()

    original_ast = ast.parse(input_content)

    instrumented_ast = InstrumentationTransformer().visit(original_ast)

    print("=== Original AST ===")
    print(ast.unparse(original_ast))

    print("=== Instrumented AST ===")
    print(ast.unparse(instrumented_ast))

