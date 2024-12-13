from services.firebase_service import FirebaseService
from models.user import User

class AuthController:
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.user = User()
        
    def login(self, email, password):
        user = self.firebase_service.login_user(email, password)
        if user:
            self.user.update(user,'login')
            self.user.save(self.user.to_dict())
            return user

    def register(self, email, password):
        user = self.firebase_service.register_user(email, password)
        if user:
            self.user.update(user,'register')
            self.user.save(self.user.to_dict())
            return user

    def get_user_id(self):
        return self.user.load()['localId']
    
    def get_user_token(self):
        return self.user.load()['idToken']
    
    def load_user_profile(self):
        return self.user.load()
    
    def update_user_profile(self,profile):
        self.user.update(profile,'profile')
        self.user.save(self.user.to_dict())

    def set_user_profile(self,profile_label,address,phone):
        creds = self.user.set_user_profile(profile_label,address,phone)
        self.user.update(creds,'profile')
        self.user.save(self.user.to_dict())
        return creds['profile']
    
    def send_user_profile(self,data):
        creds = self.user.load()
        idToken = creds['idToken']
        localId = creds['localId']
        self.firebase_service.update_data(f'users/{localId}',data,idToken)
    
    def is_user_profile(self):
        profile = self.user.load()['profile']
        return self.user.check_user_profile(profile)
