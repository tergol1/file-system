from src.metadata.merkle_tree import MerkleTree
from src.model.tree.node import BinaryTreeNode


def compare_tree(tree1: MerkleTree, tree2: MerkleTree)-> list[str]:
    if tree1.root.hash_value == tree2.root.hash_value:
        return []
    
    return compare_diff_nodes_recursive(tree1.root, tree2.root)

def compare_diff_nodes_recursive(root1: BinaryTreeNode, root2: BinaryTreeNode) -> list[str]:
    list_of_files: list[str] = []

    if root1.left is None and root2.left is None:
        return [root1.value]
    
    if root1.left.hash_value != root2.left.hash_value:
        list_of_files.append(compare_diff_nodes_recursive(root1.left, root2.left))

    if root1.right.hash_value != root2.right.hash_value:
        list_of_files.append(compare_diff_nodes_recursive(root1.right, root2.right))