from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class Chat():
    def build(self):
        b = BoxLayout(orientation='vertical')  # The default BoxLayout, no
        # extra properties set
        t = TextInput(text='default',
              font_size=15,
              size_hint_y=None,
              height=200)
        f = FloatLayout()
        s = Scatter()
        l = Label(text='Hello!', font_size=200)

        t.bind(text=l.setter('text'))

        f.add_widget(s)
        s.add_widget(l)
        b.add_widget(f)
        b.add_widget(t)
        return b

class InterfaceApp(App):
    def build(self):
        main_widget = BoxLayout(orientation='horizontal')

        ####### chat #######
        chat = BoxLayout(orientation='vertical')
        t = TextInput(text='default', font_size=15, size_hint_y=0.15, height=100)
        f = FloatLayout()
        s = Scatter()
        l = Label(text='Hello!', font_size=20, size_hint_y=0.85)

        t.bind(text=l.setter('text'))

        f.add_widget(s)
        s.add_widget(l)
        chat.add_widget(f)
        chat.add_widget(t)
        ####### end chat #######

        ####### dummy #######
        carte = BoxLayout(orientation='vertical')
        dummy_label = Label(text='Je suis un label', font_size=20)
        carte.add_widget(dummy_label)
        ####### end dummy #######

        main_widget.add_widget(chat)
        main_widget.add_widget(carte)
        return main_widget

    pass

if __name__ == "__main__":
    InterfaceApp().run()
