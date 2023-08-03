import asyncio
import websockets

async def receive_message():
    uri = "ws://192.168.2.10:8765"  # 改为你的服务器地址
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"< {message}")

asyncio.get_event_loop().run_until_complete(receive_message())
