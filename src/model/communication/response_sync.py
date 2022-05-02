from dataclasses import dataclass

from src.model.communication.node_exchange import NodeExchange
from src.model.files.metadata import FileMetadata


@dataclass
class ResponseData:
    root: NodeExchange
    tree: list[NodeExchange]

@dataclass
class ChangedFileResponseData:
    data: FileMetadata