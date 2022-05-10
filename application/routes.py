from application import app, models, socket, chatbot, chat_log, mood_log, Journal
from flask import jsonify, request, make_response
from flask_jwt_extended import JWTManager,jwt_required, get_jwt_identity, decode_token   
import datetime

jwtManager = JWTManager(app)


#       **** Routes / Controllers ****



#       **** User Routes / Controllers ****
# Register Route
@app.route('/users/register', methods=['POST'])
def register():
    # Requesting JSON from request and using get_json() to parse it to a python Dict
    req = request.get_json()
    # Calling the saveUser() from the User model and passing it the python Dict. The response of createUser() is assigned to response
    register = models.User.saveUser(req)
    if register:
        authenticate = models.User.authenticate(req)
    
    # Changing python Dict from response using Jsonify and return JSON response ot client
    return make_response(jsonify(authenticate), authenticate['status'])

# Login route
@app.route('/users/login', methods=['POST'])
def login():
    # Requesting JSON from request and using get_json() to parse it to a python Dict
    req = request.get_json()
    print(req)
    # Calling the saveUser() from the User model and passing it the python Dict. The response of createUser() is assigned to response
    response = models.User.authenticate(req)
     # Changing python Dict from response using Jsonify and return JSON response ot client
  
    return make_response(jsonify(response), response['status'])


# Mood Routes
@app.route('/users/mood', methods=['GET'])
@jwt_required()
def get_moods():
    identity = get_jwt_identity()
    id  = identity['id']['$oid']
    print("/// This is the user id to get moods with")
    print(id)
    response = mood_log.Mood.get_moods(id)

    return make_response(jsonify(response))

@app.route('/users/mood', methods=['POST'])
@jwt_required()
def create_mood():
    mood = request.get_json()
    identity = get_jwt_identity()
    id  = identity['id']['$oid']
    print(id)
    print("///// Printing mood /////")
    print(mood)
    md = {
        "user_id": id,
        "mood":mood['mood'],
        "description":mood['description']
    }
    response = mood_log.Mood.save_mood(md)
    return make_response(jsonify(response), response['status'])

## Journal Routes
@app.route('/users/journal', methods=['POST'])
@jwt_required()
def create_journal_entry():
    data = request.get_json()
    identity = get_jwt_identity()
    id  = identity['id']['$oid']
    print(id)
    print(data)
    journal = {
        "user_id": id,
        "journal_body": data['journal_body']
    }
    response = Journal.Journal.save_journal(journal)
    return  make_response(jsonify(response))

@app.route('/users/journal', methods=['GET'])
@jwt_required()
def get_journal_entry():
    identity = get_jwt_identity()
    id  = identity['id']['$oid']
    response = Journal.get_all_journals(id)

    return make_response(jsonify(response))

# Chat Log Routes
@app.route('/users/chat_log', methods=['GET'])
@jwt_required()
def get_chat_log():
    identity = get_jwt_identity()
    id  = identity['id']['$oid']
    res = chat_log.Chat_log.get_log(id)
    return make_response(jsonify(res))


#       **** Test Routes / Controllers ****

@app.route('/HelloWorld')
def helloWorld():
    return jsonify({"message": "Hello World !"})

@app.route('/json', methods=['POST'])
def json():
    # get_json() takes in json from request and converts it to python dict
    req = request.get_json()
    # response is a python dict which will contain the name contained in req
    response = {
        "name": req.get("name"),
        "message":"JSON recieved, convert to Dict, then back to JSON and sent to you" 
    }
    # make_response is used to make the response. The function jsonify is passed 
    # through containing the response (python dict) which 
    # converts python dicts to json.
    res = make_response(jsonify(response), 200)
    return res
    
@app.route('/test')
def test():
    response =  {"message":"Here is the response"}
    res = make_response(jsonify(access_token=response))
    return res


@app.route('/protected')
@jwt_required()
def protected():
    message = get_jwt_identity()
   
    return make_response(jsonify(message))


#       **** Socket.IO ****

@socket.event
@jwt_required()
def connect(auth):
    sid = request.sid
    user = auth
    identity = get_jwt_identity()
    print(identity)
    print("WebSocket connection established with React Native app")
  
    

@socket.on('user_login')
def user_login(user):
    user= user['email']
    print(f"My User info:{user}")

# This function takes in message, assigns message from user to user_message. Sends the user_message to chatbot model. 
# Creates datetime object to get current datetime and convert to a string. Create res object. 
# This object will be saved to the db and sent to user. Pause the for 0.3 seconds to create the illusion that 
# the chatbot is thinking. Sends res object back to React Native application.
@socket.on('msg_from_react')
def message_sent(message):
    sid = request.sid
    token_info = decode_token(message['token'])
    msg = {
        "user_id": token_info['sub']['id']['$oid'],
        "msg":message['msg'],
        "is_user": message['is_user'],
        "timestamp": message['timestamp'],
    }
    chat_log.Chat_log.saveMessage(msg)
    # Save user message with id here.
    user_msg = message['msg'] 
    amicaResponse = chatbot.chat(user_msg)
    dateTimeObj = datetime.datetime.today()
    timestampStr = dateTimeObj.isoformat()
    res = {
        "user_id": token_info['sub']['id']['$oid'],
        "msg": amicaResponse['response'],
        "is_user": False,
        "timestamp": timestampStr,
        "action": amicaResponse['action']
    }
    # Save amica message here
    chat_log.Chat_log.saveMessage(res)
    socket.emit("msg_from_flask", res, to=sid)

#@socket.on('get_chat_log')
#def get_chat_log(token):
#    sid= request.sid
#    token = decode_token(token)
#    id = token['sub']['id']['$oid']
#    res = chat_log.Chat_log.get_log(id)
#    # socket.emit('chat_log_from_flask', res,to=sid)
#    print(f"get chat log")

@socket.event
def disconnect():
    sid = request.sid
    print(f"User {sid} disconnected")
