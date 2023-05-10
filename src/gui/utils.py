import tkinter as tk
from tkinter import messagebox

def show_help_message():
    help_text = "1. 点击摄像头捕获按钮获取图像。\n" \
                "2. 在图像上点击四个点以创建多边形区域。\n" \
                "3. 使用滑块调整多边形区域的形状。\n" \
                "4. 查看实时检测结果和统计信息。\n" \
                "5. 保存检测结果和多边形设置。"
    messagebox.showinfo("操作提示", help_text)
