import ast
import os
import sys

from id_mapped_source_file import IdMappedSourceFile
from instrumentation_transformer import InstrumentationTransformer
from source_file import SourceFile


def get_py_files_inside_directory(directory_path: str) -> list[str]:
    paths: list[str] = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                paths.append(path)

    return paths


if __name__ == "__main__":
    input_path = sys.argv[1]
    source_file_paths = []

    if os.path.isdir(input_path):
        source_file_paths = get_py_files_inside_directory(input_path)
    elif os.path.isfile(input_path):
        source_file_paths = [input_path]

    source_files = [
        SourceFile.from_path(source_file_path)
        for source_file_path in source_file_paths
    ]

    if len(source_files) == 0:
        print("no source files found")
        sys.exit(1)

    print(len(source_files), "source files found")
    id_mapped_source_files = [
        IdMappedSourceFile(source_file) for source_file in source_files
    ]

    for id_mapped_source_file in id_mapped_source_files:
        transformed_ast = InstrumentationTransformer(id_mapped_source_file).transform()
        print(id_mapped_source_file.dumps())
        # print(ast.unparse(transformed_ast))

