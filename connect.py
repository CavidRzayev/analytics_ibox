import asyncio
import websockets



class A:
    def __init__(self):
        self.ip = ""

    async def hello():
        uri = "ws://localhost:8765/health/"
        async with websockets.connect(uri) as websocket:
            print(dir(websocket))
            greeting = await websocket.recv()

asyncio.run(A.hello())