import asyncio
import websockets

async def receive_data():
    uri = "ws://localhost:8763"  # 此处应替换为你的WebSocket服务器地址
    while True:  # 尝试重连的外层循环
        try:
            async with websockets.connect(uri) as websocket:
                while True:  # 接收消息的内层循环
                    message = await websocket.recv()
                    print(f"Received message: {message}")
        except websockets.ConnectionClosedError as e:
            print(f"Connection closed unexpectedly: {e}")
            await asyncio.sleep(1)  # 等待一秒后尝试重新连接

# 执行异步任务
asyncio.get_event_loop().run_until_complete(receive_data())
