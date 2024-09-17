import ast
from uuid import UUID, uuid1

NodeId = UUID


class NodeIdMappedAST:
    node_id_to_node: dict[NodeId, ast.AST] = {}
    node_to_node_id: dict[ast.AST, NodeId] = {}

    def __init__(self, input_ast: ast.AST):
        self.raw_ast = input_ast

        for node in ast.walk(self.raw_ast):
            node_id = uuid1()
            self.node_id_to_node[node_id] = node
            self.node_to_node_id[node] = node_id

    def get_node_id(self, node: ast.AST) -> NodeId:
        node_id = self.node_to_node_id.get(node)

        if node_id is None:
            raise ValueError("Node not found in mapped source files")

        return node_id

    def items(self):
        return self.node_id_to_node.items()

    # def dumps(self):
    #     node_id_to_range: dict[NodeId, Tuple[int, int]] = {}
    #
    #     for node_id, node in self.node_id_to_node.items():
    #         if isinstance(node, ast.Module):
    #             node_id_to_range[node_id] = (
    #                 0,
    #                 len(self.original_source_file.content),
    #             )
    #
    #         if isinstance(node, (ast.stmt, ast.expr)):
    #             if node.end_col_offset is None:
    #                 raise ValueError("Node has no end_col_offset")
    #
    #             node_id_to_range[node_id] = (node.col_offset, node.end_col_offset)
    #
    #     node_id_to_range_json_dict = {
    #         str(node_id): (start, end)
    #         for node_id, (start, end) in node_id_to_range.items()
    #     }
    #
    #     data = {
    #         "path": self.original_source_file.path,
    #         "content": self.original_source_file.content,
    #         "node_id_to_range": node_id_to_range_json_dict,
    #     }
    #
    #     return json.dumps(data, indent=2)
