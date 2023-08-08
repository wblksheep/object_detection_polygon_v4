from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.text_input = TextInput(hint_text='Enter your text here')  # 创建文本输入框
        button = Button(text='Submit')

        button.bind(on_press=self.show_input)  # 绑定按钮事件

        layout.add_widget(self.text_input)
        layout.add_widget(button)

        return layout

    def show_input(self, instance):
        print("User input:", self.text_input.text)  # 输出用户输入的文本


if __name__ == '__main__':
    MyApp().run()
