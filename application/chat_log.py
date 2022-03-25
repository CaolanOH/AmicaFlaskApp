from application import app
from mongoengine import connect, ListField, Document, ObjectIdField, DateTimeField
connect(host=app.config["DB_URI"])
# This is a mongoDB Dynamic Document.
# Attributes can be added to this document dynmically before it is saved to DB
class Chat_log (Document):
    user_id = ObjectIdField(required=True)
    chat_log = ListField()


# This method takes in a message from the user or chatbot. Checks if the messages user_id already has a chat_log.
# If the user_id has a chat_log it appends the message to chat_log ListField and saves. If the user_id does not
# have a chat log it creates one, appends the message to the chat_log ListField and saves.
    def saveMessage(data):
        user_id = data['user_id']
        #msg = {
        #    "msg":data['msg'],
        #    "is_user": data['is_user'],
        #    "timestamp": data['timestamp'],
        #    "context": data['context']
        #}
        if Chat_log.objects(user_id=user_id):
            chat = Chat_log.objects(user_id=user_id).get()
         
            chat.chat_log.append(data)
            chat.save()
            return print("Message saved to db")
        else:
            chat = Chat_log(
                user_id = user_id,
            )
            chat.chat_log.append(data)
            chat.save()
            return print("Message saved to db")


# This method takes in a user_id. It takes this id and retrieves a chat_log with the respective user_id
    def get_log(data):
        log = Chat_log.objects(user_id=data).get()
        if log:
            print(log.chat_log)
            chat_log ={
                "log": log.chat_log,
                "status": 200
            }
            return chat_log
        return {"error":"Sorry! Unable to retrieve chat log","status":401}
            
        



     