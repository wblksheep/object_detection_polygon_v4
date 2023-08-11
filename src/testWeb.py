import asyncio
from random import random
import websockets

class MySender:
    def __init__(self, port):
        self.port = port

    async def send_data(self, data):
        async with websockets.connect(f'ws://localhost:{self.port}') as websocket:
            await websocket.send(f'{data}')

    async def start_sending(self, data_stream):
        async for data in data_stream:
            await self.send_data(data)

async def generate_data_stream1(condition):
    # 基于某些条件生成数据流
    while True:
        data = random() * condition  # 基于条件产生数据
        await asyncio.sleep(10)  # 等待10秒
        yield data
async def generate_data_stream2(condition):
    # 基于某些条件生成数据流
    while True:
        data = random() * condition  # 基于条件产生数据
        await asyncio.sleep(5)  # 等待5秒
        yield data

async def main():
    # 创建两个不同实例，使用不同的端口
    # sender1 = MySender(port=8760)
    sender2 = MySender(port=8761)

    # 两个不同的数据流
    data_stream1 = generate_data_stream1(5)
    data_stream2 = generate_data_stream2(10)

    # 同时启动两个发送任务
    await asyncio.gather(
        # sender1.start_sending(data_stream1),
        sender2.start_sending(data_stream2)
    )

# 启动主任务
asyncio.get_event_loop().run_until_complete(main())
