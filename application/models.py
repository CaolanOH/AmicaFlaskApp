
from application import app
import json
from mongoengine import connect, Document, StringField, EmailField
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util 
connect(host=app.config["DB_URI"])
class Util:
    def parse_json(data):
        return json.loads(json_util.dumps(data))
# Defining documents
class User(Document):
    username = StringField(required=True)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)

    def jsonUser(self):
        user_dict = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        return json.dumps(user_dict)

    meta = {
        "indexes": ["username","email"]
    }

    def saveUser(data):
        # Creating user Dict
        user =  User(
            username = data['username'],
            email = data['email'],
            password = data['password'],
        )
        # Checking if email is already in database    
        if User.objects(email=user['email']):
            error = {"error": "Sorry email already exists !", "status":409}
            return error
        # Checking if password is greater than the minimun length
        if len(user['password']) < 5:
            error = {"error": "Password too short", "status":400}
            return error
        # Hashing password    
        user['password'] = generate_password_hash(user['password'], method='sha256', salt_length=10)
        # Saving to database     
        if user.save():
            # Creating new Dict to be sent back and jsonified
            res = {
                "username": user['username'],
                "email": user['email'],
                "message":"User created successfully !",
                "status":201
            }
            return res
        # Catch all error incase anything else fails
        return {"error":"Register Failed !","status":400} 

    def authenticate(data):
        # Find the user in the data by the email supplied
        user = User.objects(email=data['email']).get()
        if user and check_password_hash(user['password'],data['password']):
            user_dict = {"id":user['id'],
                        "username":user['username'],
                        "email": user['email']
                        }
            token = create_access_token(identity=Util.parse_json(user_dict))
            response = token
            return response
        return {"error":"Authorization denied", "status":401}

