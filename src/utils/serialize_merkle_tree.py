from src.metadata.merkle_tree import MerkleTree
from src.model.communication.node_exchange import NodeExchange
from src.model.tree.node import BinaryTreeNode


def serialize_merkle_tree(tree: MerkleTree) -> tuple[NodeExchange, list[NodeExchange]]:
    return serialize_binary_tree_node(tree.root), serialize_tree_recursive(tree.root)

def serialize_tree_recursive(root: BinaryTreeNode) -> list[NodeExchange]:
    exchange_data = []
    exchange_data.append(serialize_binary_tree_node(root))

    if root.left is not None:
        exchange_data.extend(serialize_tree_recursive(root.left))
        exchange_data.extend(serialize_tree_recursive(root.right))

    return exchange_data

def serialize_binary_tree_node(node: BinaryTreeNode) -> list[NodeExchange]:
    left_node = ""
    right_node = ""
    if node.left is not None:
        left_node = node.left.hash_value
        right_node = node.right.hash_value

    return NodeExchange(
        node.value,
        node.hash_value,
        left_node,
        right_node
    )
