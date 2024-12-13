# views/order_view.py
from kivy.uix.screenmanager import Screen
from controllers.auth_controller import AuthController
from controllers.order_controller import OrderController
from libraries.utils.error_handler import error_handler
from kivy.clock import Clock

class UserInfoView(Screen):
    def __init__(self, **kwargs):
        super(UserInfoView, self).__init__(**kwargs)
        self.controller = AuthController()
        self.order = OrderController()
        self.is_profile = None
    
    def validate_input(self):
        inputs = [
            self.ids.input_district,
            self.ids.input_flat_no,
            self.ids.input_building_no,
            self.ids.input_phone]
        state = []
        for i in inputs:
            if i.state is False:
                i.parent.alert = True
                state.append(False)
        if False in state:
            return False
        else:
            return True

    # @error_handler
    def checkout(self):
        # self.disabled = True
        def callback(*args):
            try:
                order_write = None
                items = self.parent.get_screen('home_view').ids.basket.items
                localId = self.controller.get_user_id()
                idToken = self.controller.get_user_token()
                order = self.order.create_order(items)
                order_write = self.order.send_order(order,localId,idToken)
                if order_write:
                    # perform successful operation
                    self.order.send_order_date(order_write['name'],localId,idToken)
                    order = self.order.get_order(order_write['name'],localId,idToken)
                    merge = self.order.sync_orders(order)
                    self.order.save_order(merge,order_write['name'])
                    self.ids.load.state = False
                    self.parent.current = "order_status"
                else:self.ids.load.error = True
            except:
                self.ids.load.error = True

        self.ids.load.state = True
        Clock.schedule_once(callback,2)
        Clock.schedule_once(self.init_basket,2.1)


    def init_basket(self,*args):
        main = self.parent.get_screen('home_view')
        main.ids.basket.items.clear()
        main.ids.basket.total_price = 0
        main.ids.basket.counter = 0
        main.ids.basket.pos_hint = {'center_y':-1}
        main.refresh_product_view()

    @error_handler
    def set_user_profile(self):
        address = [
            self.ids.input_street.text,
            self.ids.input_district.text,
            self.ids.input_building_no.text,
            self.ids.input_flat_no.text,
            self.ids.input_floor_no.text,
            ]
        profile_label = self.ids.input_label.text
        format_address = ', '.join(address)
        phone = self.ids.input_phone.text
        profile = self.controller.set_user_profile(profile_label,format_address,phone)
        self.controller.send_user_profile(profile)
    
    def user_info_view_init(self):
        print('check user profile ...')
        profile = self.controller.is_user_profile()
        if profile:
            self.user_view_auto_fill(profile)
            self.is_profile = True
        else:
            self.is_profile = False

    def user_view_auto_fill(self,profile):
        print(profile['profile']['address'].split(', '))
        i = profile['profile']['address'].split(', ')
        self.ids.input_street.text = i[0]
        self.ids.input_district.text = i[1]
        self.ids.input_building_no.text = i[2]
        self.ids.input_flat_no.text = i[3]
        self.ids.input_floor_no.text = i[4]
        self.ids.input_phone.text = profile['profile']['phone']
        self.ids.input_label.text = profile['profile']['label']
    
