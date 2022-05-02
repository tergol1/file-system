from hashlib import sha256

from src.model.files.metadata import FileMetadata
from src.model.tree.node import BinaryTreeNode, CreateNode
from src.utils.biggest_pow_2 import biggest_power_of2


default_value = "-"
default_hash_value = sha256(default_value.encode('utf-8')).hexdigest()

class MerkleTree:
    def __init__(self, data: list[FileMetadata]):
        self.leaves = data[:]
        self._start_correct_size()

        self.tree: list[BinaryTreeNode] = []
        self._build_tree()

    def _start_correct_size(self):
        bigg_pow_o2 = biggest_power_of2(len(self.leaves))
        if len(self.leaves) == bigg_pow_o2:
            return

        bigg_pow_o2 *= 2
        
        for _ in range(bigg_pow_o2 - len(self.leaves)):
            self.leaves.append(BinaryTreeNode(default_value, default_hash_value))

    def _build_tree(self):
        nodes = [CreateNode(e) for e in self.leaves]
        self.root = self._build_tree_recursive(nodes)

    def _build_tree_recursive(
            self, nodes: list[BinaryTreeNode])-> BinaryTreeNode:
        half: int = len(nodes) // 2
    
        if len(nodes) == 2:
            return BinaryTreeNode(
                nodes[0].value + "+" + nodes[1].value,
                sha256((nodes[0].hash_value + nodes[1].hash_value).encode('utf-8')).hexdigest(),
                nodes[0],
                nodes[1]
            )

        left: BinaryTreeNode = self._build_tree_recursive(nodes[:half])
        right: BinaryTreeNode = self._build_tree_recursive(nodes[half:])

        hash_value: str = sha256((left.hash_value + right.hash_value).encode('utf-8')).hexdigest()
        value: str = left.value + "+" + right.value
        return BinaryTreeNode(
                    value,
                    hash_value,
                    left, 
                    right
                )

    def get_root(self):
        return self.root