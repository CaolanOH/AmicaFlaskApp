from application import app
from mongoengine import connect, Document, StringField, DateTimeField
connect(host=app.config["DB_URI"])

class Journal (Document):
    user_id = StringField(requireed=True)
    journal_body = StringField(required=True)
    timestamp = DateTimeField(required=True, default=datetime.utcnow)



# This method saves a users jounral entry.
    def saveJounral(data):
        journal = Journal(
            user_id = data['user_id'],
            journal_body = data['journal_body']
        )
        if journal.save():
            res = {
                "user_id" : journal['user_id'],
                "journal_body" : journal['journal_body']
            }
            return res
        # If there is an error saving, method will return this error
        return {"error":"Sorry! Failed to save journal entry","status":400}

# this method gets all the journal entries according to the user's id.
def getAllJournals(data):
    if Journal.objects(user_id=data['user_id']):
        res  = Journal.objects(user_id=data['user_id'])
        return res
    return {"error":"Sorry! Could not retrieve journal entry"}