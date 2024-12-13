from kivymd.app import MDApp
from views.main_view import MainView
from kivy.lang import Builder
import os
import bidi.algorithm
import arabic_reshaper
from kivy.core.window import Window
# from kivymd.utils.set_bars_colors import set_bars_colors
# from kvdroid.tools import change_statusbar_color

class GroceryApp(MDApp):
    def build(self):
        # Window.size = (450, 1000)
        # Window.left = 1140
        # Window.top = 40
        Window.clearcolor = (1,1,1,1)
        # change_statusbar_color('#12aa4b',"white")
        # set_bars_colors("#12aa4b",(1,1,1,1),"white")
        Builder.load_file(os.path.join(os.getcwd(), "kv/widgets.kv"))
        Builder.load_file(os.path.join(os.getcwd(), "kv/kivy.kv"))
        return MainView()

    def ar(self,text=""):
        text = bidi.algorithm.get_display(arabic_reshaper.reshape(text))
        return text
    
if __name__ == '__main__':
    GroceryApp().run()
