# import tkinter as tk
# from gui.gui_main import TargetDetectionGUI
#
# def main():
#     root = tk.Tk()
#     root.title("Target Detection")
#     root.geometry("5120x1800")
#     # root.resizable(True, True)
#     root.resizable(False, False)
#
#     app = TargetDetectionGUI(root)
#     # app.grid(row=0, column=0, sticky="nsew")
#
#     root.rowconfigure(0, weight=1)
#     root.columnconfigure(0, weight=1)
#
#     root.mainloop()
#
# if __name__ == "__main__":
#     main()

import atexit
import threading
import tkinter as tk
from gui.gui_main import TargetDetectionGUI
import asyncio
import websockets
import queue
import time
import json

# WebSocket服务器
async def echo(websocket, path, gui):
    while True:  # 保持连接并在有数据时发送
        if not gui.data_queue.empty():  # 检查队列是否为空
            points = []
            while not gui.data_queue.empty():
                points.append(gui.data_queue.get())
            json_data = json.dumps({'points': points})
            await websocket.send(json_data)  # 发送数据到客户端
        else:
            await asyncio.sleep(0.1)  # 如果没有数据则稍微延迟以减少CPU占用

def websocket_server(gui):
    async def echo_wrapper(websocket, path):
        await echo(websocket, path, gui)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(echo_wrapper, "192.168.40.145", 8765)
    loop.run_until_complete(start_server)
    loop.run_forever()

def main():
    root = tk.Tk()
    root.title("Target Detection")
    root.geometry("2560x1440")
    root.resizable(False, False)

    app = TargetDetectionGUI(root)
    app.run_server = True

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    websocket_thread = threading.Thread(target=websocket_server, args=(app,))
    websocket_thread.start()
    def cleanup():
        app.run_server = False
        websocket_thread.join()

    root.protocol("WM_DELETE_WINDOW", cleanup)
    atexit.register(cleanup)

    root.mainloop()

if __name__ == "__main__":
    main()

