import os

from aiohttp import ClientSession
from os import walk
from time import sleep
from nbformat import write

from sqlalchemy import false

from src.model.files.metadata import FileMetadata
from src.protocol.read_protocol import read_protocol
from src.protocol.update_protocol import update_protocol


current_files = []
for (dirpath, dirnames, filenames) in walk("../files"):
    print(dirpath)
    for filename in filenames:
        current_files.append(os.path.join(dirpath, filename))

changes = {}
for f in current_files:
    changes[f] = os.path.getmtime(f)

async def start_sync_protocol(session: ClientSession):
    while True:
        await start_read_sync_protocol(session)

        for f in current_files:
            last_timestamp = changes.get(f)
            if last_timestamp < os.path.getmtime(f):
                print("File {} has been modified".format(f))
                await start_write_sync_protocol(session, f, last_timestamp)
                
                changes[f] = os.path.getmtime(f)
            else:
                print("No changes, going to sleep.")
                    
        sleep(10)

async def start_read_sync_protocol(session: ClientSession):
    """
    Steps:
    1) Read
    2) Update
    """

    files_meta = generate_list_of_files(current_files)
    changed_files = await read_protocol(session, files_meta)
    _ = await update_protocol(session, changed_files, False)

    

async def start_write_sync_protocol(session: ClientSession):
    """
    Steps:
    1) Read
    2) Try update
        a) Check if file has been modified
        b) Solve conflicts
    3) Commit
    """

    files_meta = generate_list_of_files(current_files)
    changed_files = await read_protocol(session, files_meta)
    _ = await update_protocol(session, changed_files, True)

    waiting = True
    while waiting:
        still_waiting = False
        for (dirpath, _, filenames) in walk("../files"):
            for filename in filenames:
                if "conflict" in filename:
                    still_waiting = True
                    break
                    
        waiting = still_waiting
                    
        sleep(10)
    
    
def generate_list_of_files(files: list[str])-> list[FileMetadata]:
    return [get_file_metadata(f, open(f, "r").read()) for f in files]

def get_file_metadata(file_name: str, content: str) -> FileMetadata:
    FileMetadata(file_name, content)