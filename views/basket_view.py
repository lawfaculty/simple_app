# views/order_view.py

from controllers.order_controller import OrderController
from controllers.auth_controller import AuthController
from kivy.app import App
from kivy.uix.screenmanager import Screen

from kivy.uix.label import Label
from kivy.clock import Clock
from views.components import Basket
from datetime import datetime

class BasketView(Screen):
    def __init__(self, **kwargs):
        super(BasketView, self).__init__(**kwargs)
        self.controller = OrderController()
        self.auth = AuthController()
        self.orders = {}  # Keep track of orders for the UI

    def update_basket(self,order_item):
        for item in self.parent.get_screen('home_view').ids.basket.items:
            if order_item.name == item['name']:
                item['quantity'] = order_item.quantity
                for product in self.parent.get_screen('home_view').ids.product_list.children:
                    if product.name == order_item.name:
                        product.quantity = order_item.quantity
        self.parent.get_screen('home_view').ids.basket.update_basket(self.parent.get_screen('home_view').ids.basket.items[0])
        self.parent.get_screen('home_view').ids.basket.render_status(self.parent)

    # def create_order(self):
    #     user_id = self.auth.get_user_id()
    #     items = self.parent.get_screen('home_view').ids.basket.items
    #     return self.controller.create_order(user_id,items)

    def basket_checkout(self):
        self.parent.transition.duration = .1
        self.parent.transition.direction = 'left'
        self.parent.current = 'user_info_view'
        self.parent.get_screen('user_info_view').user_info_view_init()
        '''
        create order object
        check for user profile
        if exists prompt user for it
        if not ask user for a one
        after profile finish send order
        '''