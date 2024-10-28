from kivymd.app import MDApp
from screen import Main_Screen
from kivy.lang import Builder
import os

class MainApp(MDApp):
    def build(self):
        Builder.load_file(os.path.join(os.getcwd(), "screen.kv"))
        return Main_Screen()
    
if __name__ =='__main__':
    MainApp().run()