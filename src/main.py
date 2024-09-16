import sys
import ast
import os
from typing import List

from source_file import SourceFile
from transformer import InstrumentationTransformer


def load_all_source_files(directory_path: str) -> List[SourceFile]:
    source_files: List[SourceFile] = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                source_files.append(SourceFile(os.path.join(root, file)))

    return source_files


if __name__ == "__main__":
    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        source_files = load_all_source_files(input_path)
    else:
        source_files = [SourceFile(input_path)]

    print(source_files)

    # original_ast = ast.parse(input_content)
    #
    # instrumented_ast = InstrumentationTransformer(original_ast).transform()
    #
    # print("=== Original AST ===")
    # print(ast.unparse(original_ast))
    #
    # print("=== Instrumented AST ===")
    # print(ast.unparse(instrumented_ast))
