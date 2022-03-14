
from application import app
import json
from mongoengine import connect, Document, StringField, DateTimeField
connect(host=app.config["DB_URI"])

class Mood (Document):
    mood = StringField(required=True)
    description = StringField(required=True)
    user_id = StringField(required=True)
    timestamp = DateTimeField(required=True, default=datetime.utcnow)

    meta = {
        "indexes": ["timestamp"]
    }

    def saveMood(data):
        # Creating Mood Object
        mood = Mood(
            mood = data['mood'],
            description = data['description'],
            user_id = data['user_id']
        )

        # Saving Moode Object to database. If save runs successfully the mood is return. If the savve() fails it returns an error
        if mood.save():
            res = {
                "mood": mood['mood'],
                "description": mood['description'],
                "user_id": mood['user_id'],
                "timestamp": ['timestamp'],
                "status": 201
            }
            return res
        return {"error":"Failed to save mood","status":400}
# This Method takes in a user id and queries the database for moods with that id. It returns an array of moods matching the user id passed in.
    def getAllMoods(data):
        if Mood.objects(user_id=data['user_id']):
            moods = Mood.objects(user_id=data['user_id']).get()
            res = {
                "moods": moods,
                "status": 200
            }
            return res
        return {"error":"Sorry! Could not retrieve moods.", "status":400}


