import asyncio
import websockets

async def channel_one(websocket, path):
    async for message in websocket:
        print(f"Channel One Received: {message}")

async def channel_two(websocket, path):
    async for message in websocket:
        print(f"Channel Two Received: {message}")

start_channel_one = websockets.serve(channel_one, "localhost", 8760)
start_channel_two = websockets.serve(channel_two, "localhost", 8761)

asyncio.get_event_loop().run_until_complete(start_channel_one)
asyncio.get_event_loop().run_until_complete(start_channel_two)
asyncio.get_event_loop().run_forever()
