import ast


class LinearizedAST:
    linearized_ast: list[ast.AST] = []
    node_to_index_dict: dict[ast.AST, int] = {}

    def __init__(self, tree: ast.AST):
        for node in ast.walk(tree):
            self.node_to_index_dict[node] = len(self.linearized_ast)
            self.linearized_ast.append(node)

    def node_of(self, index: int) -> ast.AST:
        return self.linearized_ast[index]

    def index_of(self, node: ast.AST) -> int:
        index = self.node_to_index_dict.get(node)

        if index is None:
            raise ValueError("Node not found in linearized AST")

        return index
