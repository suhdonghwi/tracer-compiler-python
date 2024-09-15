import ast
from typing import Union


class LinearizedAST:
    linearized_ast: list[ast.AST] = []
    node_to_index_dict: dict[ast.AST, int] = {}

    def __init__(self, tree: ast.AST):
        for node in ast.walk(tree):
            self.node_to_index_dict[node] = len(self.linearized_ast)
            self.linearized_ast.append(node)

    def node_of(self, index: int) -> Union[ast.AST, None]:
        return self.linearized_ast[index]

    def index_of(self, node: ast.AST) -> Union[int, None]:
        return self.node_to_index_dict.get(node)
