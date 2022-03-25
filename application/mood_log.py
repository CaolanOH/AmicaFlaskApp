
from application import app
import json
from mongoengine import connect, Document, StringField, DateTimeField
import datetime
connect(host=app.config["DB_URI"])

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Mood (Document):
    mood = StringField(required=True)
    description = StringField(required=True)
    user_id = StringField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "indexes": ["-timestamp"]
    }

    def save_mood(data):
        # Creating Mood Object
        mood = Mood(
            mood = data['mood'],
            description = data['description'],
            user_id = data['user_id'],

        )

        # Saving Moode Object to database. If save runs successfully the mood is return. If the savve() fails it returns an error
        if mood.save():
            
            res = {
                "mood": mood['mood'],
                "description": mood['description'],
                "user_id": mood['user_id'],
                "timestamp": mood.timestamp.isoformat(),
                "status": 201
            }
            return res
        return {"error":"Failed to save mood","status":400}
# This Method takes in a user id and queries the database for moods with that id. It returns an array of moods matching the user id passed in.
    def get_moods(data):
        if Mood.objects(user_id=data):
            moods = Mood.objects(user_id=data)
            res = {
                "moods": [],
                "status": 200
            }
            for mood in moods:
                id  = str(mood['id'])
                md = {
                    'id': id,
                    "moods": mood.mood,
                    "description": mood.description,
                    "user_id": mood.user_id,
                    "timestamp": mood.timestamp
                }
                res['moods'].append(md)
            return res
        return {"error":"Sorry! Could not retrieve moods.", "status":400}


