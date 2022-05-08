
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
# save_mood method takes in a data object containing the mood data. A new Mood object
# is created using the data passed in. If the mood passes the validation a res object
# is created contain the mood, description, user_id, timestamp and status code is returned.
# if it fails and error is returned 
    def save_mood(data):
        # Creating Mood Object
        mood = Mood(
            mood = data['mood'],
            description = data['description'],
            user_id = data['user_id'],
        )
        # Saving Moode Object to database. If save runs successfully the mood is return. 
        if mood.save():
            res = {
                "mood": mood['mood'],
                "description": mood['description'],
                "user_id": mood['user_id'],
                "timestamp": mood.timestamp.isoformat(),
                "status": 201
            }
            return res
        # Catch all error incase anything else fails
        return {"error":"Failed to save mood","status":400}

# This Method takes in a user id and queries the database for moods with that id. It returns an array of moods matching the user id passed in.
    def get_moods(data):
        moods = Mood.objects(user_id=data).order_by("-timestamp")
        if moods:
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
        # Catch all error incase anything else fails
        return {"error":"Sorry! Could not retrieve moods.", "status":400}


