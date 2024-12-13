from libraries.utils.pyrebase import pyrebase
# import pyrebase
def initialize_firebase():
    firebase_config = {
            "apiKey": "AIzaSyCOEYQLIiTIFoic1rNbv2qAVhmL3KKGFi0",
            "databaseURL":"https://storage-test-66e1e-default-rtdb.firebaseio.com/",
            "authDomain": "storage-test-66e1e.firebaseapp.com",
            "projectId": "storage-test-66e1e",
            "storageBucket": "storage-test-66e1e-default-rtdb.appspot.com",
            "messagingSenderId": "1007638083317",
            "appId": "1:1007638083317:web:92789c7c83681e9fdb37bc",
            "measurementId": "G-SX7EES4YPT"
            }
    firebase = pyrebase.initialize_app(firebase_config)
    return firebase
