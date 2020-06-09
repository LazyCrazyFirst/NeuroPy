import os
import cv2
from static.bin.python_facedars_master.base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        file = open('static/bin/flask_video_streaming_master/FacialRecognitionProject/names.txt', 'r', encoding='utf-8')
        names = file.read().split(',')
        file.close()

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('static/bin/flask_video_streaming_master/FacialRecognitionProject/trainer/trainer.yml')
        cascadePath = "static/bin/flask_video_streaming_master/FacialRecognitionProject/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);

        font = cv2.FONT_HERSHEY_SIMPLEX

        # iniciate id counter
        id = 0

        # names related to ids: example ==> Marcelo: id=1,  etc

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 1200)  # set video widht
        cam.set(4, 480)  # set video height

        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Check if confidence is less them 100 ==> "0" is perfect match
                if (confidence < 100):
                    id = names[id - 1]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break

        # Do a bit of cleanup
        cam.release()
        cv2.destroyAllWindows()

