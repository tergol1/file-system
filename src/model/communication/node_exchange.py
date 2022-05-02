from dataclasses import dataclass


@dataclass
class NodeExchange:
    value: str
    hash_value: str
    left: str
    right: str