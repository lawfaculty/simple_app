# controllers/product_controller.py
from services.firebase_service import FirebaseService
from models.product import Product
from models.user import User
from datetime import datetime

class ProductController:
    def __init__(self):
        # Initialize a Product instance for database interactions
        self.product = Product("", "", 0.0, 0, "")
        
    def initialize_product_cache(self):
        """Initialize the product cache file with an empty structure."""
        self.product.initialize_products()
        return "Product cache initialized successfully."

    # def add_product(self, name, description, price, category_id, image_url):
    #     """Add a new product."""
    #     # new_product = Product(name, description, price, category_id, image_url)
    #     new_product = {
    #         "name":name,
    #         "description":description,
    #         "price":price,
    #         "category_id":category_id,
    #         "image_url":image_url,
    #     }
    #     result = self.product_model.create_product(new_product)
    #     return {"message": "Product created successfully", "product": result}

    def get_product(self, product_id):
        """Retrieve a specific product by ID."""
        product = self.product.read_product(product_id)
        if product:
            return {"product": product}
        else:
            return {"error": "Product not found"}

    def list_products(self):
        """Retrieve all products."""
        products = self.product.load()
        return products

    def download_products(self):
        idToken = User().load()['idToken']
        self.firebase_service = FirebaseService()
        new_data = self.firebase_service.read_data('products',idToken=idToken)
        if 'error' in new_data:
            return False
        else:
            self.product.save(new_data)
            return True
    
    def format_timestamp(self,timestamp):
        return self.product.convert_firebase_timestamp(timestamp=timestamp)
    
    def is_updated(self,timestamp):
        current_stamp = str(datetime.now().isoformat()).split('T')[0]
        timestamp = str(timestamp).split('T')[0]
        if current_stamp == timestamp:
            return True
        else:
            return False