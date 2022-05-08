from application import app
import datetime
from mongoengine import connect, Document, StringField, DateTimeField
connect(host=app.config["DB_URI"])

class Journal (Document):
    user_id = StringField(requireed=True)
    journal_body = StringField(required=True)
    timestamp = DateTimeField(required=True, default=datetime.datetime.utcnow)


    meta = {
        "indexes": ["-timestamp"]
    }

# This method saves a users jounral entry. It takes in the journal entry information as data.
# A journal object is created form the data passed in. If the save is successful a res object is
# is returned. If it fails an error is returned.
    def save_journal(data):
        journal = Journal(
            user_id = data['user_id'],
            journal_body = data['journal_body']
        )
        if journal.save():
            res = {
                "user_id" : journal['user_id'],
                "journal_body" : journal['journal_body'],
                "timestamp": journal['timestamp']
            }
            return res
        # Catch all error incase anything else fails
        return {"error":"Sorry! Failed to save journal entry","status":400}

# this method gets all the journal entries according to the user's id.
def get_all_journals(data):
    journals  = Journal.objects(user_id=data).order_by("-timestamp")
    if journals:
        res = {
            "journals":[],
            "status": 200
        }
        for journal in journals:
            id = str(journal['id'])
            j = {
                "id":id,
                "user_id":journal.user_id,
                "journal_body":journal.journal_body,
                "timestamp": journal.timestamp
            }
            res['journals'].append(j)
        return res
    return {"error":"Sorry! Could not retrieve journal entry"}