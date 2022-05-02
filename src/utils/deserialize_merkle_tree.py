from src.metadata.merkle_tree import MerkleTree
from src.model.communication.node_exchange import NodeExchange
from src.model.files.metadata import FileMetadata
from src.model.tree.node import BinaryTreeNode


def deserialize_merkle_tree(root: NodeExchange, exchange_tree: list[NodeExchange]) -> MerkleTree:
    dict_nodes = create_dict_of_nodes(exchange_tree)
    list_of_files = get_files_recursive(root, dict_nodes)

    return MerkleTree(list_of_files)

def create_dict_of_nodes(exchange_tree: list[NodeExchange]) -> dict[NodeExchange]:
    dict_nodes = {}
    for node in exchange_tree:
        dict_nodes[node.hash_value] = node
    return dict_nodes

def get_files_recursive(node: NodeExchange, dict_nodes: dict[NodeExchange]) -> list[FileMetadata]:
    if node.left == "":
        return [FileMetadata(node.value, "")]

    list_of_files = []

    list_of_files.extend(get_files_recursive(dict_nodes[node.left], dict_nodes))
    list_of_files.extend(get_files_recursive(dict_nodes[node.right], dict_nodes))

    return list_of_files