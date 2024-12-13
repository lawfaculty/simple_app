# controllers/order_controller.py

import threading
# from config.firebase_config import db
from services.firebase_service import FirebaseService
from models.user import User
from models.order import Order
# from models.user import User
import json
from datetime import datetime, timezone

class OrderController:
    def __init__(self):
        self.order = Order()
        self.user = User()
        self.stream = None
        self.stop_event = threading.Event()
        self.firebase_service = FirebaseService()
        self.db = self.firebase_service.db

        self.cache_file = 'cache/order.json'

    def load_orders(self):
        return self.order.load()

    def save_order(self,order,order_id):
        orders = self.order.load()
        orders[order_id] = order
        self.order.save(order)

    def sync_orders(self,updates):
        # Load the JSON objects
        data1 = updates
        data2 = self.order.load()
        # Function to recursively merge dictionaries
        def merge_dicts(dict1, dict2):
            for key in dict1.keys():
                if key in dict2:
                    if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                        merge_dicts(dict1[key], dict2[key])
                    elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
                        # Merge lists by appending unique items
                        for item in dict1[key]:
                            if item not in dict2[key]:
                                dict2[key].append(item)
                    else:
                        dict2[key] = dict1[key]
                else:
                    dict2[key] = dict1[key]
        # Merge the JSON objects
        merge_dicts(data1, data2)
        return data2

    # def sync_orders(self,orders):
    #     self.order.save(orders)

    def create_order(self,items):
        # self.user.
        order = self.order.create_order(items)
        return order
    
    # def get_orders(self,user_id):
    #     orders = self.load_orders()
    #     user_orders = [order for order in orders if order['user_id'] == user_id]
    #     return user_orders

    def update_order(self,order_id, new_data):
        orders = self.load_orders()
        for order in orders:
            if order['id'] == order_id:
                order.update(new_data)
                order['updated_at'] = str(datetime.now().isoformat())
                self.save_order(orders)
                return order
        return None

    def delete_order(self,order_id):
        orders = self.load_orders()
        orders = [order for order in orders if order['id'] != order_id]
        self.save_order(orders)
        return True

    def send_order(self,order,localId,idToken):
        date = str(datetime.now().isoformat()).split('T')[0]
        print('send ...')
        print('order: ',order,'\ndate: ',date,'\nlocalId: ',localId,'\nidToken: ',idToken)
        result = self.firebase_service.write_data(f'orders/{date}/{localId}/',order,idToken)
        return result
    
    def send_order_date(self,order_id,localId,idToken):
        date = str(datetime.now().isoformat()).split('T')[0]
        result = self.firebase_service.write_data(f'users/{localId}/orders-date/{date}',order_id,idToken)
        return result

    def get_order(self,order_id,localId,idToken):
        date = str(datetime.now().isoformat()).split('T')[0]
        result = self.firebase_service.read_data(f'orders/{date}/{localId}/{order_id}',idToken)
        return {"orders":{date:{localId:{order_id:result}}}}
    
    def get_order_date(self,localId,idToken,date):
        date = str(datetime.now().isoformat()).split('T')[0]
        return self.firebase_service.read_data(f'users/{localId}/orders-date/',idToken)
    
    def get_orders(self,localId,idToken,date):
        # date = str(datetime.now().isoformat()).split('T')[0]
        return self.firebase_service.read_data(f'orders/{date}/{localId}',idToken)
    
    def format_timestamp(self,timestamp):
        return self.order.convert_firebase_timestamp(timestamp=timestamp)

    def format_date(self,datestamp):
        return self.order.convert_firebase_timestamp(timestamp=datestamp).split('T')[0]

    def format_time(self,datestamp):
        return self.order.convert_firebase_timestamp(timestamp=datestamp).split('T')[1].split('.')[0]

    # def check_user_profile(self):
    #     self
    # def update_products(self):
    #     pass
    # def create_order(self, order_data):
    #     """Add a new order to the database."""
    #     order = Order(**order_data)
    #     self.db.child("orders").child(order.order_id).set(order.to_dict())
    #     return order.to_dict()

    # def update_order(self, order_id, updates):
    #     """Update an order's status or other fields."""
    #     self.db.child("orders").child(order_id).update(updates)

    # def delete_order(self, order_id):
    #     """Delete an order from the database."""
    #     self.db.child("orders").child(order_id).remove()

    # def get_orders(self):
    #     """Fetch all orders from Firebase."""
    #     orders = self.db.child("orders").get()
    #     if orders.each():
    #         return [order.val() for order in orders.each()]
    #     return []

    # def listen_for_orders(self,date):
    #     """Start listening for orders in a separate thread."""
    #     print('controller listening')
    #     idToken = User().load()['idToken']
    #     self.firebase_service.start_order_stream(date=date,idToken=idToken,callback=self.handler)
    
    # def handler(self,message):
    #     # order
    #     for data in message['data'].items():
            # client = data[0]
            # print('data ',data)
            # for customer_id, orders in data.items():
                # self.customer_id = customer_id
                # print(customer_id)
                # for order in orders.items():
                #     # chunk = {
                #     #     "order_id": order[0],
                #     #     "items": order[1].get('items'),
                #     #     "total": order[1].get('total'),
                #     #     "status": order[1].get('status')
                #     # }
                #     # self.orders.append(chunk)
                #     print(order[0])
                #     print(order[1].get('items'))
                #     print(order[1].get('total'))
                #     print(order[1].get('status'))

            # Order(data[0],data[1])
        # print('handling...')

    #     self.stop_event.clear()
    #     self.stream = threading.Thread(target=self._start_stream, args=(callback,))
    #     self.stream.start()

    # def _start_stream(self, callback):
    #     """Internal method to start Firebase stream."""
    #     # self.firebase_stream = db.child("orders").stream(callback)
    #     self.stop_event.wait()  # Keep thread alive until stop_event is set

    # def stop_listening(self):
    #     print('stop stream')
    #     self.firebase_service.stop_order_stream()
    #     """Stop the Firebase stream and terminate the thread."""
        # if self.stop_event.is_set():
        #     return  # Already stopped
        # self.stop_event.set()  # Signal the thread to stop
        # if self.firebase_stream:
        #     self.firebase_stream.close()  # Close Firebase stream


    # Start the real-time order stream
