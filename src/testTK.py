import tkinter as tk

root = tk.Tk()
root.title("Target Detection")
root.geometry("2560x1440")
root.resizable(False, False)

# 创建两个框架
frame1 = tk.Frame(root, width=1920, height=1080, background="blue")
frame2 = tk.Frame(root, width=200, height=200, background="blue")
frame1.grid_propagate(False)
# 在第一个框架中使用 grid
button1 = tk.Button(frame1, text="Button 1")
button2 = tk.Button(frame1, text="Button 2")
button1.grid(row=0, column=0)
button2.grid(row=1, column=0)
# button2.grid(row=0, column=1)
# button1= tk.Button(frame1, text="Button 1")
# button1.place(x=50, y=50)
# button2= tk.Button(frame1, text="Button 2")
# button2.grid(row=0, column=1)

# 在第二个框架中使用 place
button3 = tk.Button(frame2, text="Button 3")
button3.place(x=50, y=50)
# 将两个框架添加到窗口中
frame1.pack(side='top')
frame2.pack(side='bottom')


root.mainloop()
