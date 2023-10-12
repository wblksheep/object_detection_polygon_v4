import multiprocessing
from kivy.app import App
from kivy.uix.button import Button

def run_new_process_screen():
    # 定义一个新的 Kivy App
    class NewProcessApp(App):
        def build(self):
            return Button(text="It's a new Kivy Screen!")

    NewProcessApp().run()

class MainApp(App):
    def build(self):
        btn = Button(text="click me to open a new screen")
        btn.bind(on_press=self.spawn_new_process)
        return btn

    def spawn_new_process(self, instance):
        # 使用 multiprocessing 创建新的进程来运行独立的 Kivy App
        p = multiprocessing.Process(target=run_new_process_screen)
        p.start()

if __name__ == '__main__':
    MainApp().run()
