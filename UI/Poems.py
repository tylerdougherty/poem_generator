from kivy.app import App
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

Window.clearcolor = (1, 1, 1, 1)
Window.size = (400, 600)


class PoemsApp(App):
    def build(self):
        parent = Widget(size=(200, 200))
        parent.add_widget(TextInput(size=(150, 300)))
        return parent


if __name__ == '__main__':
    PoemsApp().run()
