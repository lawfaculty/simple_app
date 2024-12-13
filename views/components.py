from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivymd.uix.textfield import MDTextField
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
class Product(ButtonBehavior,MDBoxLayout):
    id             = NumericProperty()
    name           = StringProperty("")
    price          = NumericProperty()
    quantity       = NumericProperty()
    image_url      = StringProperty("")
    description    = StringProperty("")
    category_id    = NumericProperty()
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "price":self.price,
            "quantity":self.quantity,
            "image_url":self.image_url,
            "description":self.description,
            "category_id":self.category_id,
            }

    

    def update_basket(self,main):
        Basket.update_basket(Basket,self.to_dict())
        Basket.render_status(Basket,main)
class OrderItem(ButtonBehavior,MDBoxLayout):
    id             = NumericProperty()
    name           = StringProperty("")
    price          = NumericProperty()
    quantity       = NumericProperty()
    image_url      = StringProperty("")
    description    = StringProperty("")
    category_id    = NumericProperty()

    def __init__(self, **kwargs):
        super(OrderItem, self).__init__(**kwargs)

class Basket(ButtonBehavior,MDBoxLayout):
    items       = []
    total_price = NumericProperty()
    counter     = NumericProperty()
    def update_basket(self,data):
        duplicate = False
        self.total_price = 0
        for item in self.items:
            if data['id'] == item['id']:
                if data['quantity'] > 0:
                    self.items[self.items.index(item)]['quantity'] = data['quantity']
                else:
                    self.items.remove(item)
                duplicate = True
        if not duplicate:
            self.items.append(data)
        
        self.total_price = 0 
        self.counter = 0
        for item in self.items:
            self.total_price += item['price']*item['quantity']
            self.counter += item['quantity']

    def render(self,parent):
        parent.get_screen('basket_view').ids.order_list.clear_widgets()
        for item in self.items:
            widget = OrderItem()
            widget.name = item['name']
            widget.price = str(item['price'])
            widget.quantity = int(item['quantity'])
            widget.image_url = item['image_url']
            parent.get_screen('basket_view').ids.order_list.add_widget(widget)
    
    def render_status(self,parent):
        # parent.get_screen('checkout').ids.basket
        parent.get_screen('home_view').ids.basket.ids.total_price.total_price = str(self.total_price)
        parent.get_screen('home_view').ids.basket.ids.counter.text = str(self.counter)
        if Basket.counter > 0:
            parent.get_screen('home_view').ids.basket.pos_hint = {'center_y':.5}
        else:parent.get_screen('home_view').ids.basket.pos_hint = {'center_y':-1}

class OrderCard(ButtonBehavior,MDBoxLayout):
    order_id = StringProperty()
    order_date = StringProperty()
    order_total = StringProperty()
    order_status = StringProperty()
    order_items = ListProperty()
    order_created_at = StringProperty()
    order_delivered_at = StringProperty()

class OrderDetail(ButtonBehavior,MDBoxLayout):
    product_id = StringProperty()
    product_name = StringProperty()
    product_image_url = StringProperty()
    product_price = NumericProperty()
    product_quantity = NumericProperty()

def ar(text):
    import bidi.algorithm
    import arabic_reshaper
    text = bidi.algorithm.get_display(arabic_reshaper.reshape(text))
    return text

class InputBox(TextInput):
    str = StringProperty()
    def __init__(self, **kwargs):
        super(InputBox, self).__init__(**kwargs)
        self.text = ''

    def insert_text(self, substring, from_undo=False):
        filter = None
        if substring.isalpha():
            filter = 'null'
        elif substring == ' ':
            filter = 'null'
        elif substring.isdigit():
            filter = 'number'  
        if self.input_type == filter or (filter== 'number' and self.input_type=='null'): 
            if len(self.str+substring)-1 < self.max_length:
                substring = substring[:self.max_length - len(self.text)]
                self.str = self.str+substring
                self.text = ar(self.str)
                substring = ""
                self.do_cursor_movement(action='cursor_home', control=False, alt=False)
                return super(InputBox, self).insert_text(substring, from_undo)

    def move_cursor(self):
        print('move')
        print(self.cursor_pos)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str)-1]
        self.text = ar(self.str)
        self.do_cursor_movement(action='cursor_home', control=False, alt=False)


class Load(FloatLayout):
    def __init__(self, **kwargs):
        super(Load, self).__init__(**kwargs)
        Window.bind(on_touch_down=self.lock_view)
    
    def lock_view(self,window,touch):
        if self.state:
            if self.ids.load_close.collide_point(*touch.pos):
                pass
            else:
                return True