#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_opencv import Camera
    from camera_opencv2 import Camera2

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

name = ''


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        global name
        name = request.form['my_input']  # raises 400 error
    return render_template('index.html')


@app.route('/raspoznovanie')
def lox():
    """Video streaming home page."""
    return render_template('face_detected_real_time_raspozn.html')


@app.route('/dobavlenie')
def daun():
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
    file = open('FacialRecognitionProject/names.txt', 'a', encoding='utf-8')
    file.write(',' + name)
    file.close()
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera2()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
    app.run(threaded=True)
