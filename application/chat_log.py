from application import app
from mongoengine import connect, DynamicDocument, StringField, DateTimeField
connect(host=app.config["DB_URI"])
# This is a mongoDB Dynamic Document.
# Attributes can be added to this document dynmically before it is saved to DB
class Chat_log (DynamicDocument):

        def saveMessage(data):
            Chat_log.save()
            print("Message Saved to db")