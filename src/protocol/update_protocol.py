


from aiohttp import ClientSession
from os import environ

from src.model.communication.response_sync import ChangedFileResponseData
from src.model.files.metadata import FileMetadata


async def update_protocol(
            session: ClientSession, files_path: list[str], conflicts: bool = False) -> list[FileMetadata]:
    new_files = []
    for path in files_path:
        new_file = await _read_new_file(session, path)

        if conflicts:
            name, extension = path.split(".")
            conflict_path = name + "_conflict." + extension
            
            with open(conflict_path, "w") as myfile:
                myfile.write(new_file.data.content)    
            
            continue

        with open(path, "w") as myfile:
            myfile.write(new_file.data.content)

        new_files.append(new_file.data)

    return new_files
    

async def _read_new_file(session: ClientSession, file_name: str) -> ChangedFileResponseData:
    response_data: ChangedFileResponseData = None

    async with session.post(
            url=f'{environ.get("URL_FILE")}/{file_name}'
        ) as response:
        response_data = await response.json()

    return response_data