from aiohttp import ClientSession
from http.server import HTTPServer
from threading import Thread

import asyncio

from src.protocol.sync_protocol import start_sync_protocol
from src.server.http_server import MyServer


hostName = "localhost"
serverPort = 8080

async def main():
    thread = Thread(target = run_server)
    thread.start()
    thread.join()

    async with ClientSession() as session:
        start_sync_protocol(session)

def run_server():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

asyncio.run(main())