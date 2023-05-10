import tkinter as tk
# 在CustomSlider类中，我们定义了一个带有标签的滑块，可以获取和设置滑块的值。
class CustomSlider:
    def __init__(self, parent, min_value, max_value, default_value, label_text, command):
        self.slider_frame = tk.Frame(parent)
        self.slider_frame.pack(side='left', padx=5)

        self.label = tk.Label(self.slider_frame, text=label_text)
        self.label.pack()

        self.slider = tk.Scale(self.slider_frame, from_=min_value, to=max_value, orient='horizontal', command=command)
        self.slider.set(default_value)
        self.slider.pack()

    def on_slider_change(self, value):
        self.slider.set(value)

    def get_slider_value(self):
        return self.slider.get()
