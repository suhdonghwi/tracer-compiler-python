import sys
import ast
import os
from typing import List
from id_mapped_source_files import IdMappedSourceFiles

from source_file import SourceFile
from transformer import InstrumentationTransformer


def load_all_source_files(directory_path: str) -> List[SourceFile]:
    source_files: List[SourceFile] = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                source_files.append(SourceFile.from_file(path))

    return source_files


if __name__ == "__main__":
    input_path = sys.argv[1]
    source_files = []

    if os.path.isdir(input_path):
        source_files = load_all_source_files(input_path)
    elif os.path.isfile(input_path):
        source_files = [SourceFile.from_file(input_path)]

    if len(source_files) == 0:
        print("Error: No source files found")
        sys.exit(1)

    print(len(source_files), "source files found")
    id_mapped_source_files = IdMappedSourceFiles(source_files)

    for source_file in source_files:
        node_id_getter = id_mapped_source_files.get_node_id
        instrumented_ast = InstrumentationTransformer(
            source_file.ast, node_id_getter
        ).transform()

        # print("Printing instrumented AST for file: ", source_file.path)
        # print(ast.unparse(instrumented_ast))
        # print("======================\n\n")
    # original_ast = ast.parse(input_content)
    #
    # instrumented_ast = InstrumentationTransformer(original_ast).transform()
    #
    # print("=== Original AST ===")
    # print(ast.unparse(original_ast))
    #
    # print("=== Instrumented AST ===")
    # print(ast.unparse(instrumented_ast))
