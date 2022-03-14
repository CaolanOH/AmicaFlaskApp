from flask import Flask
from flask_socketio import SocketIO
import socketio
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

socket = SocketIO(app, async_mode='eventlet')
from application import routes, chatbot

#from wsgi import app  # a Flask, Django, etc. application
#app = socketio.WSGIApp(sio, app)