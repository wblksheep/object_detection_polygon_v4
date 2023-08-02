import tkinter as tk

def print_text():
    print(entry_text.get())  # 当按钮被点击时，打印文本框内容

root = tk.Tk()

entry_text = tk.StringVar()  # 创建一个StringVar变量来存储文本框内容

entry = tk.Entry(root, textvariable=entry_text, width=200)  # 创建一个文本框，将StringVar变量绑定到它上面
entry.pack(expand=True)

button = tk.Button(root, text='Print Text', command=print_text)  # 创建一个按钮，点击时执行print_text函数
button.pack()

root.mainloop()
