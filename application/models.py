# Importing app variable application folder for DB connection
from application import app
import json
# MongoEngine Imports
from mongoengine import connect, Document, StringField, EmailField
# JWT Imports
from flask_jwt_extended import create_access_token
# Werkzeug Password Hash Import
from werkzeug.security import generate_password_hash, check_password_hash
# Bson import
from bson import json_util 

# MongoDB Connection
connect(host=app.config["DB_URI"])

class Util:
    def parse_json(data):
        return json.loads(json_util.dumps(data))


# Defining User document
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
# saveUser takes in an object containing a username, email, and password. A User object is created
# using the data passed. The User object is validated and saved. If the User object fails the validation
# an error is returned.
    def saveUser(data):
        # Creating user object
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
            user_dict = {
                        "id":user['id'],
                        "username":user['username'],
                        "email": user['email']
                        }
            token = create_access_token(identity=Util.parse_json(user_dict))
            res = {
                
                "username": user['username'],
                "email": user['email'],
                "access_token": token,
                "status": 200
            }
            return res
            # Catch all error incase anything else fails
        return {"error":"Authorization denied", "status":401}

