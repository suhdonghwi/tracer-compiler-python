import sys
import ast
import os
from typing import List

from source_file import SourceFile
from transformer import InstrumentationTransformer
from id_mapped_source_file import IdMappedSourceFile


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
    id_mapped_source_files = [
        IdMappedSourceFile(source_file) for source_file in source_files
    ]

    for id_mapped_source_file in id_mapped_source_files:
        print(
            ast.unparse(InstrumentationTransformer(id_mapped_source_file).transform())
        )

    # original_ast = ast.parse(input_content)
    #
    # instrumented_ast = InstrumentationTransformer(original_ast).transform()
    #
    # print("=== Original AST ===")
    # print(ast.unparse(original_ast))
    #
    # print("=== Instrumented AST ===")
    # print(ast.unparse(instrumented_ast))
