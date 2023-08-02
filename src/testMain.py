import asyncio
import websockets
import queue
import threading
import time
import tkinter as tk
from gui.gui_main import TargetDetectionGUI

# WebSocket服务器
async def echo(websocket, path, gui):
    while True:  # 保持连接并在有数据时发送
        if not gui.data_queue.empty():  # 检查队列是否为空
            data = gui.data_queue.get()  # 从队列中获取数据
            await websocket.send(data)  # 发送数据到客户端
        else:
            await asyncio.sleep(0.1)  # 如果没有数据则稍微延迟以减少CPU占用

def websocket_server(gui):
    async def echo_wrapper(websocket, path):
        await echo(websocket, path, gui)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(echo_wrapper, "localhost", 8765)
    loop.run_until_complete(start_server)
    loop.run_forever()

def main():
    root = tk.Tk()
    root.title("Target Detection")
    root.geometry("5120x1800")
    root.resizable(False, False)

    app = TargetDetectionGUI(root)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    websocket_thread = threading.Thread(target=websocket_server, args=(app,))
    websocket_thread.start()

    root.mainloop()  # 阻塞主线程，等待Tkinter窗口关闭

    # 当Tkinter窗口关闭后，停止WebSocket服务器线程
    websocket_thread.join()

if __name__ == "__main__":
    main()
