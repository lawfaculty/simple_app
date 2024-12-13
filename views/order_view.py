# views/order_view.py
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from views.components import OrderCard, OrderDetail
from controllers.order_controller import OrderController
from controllers.auth_controller import AuthController
from kivy.animation import Animation
class OrderView(Screen):
    def __init__(self, **kwargs):
        super(OrderView, self).__init__(**kwargs)
        self.controller = OrderController()
        self.user = AuthController()
        # Clock.schedule_once(self.render,.1)

    def order_view_init(self):
        self.render(.1)
        # self.user.get_user_id()
        # self.user.get_user_token()
        # self.controller.get
        # if self.get_orders():

    def get_orders(self,localId,idToken,date):
        return self.controller.get_orders(localId,idToken,date)
        
    def order_view_udpate(self):
        if self.update_attempt < 5:
            self.ids.load.state = True
            self.ids.load.error = False
            self.update_attempt += 1
            products = self.controller.list_products()
            if self.download_attempt and not self.controller.is_updated(date):
                self.ids.load.state = True
                self.ids.load.error = True
                self.ids.load.error_msg = 2
                self.download_attempt = None
            else:
                Clock.schedule_once(self.download_product_view,.1)
                Clock.schedule_once(self.update_product_view,5)
        else:
            self.ids.load.state = True
            self.ids.load.error = True
            self.ids.load.error_msg = 0
            self.update_attempt = 0

        # def callback(*args):
        #     idToken = self.user.get_user_token()
        #     orders = self.controller.get_orders(idToken)
        #     print(orders)
        #     if orders:
        #         self.controller.sync_orders(orders)
        #         self.ids.load.state = False
        #     else:self.ids.load.error = True
        # self.ids.load.state = True
        # Clock.schedule_once(callback,.1)

    def render(self,_):
        orders = self.controller.load_orders()
        self.ids.order_card_list.clear_widgets()
        for order in orders.items():
            widget = OrderCard()
            widget.order_id = order[0]
            order = order[1]
            widget.order_date = self.controller.format_date(order['created_at'])
            widget.order_total = str(order['total'])
            widget.order_status = order['status']
            widget.order_items = order['items']
            widget.order_created_at = self.controller.format_time(order['created_at'])
            if widget.order_status == 'delivered':
                widget.order_delivered_at = order['delivered_at']
            self.ids.order_card_list.add_widget(widget)

    def animate_order_detail(self,state):
        if state:
            Animation(pos_hint={"center_y":.4},duration=.2).start(self.ids.order_detail_card)
            Animation(back_opacity=.7,duration=.2).start(self.ids.order_detail)
        else:
            Animation(pos_hint={"center_y":-.5},duration=.2).start(self.ids.order_detail_card)
            Animation(back_opacity=0,duration=.2).start(self.ids.order_detail)
    def view_order_detail(self,order_object,order_items):
        self.animate_order_detail(state=True)
        self.ids.order_detail.order_id = order_object.order_id
        self.ids.order_detail.order_date = order_object.order_date
        self.ids.order_detail.order_total = order_object.order_total
        self.ids.order_detail.order_status = order_object.order_status
        self.ids.order_detail.order_created_at = order_object.order_created_at
        self.ids.order_detail.order_delivered_at = order_object.order_delivered_at
        
        self.ids.order_card_detail_item_list.clear_widgets()
        for item in order_items:
            widget = OrderDetail()
            widget.product_id = str(item['id'])
            widget.product_name = item['name']
            widget.product_image_url = item['image_url']
            widget.product_price = item['price']
            widget.product_quantity = item['quantity']
            self.ids.order_card_detail_item_list.add_widget(widget)

    # def order_view_init(self):
    #     items = self.parent.get_screen('home_view').ids.basket.items
    #     self.controller.create_order(items)