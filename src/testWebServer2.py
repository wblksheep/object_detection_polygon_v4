import asyncio
import websockets

async def send_message():
    uri = "ws://47.98.235.96:20030/webserver/python/1"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, World!")
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.get_event_loop().run_until_complete(send_message())