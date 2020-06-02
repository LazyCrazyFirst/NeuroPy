from flask import Flask, Response, redirect, request, url_for, render_template, jsonify
from flask_socketio import SocketIO, emit
import time
import os
import requests
from static.bin.voice.voice_assistant2 import anya
from static.bin.send_email.send_email import send_email

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

anyachka = ''
k = ''


# потоковая передача
@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            global k
            if anyachka != k:
                yield 'data: %s\n\n' % (anyachka)
                k = anyachka

        return Response(events(), content_type='text/event-stream')
    return render_template('index.html')


# получение данных от js
@socketio.on("submit vote")
def yes(data):
    # переводим в нужную кодировку и ставим нижний регистр, также убирпем запятые
    selection = data["selection"].encode('iso-8859-1').decode('utf8')
    selection = str(selection).lower().replace(",", "")
    global anyachka
    anyachka = anya(selection)


@socketio.on("send email")
def yes(data):
    # переводим в нужную кодировку и ставим нижний регистр, также убирпем запятые
    selection = data["selection"]
    name_value = selection['name_value']
    mail_value = selection['mail_value']
    subject_value = selection['subject_value']
    message_value = selection['message_value']
    send_email(name_value, mail_value, subject_value, message_value)