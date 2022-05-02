from aiohttp import ClientSession
from os import environ

from src.metadata.merkle_tree import MerkleTree
from src.model.communication.response_sync import ResponseData
from src.model.files.metadata import FileMetadata
from src.utils.compare_merkle_trees import compare_tree
from src.utils.deserialize_merkle_tree import deserialize_merkle_tree
from src.utils.serialize_merkle_tree import serialize_merkle_tree


async def read_protocol(
            session: ClientSession, files_meta: list[FileMetadata]) -> list[str]:
    diretories_meta = await _get_diretories_metadata(session)
    external_m_tree = deserialize_merkle_tree(diretories_meta.root, diretories_meta.tree)

    m_tree = _generate_current_merkle_tree(files_meta)
    exchange_tree = serialize_merkle_tree(m_tree)
    print(exchange_tree)

    return compare_tree(external_m_tree, m_tree)

async def _get_diretories_metadata(session: ClientSession) -> ResponseData:
    response_data: ResponseData = None

    async with session.get(environ["URL_SYNC"]) as response:
        response_data = await response.json()

    return response_data

def generate_response_data(files_meta: list[FileMetadata]) -> ResponseData:
    m_tree = _generate_current_merkle_tree(files_meta)
    root, serialized_m_tree = serialize_merkle_tree(m_tree)
    return ResponseData(root, serialized_m_tree)

def _generate_current_merkle_tree(files_meta: list[FileMetadata]) -> MerkleTree:
    m_tree = MerkleTree(files_meta)
    return m_tree