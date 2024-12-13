from datetime import datetime
from services.firebase_service import FirebaseService
from datetime import datetime
import pytz
from services.json_crud import save_json, load_json
class Product:
    def __init__(self, name, description, price, category_id, image_url):
        self.id             = None  # ID will be set when the product is added to the database
        self.name           = name
        self.description    = description
        self.price          = price
        self.category_id    = category_id
        self.image_url      = image_url
        self.created_at     = datetime.now().isoformat()
        self.updated_at     = datetime.now().isoformat()

        self.CACHE_FILE = 'cache/product.json'

        self.firebase = FirebaseService()
        self.db = self.firebase.db
    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'image_url': self.image_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def save(self,orders):
        """Save the order data to a JSON cache file."""
        save_json(json_file=self.CACHE_FILE,data=orders)
    
    def load(self):
        return load_json(json_file=self.CACHE_FILE)
    # def load_products(self):
    #     with open(self.json_file, 'r') as f:
    #         return json.load(f)

    # def save_products(self,products):
    #     with open(self.json_file, 'w') as f:
    #         json.dump(products, f, indent=4)
        
    def read_product(self,product_id):
        products = self.load_products()
        product_list=[]
        for product in products:
            if product['id'] == product_id:
                product_list.append(product)
            else:
                product_list.append(product)

        return product_list

    def convert_firebase_timestamp(self,timestamp):
        if timestamp:
            utc_dt = datetime.fromtimestamp(timestamp / 1000, tz=pytz.UTC)
            return "T".join(str(utc_dt.astimezone(pytz.timezone("Africa/Cairo"))).split(' '))
    
    # def sync_products(self):
    #     auth = AuthController()
    #     profile = auth.load_user_profile()
    #     return self.firebase.read_data('products',profile['idToken'])