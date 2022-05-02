from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from src.model.files.metadata import FileMetadata


@dataclass
class BinaryTreeNode:
    value: str
    hash_value: str
    left: Optional[BinaryTreeNode] = None
    right: Optional[BinaryTreeNode] = None

def CreateNode(value: FileMetadata) -> BinaryTreeNode:
    return BinaryTreeNode(
            value, 
            sha256(value.content.encode('utf-8')).hexdigest())