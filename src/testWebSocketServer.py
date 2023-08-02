import asyncio
import websockets
import queue
import threading
import time

# 创建一个队列用于存储数据
data_queue = queue.Queue()

# 这是你的数据生成线程
def data_generator():
    while True:
        data = "Hello, client!"  # 生成你的数据
        data_queue.put(data)  # 将数据放入队列
        time.sleep(1)  # 模拟数据生成频率

# 启动数据生成线程
data_thread = threading.Thread(target=data_generator)
data_thread.start()

# WebSocket服务器
async def echo(websocket, path):
    while True:  # 保持连接并在有数据时发送
        if not data_queue.empty():  # 检查队列是否为空
            data = data_queue.get()  # 从队列中获取数据
            await websocket.send(data)  # 发送数据到客户端
        else:
            await asyncio.sleep(0.1)  # 如果没有数据则稍微延迟以减少CPU占用

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
