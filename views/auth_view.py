from kivy.uix.screenmanager import Screen
from controllers.auth_controller import AuthController
from libraries.utils.error_handler import error_handler
from kivy.clock import Clock

class AuthView(Screen):
    def __init__(self, **kwargs):
        super(AuthView, self).__init__(**kwargs)
        self.controller = AuthController()

    @error_handler
    def auth(self):
        def callback(*args):
            self.ids.load.state = False
            self.parent.current = 'home_view'
            self.parent.get_screen('home_view').list_product_view(1)
        email = self.ids.email.text
        password = self.ids.password.text
        
        self.ids.load.state = True
        if self.login(email,password):
            Clock.schedule_once(callback,2)
        elif self.register(email,password):
            Clock.schedule_once(callback,2)
        else:
            self.ids.load.error = True
        
        # if 'idToken' in self.controller.load_user_profile():
        # elif self.register(email,password):
        #     Clock.schedule_once(callback,.5)
        
        # if 
        #     self.parent.current = 'home_view'
        #     return True
        # elif self.login(email,password):
        #     print('register')
        #     return False

    def login(self,email,password):
        user = self.controller.login(email, password)
        print('login ',user)
        if user:
            return True
        else:return False

    def register(self,email,password):
        user = self.controller.register(email, password)
        print('register ',user)
        if user:
            return True
