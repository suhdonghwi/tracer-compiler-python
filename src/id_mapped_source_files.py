from typing import List, Tuple
import ast

from source_file import SourceFile

FileId = int
NodeId = int


class IdMappedSourceFiles:
    file_id_to_file: dict[FileId, SourceFile] = {}

    node_id_to_node: dict[NodeId, Tuple[FileId, ast.AST]] = {}
    node_to_node_id: dict[ast.AST, NodeId] = {}

    def __init__(self, source_files: List[SourceFile]):
        self._map_files(source_files)
        self._map_nodes()

    def _map_files(self, source_files: List[SourceFile]):
        for index, source_file in enumerate(source_files):
            file_id = index
            self.file_id_to_file[file_id] = source_file

    def _map_nodes(self):
        current_node_id = 0

        for file_id, source_file in self.file_id_to_file.items():
            for node in ast.walk(source_file.ast):
                self.node_id_to_node[current_node_id] = (file_id, node)
                self.node_to_node_id[node] = current_node_id
                current_node_id += 1

    def get_node_id(self, node: ast.AST) -> NodeId:
        node_id = self.node_to_node_id.get(node)

        if node_id is None:
            raise ValueError("Node not found in mapped source files")

        return node_id
