import os
import cv2
import time
from PIL import Image
import numpy as np
import glob
from static.bin.python_facedars_master.base_camera import BaseCamera


class Camera2(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera2.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera2, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera2.video_source = source

    @staticmethod
    def frames():
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # set video width
        cam.set(4, 480)  # set video height

        face_detector = cv2.CascadeClassifier(
            'static/bin/flask_video_streaming_master/FacialRecognitionProject/haarcascade_frontalface_default.xml')

        # For each person, enter one numeric face id

        list_of_files = glob.glob(
            'static/bin/flask_video_streaming_master/FacialRecognitionProject/dataset/*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime).split('.')
        face_id = str(int(latest_file[1]) + 1)

        # Initialize individual sampling face count
        count = 0

        while (True):
            ret, img = cam.read()
            yield cv2.imencode('.jpg', img)[1].tobytes()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                time.sleep(0.2)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite("static/bin/flask_video_streaming_master/FacialRecognitionProject/dataset/User." + str(
                    face_id) + '.' + str(count) + ".jpg",
                            gray[y:y + h, x:x + w])

                yield cv2.imencode('.jpg', img)[1].tobytes()

            k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30:  # Take 30 face sample and stop video
                break

        # Do a bit of cleanup
        cam.release()
        cv2.destroyAllWindows()

        # Path for face image database
        path = 'static/bin/flask_video_streaming_master/FacialRecognitionProject/dataset'

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(
            "static/bin/flask_video_streaming_master/FacialRecognitionProject/haarcascade_frontalface_default.xml")

        # function to get the images and label data
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
                img_numpy = np.array(PIL_img, 'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(id)
            return faceSamples, ids

        faces, ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.write(
            'static/bin/flask_video_streaming_master/FacialRecognitionProject/trainer/trainer.yml')  # recognizer.save() worked on Mac, but not on Pi
