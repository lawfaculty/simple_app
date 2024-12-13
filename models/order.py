# models/order.py

import pytz
from datetime import datetime
from services.json_crud import save_json, load_json
# class OrderItem:
#     def __init__(self):


#     def to_dict(self):
#         return {
#             "id":self.order_id,
#             "name": self.product_name,
#             "quantity": self.quantity,
#             "unit_price": self.unit_price,
#         }

class Order:

    def __init__(self):
        self.id = None
        # self.user_id = None
        self.items = None
        self.total = None
        self.status = None
        self.created_at = None
        self.updated_at = None
    
        self.CACHE_FILE = 'cache/order.json'
    def to_dict(self):
        return {
            # "id":str(uuid.uuid4()),
            # "user_id":self.user_id,
            "items":self.items,
            "total":self.calculate_total(),
            "status":self.status,
            "created_at":{".sv": "timestamp"},
            "updated_at":self.updated_at
        }
    
    def save(self,orders):
        """Save the order data to a JSON cache file."""
        save_json(json_file=self.CACHE_FILE,data=orders)
    
    def load(self):
        return load_json(json_file=self.CACHE_FILE)
        # try:
        #     if not os.path.exists(os.path.dirname(self.CACHE_FILE)):
        #         os.makedirs(os.path.dirname(self.CACHE_FILE))

        #     with open(self.CACHE_FILE, 'w') as f:
        #         json.dump(orders, f, indent=4)
        #     print(f"Order {self.id} saved to cache.")
        # except Exception as e:
        #     print(f"Failed to save order to cache: {e}")

        # with open('cache/order.json', 'r') as f:
        #     return json.load(f)

    def calculate_total(self):
        """Calculate the total price of the order."""
        return sum(item['quantity'] * item['price'] for item in self.items)

    def create_order(self,items):
        # self.user_id = user_id
        self.items = items
        self.status = 'pending'
        return self.to_dict()

    def convert_firebase_timestamp(self,timestamp):
        if timestamp:
            utc_dt = datetime.fromtimestamp(timestamp / 1000, tz=pytz.UTC)
            return "T".join(str(utc_dt.astimezone(pytz.timezone("Africa/Cairo"))).split(' '))
    # def send_order(self,order):
    #     self.fire
    # def append_to_cache(self,data):
    #     print('load ',self.load())
    #     order_list = self.load()
    #     order_list.append(self.to_dict())
    #     with open(self.CACHE_FILE, 'w') as f:
    #         json.dump(order_list, f, indent=4)
    #     print(f"Order {self.order_id} saved to cache.")


    # def save_stream_to_cache(self,stream):
    #     print(stream)
        # for date in stream['data'].items():
        #     self.created_at = date[0]
        #     for customer_id, orders in date[1].items():
        #         self.customer_id = customer_id
        #         for order in orders.items():
        #             chunk = {
        #                 "order_id": order[0],
        #                 "items": order[1].get('items'),
        #                 "total": order[1].get('total'),
        #                 "status": order[1].get('status')
        #             }
        #             self.orders.append(chunk)
        #             # self. order_id = order[0]
        #             # self. items = order[1].get('items')
        #             # self.total = order[1].get('total')
        #             # self.status = order[1].get('status')
        #         print(self.to_dict())
        #         self.save()
    