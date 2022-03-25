from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

socket = SocketIO(app, async_mode='eventlet')
from application import routes, chatbot
