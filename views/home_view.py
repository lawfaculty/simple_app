# views/product_view.py
from kivy.uix.screenmanager import Screen
from controllers.product_controller import ProductController
from controllers.auth_controller import AuthController
from controllers.order_controller import OrderController


from views.components import Product
from kivy.clock import Clock
from libraries.utils.error_handler import error_handler

class HomeView(Screen):
    def __init__(self, **kwargs):
        super(HomeView, self).__init__(**kwargs)
        self.controller = ProductController()
        self.update_attempt = 0
        self.download_attempt = None
        Clock.schedule_once(self.list_product_view,.2)
    
    def order_view_init(self):
        self.parent.get_screen('order_view').order_view_init()

    @error_handler
    def empty_product_view(self):
        self.ids.id.text = '0'
        self.ids.name.text = ''
        self.ids.price.text = ''
        self.ids.description.text = ''
        self.ids.category_id.text = ''
        self.ids.image_url.text = ''
    
    # @error_handler
    def list_product_view(self,*args):
        products = self.controller.list_products()
        if products:
            products.pop('date')
            if self.is_product_view_updated():
                self.ids.update_product.status = True
                self.ids.update_product.md_bg_color = 0,0,0,.1
            else:
                self.ids.load.state = True
                self.ids.load.error = True
                self.ids.load.error_msg = 1
            for product in products.get('products'):    
                widget = Product()
                widget.id = product['id']
                widget.name = product['name']
                widget.price = product['price']
                widget.image_url = product['image_url']
                widget.description = product['description']
                widget.category_id = product['category_id']
                self.ids.product_list.add_widget(widget)
        self.ids.load.state = False
        self.ids.load.error = False
    @error_handler
    def refresh_product_view(self):
        self.ids.product_list.clear_widgets()
        Clock.schedule_once(self.list_product_view,.1)
    
    def is_product_view_updated(self):
        products = self.controller.list_products()
        date = self.controller.format_timestamp(products.get('date'))
        if self.controller.is_updated(date):
            return True
        else: return False

    @error_handler
    def update_product_view(self,*args):
        if self.update_attempt < 5:
            self.ids.load.state = True
            self.ids.load.error = False
            self.update_attempt += 1
            products = self.controller.list_products()
            date = self.controller.format_timestamp(products.get('date'))
            if self.controller.is_updated(date):
                self.refresh_product_view()
                self.update_attempt = 0
                self.ids.load.state = False
                self.ids.load.error = False
            elif self.download_attempt and not self.controller.is_updated(date):
                self.ids.load.state = True
                self.ids.load.error = True
                self.ids.load.error_msg = 2
                self.download_attempt = None
            else:
                Clock.schedule_once(self.download_product_view,.1)
                Clock.schedule_once(self.update_product_view,3)
        else:
            self.ids.load.state = True
            self.ids.load.error = True
            self.ids.load.error_msg = 0
            self.update_attempt = 0
        Clock.schedule_once(self.list_product_view,3)

    @error_handler
    def download_product_view(self,*args):
        attempt = self.controller.download_products()
        self.download_attempt = attempt

    def empty_basket(self,*args):
        self.ids.basket.items.clear()
        self.ids.basket.total_price = 0
        self.ids.basket.counter = 0
        self.refresh_product_view()
        print('widget: ',self.parent)
        print('class: ',HomeView.parent)
        # self.parent.get_screen('basket_view').ids.order_list.clear_widgets()
