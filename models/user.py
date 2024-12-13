import json
from services.json_crud import save_json, load_json
class User:
    def __init__(self):
        self.displayName = None
        self.email = None
        self.localId = None
        self.idToken = None
        self.refreshToken = None
        self.registered = None
        self.expiresIn = None
        self.address = None
        self.phone = None
        self.label = None
        # self.failed_attempts = 0
        
        self.CACHE_FILE = 'cache/user.json'

    def to_dict(self):
        return {
            'displayName':self.displayName if self.displayName else "",
            'email':self.email,
            'localId':self.localId,
            'idToken':self.idToken,
            'refreshToken':self.refreshToken,
            'registered':self.registered if self.registered else False,
            'expiresIn':self.expiresIn,
            'profile':{
                'address':self.address if self.address else None,
                'phone':self.phone if self.phone else None,
                'label':self.label if self.label else 'profile_1'
            }
        }

    def update(self,creds,type):
        self.localId = creds['localId']
        self.email = creds['email']
        self.idToken = creds['idToken']
        self.refreshToken = creds['refreshToken']
        self.expiresIn = creds['expiresIn']
        if type == 'login':
            self.registered = creds['registered']
            self.displayName = creds['displayName']
            load = self.load()
            self.address = load['profile']['address']
            self.phone = load['profile']['phone']
            self.label = load['profile']['label']
        elif type == 'profile':
            self.address = creds['profile']['address']
            self.phone = creds['profile']['phone']
            self.label = creds['profile']['label']
        elif type == 'register':
            pass
        return self.to_dict()

    def save(self,data):
        """Save the order data to a JSON cache file."""
        save_json(json_file=self.CACHE_FILE,data=data)
    
    def load(self):
        load = load_json(json_file=self.CACHE_FILE)
        if load == {}:
            return self.to_dict()
        else:return load
    # def save(self):
    #     with open(self.json_file, 'w') as f:
    #         json.dump(self.to_dict(), f, indent=2)

    # def load(self):
    #     with open(self.json_file, 'r') as f:
    #         creds = json.load(f)
    #         self.update(creds) 
    #         return self.to_dict()
    
    def set_user_profile(self,profile_label,address,phone):
        creds = self.load()
        self.update(creds,'profile')
        self.label = profile_label
        self.address = address
        self.phone = phone
        return self.to_dict()
    
    def check_user_profile(self,profile):
        print(profile)
        print(bool(None in profile.values()))
        if None in profile.values():
            return None
        else:
            return self.load()