"""
just a way to make the communication between two machines
"""
import os

from http.server import BaseHTTPRequestHandler
from os import walk
from src.model.communication.response_sync import ResponseData

from src.protocol.read_protocol import _generate_current_merkle_tree
from src.protocol.sync_protocol import generate_list_of_files
from src.utils.serialize_merkle_tree import serialize_merkle_tree

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        current_files = []
        for (dirpath, _, filenames) in walk("../files"):
            for filename in filenames:
                current_files.append(os.path.join(dirpath, filename))

        files_meta = generate_list_of_files(current_files)
        m_tree = _generate_current_merkle_tree(files_meta)
        root, exchange_tree = serialize_merkle_tree(m_tree)
        data = ResponseData(root, exchange_tree)
        
        self.wfile.write(bytes(data, "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        path_arr = self.path.split("/")
        file_path = path_arr[-1]

        desired_file = ""
        for (dirpath, _, filenames) in walk("../files"):
            for filename in filenames:
                if file_path in filename:
                    text_file = open(os.path.join(dirpath, filename), "r")
                    desired_file = text_file.read()
        
        self.wfile.write(bytes(desired_file, "utf-8"))