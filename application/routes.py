from application import app, models, socket, chatbot, chat_log
from flask import jsonify, request, make_response
from flask_jwt_extended import JWTManager,jwt_required, get_jwt_identity   
import datetime
#jwt = JWT(app, models.User.authenticate, models.User.identity)
jwtManager = JWTManager(app)


#       **** Routes / Controllers ****



#       **** User Routes / Controllers ****
# Register Route
@app.route('/users/register', methods=['POST'])
def register():
    # Requesting JSON from request and using get_json() to parse it to a python Dict
    req = request.get_json()
    # Calling the saveUser() from the User model and passing it the python Dict. The response of createUser() is assigned to response
    response = models.User.saveUser(req)
    # Changing python Dict from response using Jsonify and return JSON response ot client
    return make_response(jsonify(response), response['status'])

# Login route
@app.route('/users/login', methods=['POST'])
def login():
    # Requesting JSON from request and using get_json() to parse it to a python Dict
    req = request.get_json()
   
    # Calling the saveUser() from the User model and passing it the python Dict. The response of createUser() is assigned to response
    response = models.User.authenticate(req)
     # Changing python Dict from response using Jsonify and return JSON response ot client
  
    return make_response(jsonify(response), response['status'])


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
def connect():
    sid = request.sid
    print(f"User {sid} connected")

# This function takes in message, assigns message from user to user_message. Sends the user_message to chatbot model. 
# Creates datetime object to get current datetime and convert to a string. Create res object. 
# This object will be saved to the db and sent to user. Pause the for 0.3 seconds to create the illusion that 
# the chatbot is thinking. Sends res object back to React Native application.
@socket.on('msg_from_react')
def message_sent(message):
    sid = request.sid
    user_message = message['message'] 
    amicaResponse = chatbot.chat(user_message)
    user = get_jwt_identity()
    print(user)
    dateTimeObj = datetime.datetime.today()
    timestampStr = dateTimeObj.strftime("%H:%M:%S.%f - %b %d %Y")
    res = {
       
        "msg": amicaResponse['response'],
        "msgAuthor": "amica",
        "timestamp": timestampStr,
        "context": amicaResponse['context']
    }
    #chat_log.Chat_log.saveMessage(res)
    print(res)
    socket.sleep(0.3)
    socket.emit("msg_from_flask", res, to=sid)

@socket.event
def disconnect(sid):
    sid = request.sid
    print(f"User {sid} disconnected")
