from flask import Flask, Response, redirect, request, url_for, render_template, jsonify
from flask_socketio import SocketIO, emit
import time
import os
import requests
from static.bin.voice.voice_assistant2 import anya
from static.bin.send_email.send_email import send_email
from importlib import import_module
import glob
import cv2
from static.bin.python_facedars_master.base_camera import BaseCamera

from static.bin.python_facedars_master.camera_opencv import Camera3
from static.bin.python_facedars_master.camera_opencv2 import Camera4

from static.bin.flask_video_streaming_master.camera_opencv import Camera
from static.bin.flask_video_streaming_master.camera_opencv2 import Camera2

from static.bin.real_time_object_detection.camera_opencv import Camera5

from static.bin.first_neiroset.neiroset import start

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

anyachka = ''
k = ''
name = ''
name2 = ''


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


@app.route('/theoryfrombook')
def theoryfrombook():
    return render_template('theoryfrombook.html')


@app.route('/theorymat')
def theorymat():
    return render_template('theorymat.html')


@app.route('/practicemat')
def practicemat():
    return render_template('practicemat.html')


@app.route('/face_detected_real_time', methods=['POST', 'GET'])
def face_detected_real_time():
    BaseCamera.stop()
    if request.method == 'POST':
        global name
        name = request.form['my_input']  # raises 400 error
    return render_template('face_detected_real_time.html')


@app.route('/face_detected_real_time_raspozn')
def face_detected_real_time_raspozn():
    """Video streaming home page."""
    return render_template('face_detected_real_time_raspozn.html')


@app.route('/face_detected_real_time_dobavl')
def face_detected_real_time_dobavl():
    """Video streaming home page."""
    return render_template('face_detected_real_time_dobavl.html')


# Для распознования
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Для добавления нового лица
@app.route('/video_feed2', methods=['POST', 'GET'])
def video_feed2():
    file = open('static/bin/flask_video_streaming_master/FacialRecognitionProject/names.txt', 'r',
                encoding='utf-8')
    names = file.read().split(',')
    file.close()

    k = 1

    for new_name in names:
        if name == new_name:
            print('kssa')
            k = 0

    if k == 1:
        file = open('static/bin/flask_video_streaming_master/FacialRecognitionProject/names.txt', 'a',
                    encoding='utf-8')
        file.write(',' + name)
        file.close()
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(gen(Camera2()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/object_detected')
def object_detected():
    BaseCamera.stop()
    return render_template('object_detected.html')


@app.route('/object_detected_real_time')
def object_detected_real_time():
    return render_template('object_detected_real_time.html')


@app.route('/video_feed3')
def video_feed3():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera5()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/face_detected_for_cam', methods=['POST', 'GET'])
def face_detected_for_cam():
    BaseCamera.stop()
    if request.method == 'POST':
        global name2
        name2 = request.form['my_input']
        file = open('static/bin/python_facedars_master/demo/people/new_name.txt', 'w', encoding='utf-8')
        file.write(name2)
        file.close()
    return render_template('face_detected_for_cam.html')


@app.route('/face_detected_for_cam_raspozn')
def face_detected_for_cam_raspozn():
    if request.headers.get('accept') == 'text/event-stream':
        def gen(camera):
            # Проверка того, не вышел ли ты со страницы
            camera.get_frame()

        return Response(gen(Camera3()), content_type='text/event-stream')

    return render_template('face_detected_for_cam_raspozn.html')


@app.route('/face_detected_for_cam_dobavl')
def face_detected_for_cam_dobavl():
    if request.headers.get('accept') == 'text/event-stream':
        try:
            def gen(camera):
                # Проверка того, не вышел ли ты со страницы
                camera.get_frame()

            list_of_files = glob.glob(
                'static/bin/python_facedars_master/demo/people/' + name2 + '/*')  # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getmtime).split('.')
            latest_file = str(latest_file[0]).split('(')[1].split(')')[0]

            if int(latest_file) < 23:
                return Response(gen(Camera4()), content_type='text/event-stream')
            else:
                print("Готово")
        except:
            return Response(gen(Camera4()), content_type='text/event-stream')

    return render_template('face_detected_for_cam_dobavl.html')


@app.route('/first_neiro', methods=['POST', 'GET'])
def first_neiro():
    if request.method == 'POST':
        print("DAUN")
        slov = start()
        ves1 = slov['Случайные инициализирующие веса:']
        ves2 = slov['Веса после обучения:']
        ves3 = slov['Результат после обучения:']
        return render_template('first_neiro.html', ves1=ves1, ves2=ves2, ves3=ves3)
    return render_template('first_neiro.html')