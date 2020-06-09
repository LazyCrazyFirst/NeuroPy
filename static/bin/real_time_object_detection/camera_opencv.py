import os
import cv2
from static.bin.python_facedars_master.base_camera import BaseCamera
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import cv2


class Camera5(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera5.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera5, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera5.video_source = source

    @staticmethod
    def frames():
        # инициализировать список меток классов MobileNet SSD был обучен
        # обнаружить, а затем создать набор цветов ограничивающего прямоугольника для каждого класса
        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                   "sofa", "train", "tvmonitor"]
        COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

        # загрузить нашу сериализованную модель с диска
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(
            "static/bin/real_time_object_detection/object_detection/MobileNetSSD_deploy.prototxt.txt",
            "static/bin/real_time_object_detection/object_detection/MobileNetSSD_deploy.caffemodel")

        # инициализировать потоковое видео, позволяют датчик cammera для прогрева,
        # и инициализировать счетчик кадров в секунду
        print("[INFO] starting video stream...")
        vs = cv2.VideoCapture(0)
        vs.set(3, 960)  # set video widht
        w = 960
        vs.set(4, 540)  # set video height
        h = 540

        # цикл по кадрам из видеопотока
        while True:
            # возьмите кадр из потокового видеопотока
            ret, frame = vs.read()

            # захватите размеры кадра и преобразуйте его в большой двоичный объект

            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                         0.007843, (300, 300), 127.5)

            # передайте большой двоичный объект через сеть и получите обнаружение и предсказание
            net.setInput(blob)
            detections = net.forward()

            # цикл по детекции
            for i in np.arange(0, detections.shape[2]):
                # извлеките уверенность (то есть вероятность), связанную с предсказанием
                confidence = detections[0, 0, i, 2]

                # отфильтруйте слабые обнаружения, убедившись, что "уверенность" больше, чем минимальная уверенность
                if confidence:
                    # извлеките индекс метки класса из ' detections`,
                    # затем вычислите (x, y)-координаты ограничивающего
                    # прямоугольника для объекта
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # нарисуйте предсказание на кадре
                    label = "{}: {:.2f}%".format(CLASSES[idx],
                                                 confidence * 100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                                  COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            # показать выходной кадр
            yield cv2.imencode('.jpg', frame)[1].tobytes()
            key = cv2.waitKey(1) & 0xFF

            # если клавиша " q " была нажата, выходите из цикла
            if key == ord("q"):
                break

        # сделайте небольшую уборку
        cv2.destroyAllWindows()
        vs.stop()
