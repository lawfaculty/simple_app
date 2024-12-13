from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock

from views.auth_view import AuthView
from views.home_view import HomeView
from views.basket_view import BasketView
from views.order_view import OrderView
from views.user_info_view import UserInfoView

from kivy.lang import Builder
import os

class MainView(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.key_input)

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if self.current == 'home_view':
                pass
            else:return True