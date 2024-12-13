from config.firebase_config import initialize_firebase
import requests, json, threading
from models.order import Order

class FirebaseService:
    def __init__(self):
        self.firebase = initialize_firebase()
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        
        self.order_stream = None
        self.stream_thread = None
        self.stop_event = threading.Event()

    # Authentication methods
    def login_user(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        if 'error' in user:
            return False
        else:
            return user
    
    def register_user(self, email, password):
        user = self.auth.create_user_with_email_and_password(email, password)
        if 'error' in user:
            return False
        else:
            return user
    
    def reset_password(self,email):
        return self.auth.send_password_reset_email(email)

    def get_account_info(self,idToken):
        return self.auth.get_account_info(idToken)
    
    def check_idToken(self,id_token):
        request_ref = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={api_key}'.format(api_key=self.firebase['apiKey'])
        headers = {"content-type": "application/json; charset=UTF-8"}
        payload = json.dumps({'idToken': id_token})
        request_object = requests.post(request_ref, headers=headers, data=payload)

        return request_object.json()
    
    def refresh_token(self,refresh_token):
        request_ref = "https://securetoken.googleapis.com/v1/token?key={api_key}".format(api_key=self.firebase['apiKey'])
        payload = {"grant_type": "refresh_token","refresh_token": refresh_token}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_ref, headers=headers, data=payload)
        
        return response.json()
    

    # Additional methods as needed
        
    # CRUD operations for orders
    # def create_order(self, user_id, order_data):
    #     return self.db.child("orders").child(user_id).push(data=order_data, token=self.creds['idToken'])
    
    # def update_order(self, user_id, order_id, order_data):
    #     return self.db.child("orders").child(user_id).child(order_id).update(data=order_data, token=self.creds['idToken'])
    
    def read_data(self,path,idToken):
        data = self.db.child(path).get(token=idToken).val()
        print(f"Data read from {path}: {data}")
        return data

    def write_data(self,path,data,idToken):
        # print(f"Data write from {path}: {data}")
        return self.db.child(path).push(data, token=idToken)

    def update_data(self,path,data,idToken):
        self.db.child(path).set(data, token=idToken)
        print(f"Data write from {path}: {data}")

    def start_order_stream(self,date='',idToken=None,callback=None):
        self.order_stream = self.db.child("orders/2024-11-03").stream(callback,token=idToken)

    def stop_order_stream(self):
        """Stop the active order stream and terminate the thread."""
        print('object: ',self.order_stream)
        self.order_stream.close()  # Close the Firebase stream
        print("Order streaming stopped.")

    # def create_order(self, order_data):
    #     """Create a new order in the Firebase database."""
    #     self.db.child("orders").push(order_data)
    #     print("Order created in Firebase:", order_data)

    # def update_order(self, order_id, updated_data):
    #     """Update an existing order in the Firebase database."""
    #     self.db.child("orders").child(order_id).update(updated_data)
    #     print(f"Order {order_id} updated in Firebase:", updated_data)

    # def delete_order(self, order_id):
    #     """Delete an order from the Firebase database."""
    #     self.db.child("orders").child(order_id).remove()
    #     print(f"Order {order_id} deleted from Firebase.")