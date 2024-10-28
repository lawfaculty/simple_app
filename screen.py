from kivy.uix.screenmanager import ScreenManager
import pyrebase
import traceback

def error_handler(file_name='error_log.txt'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print('[ERROR] ',e)
                with open(file_name, 'a') as f:
                    f.write(f"Error in function '{func.__name__}': {str(e)}\n")
                    f.write(traceback.format_exc())
        return wrapper
    return decorator

class Main_Screen(ScreenManager):
    token = None
    result = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = {
            "apiKey": "AIzaSyCOEYQLIiTIFoic1rNbv2qAVhmL3KKGFi0",
            "databaseURL":"https://storage-test-66e1e-default-rtdb.firebaseio.com/",
            "authDomain": "storage-test-66e1e.firebaseapp.com",
            "projectId": "storage-test-66e1e",
            "storageBucket": "storage-test-66e1e-default-rtdb.appspot.com",
            "messagingSenderId": "1007638083317",
            "appId": "1:1007638083317:web:92789c7c83681e9fdb37bc",
            "measurementId": "G-SX7EES4YPT"
            }
        self.firebase = pyrebase.initialize_app(config)
        
    @error_handler()
    def list(self):
        auth = self.firebase.auth()
        email='admin@example.com'
        password = 'securepassword'
        user = auth.sign_in_with_email_and_password(email, password)

        self.ids.label.text += str(user)
        self.token = user['idToken']
        
    @error_handler()
    def stream(self):
        def stream_handler(message):
            print(message["event"])
            print(message["path"])
            print(message["data"])
            return message
        db = self.firebase.database()
        self.result = db.child("orders").stream(stream_handler,token=self.token)
        self.ids.label.text = str(self.result)
    
    @error_handler()
    def close_stream(self):
        self.result.close()
