import os
import cv2
from static.bin.python_facedars_master.base_camera import BaseCamera
from mtcnn.mtcnn import MTCNN
import statistics
import numpy
import keras
import imutils
import datetime
import time


class Camera4(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera4.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera4, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera4.video_source = source

    @staticmethod
    def frames():
        # Создание сети нахождения лиц
        detector = MTCNN()

        # Загрузка модели сети определения лиц
        embedder = keras.models.load_model('static/bin/python_facedars_master/model/keras/facenet_keras.h5', compile=False)

        # Получить дистанцию лица
        def get_distance(model, face):
            face = face.astype('float32')
            face = (face - face.mean()) / face.std()
            face = numpy.expand_dims(face, axis=0)
            return embedder.predict(face)[0]

        '''
        Созданием базы с известными лицами
        '''

        base = {}
        file = open('static/bin/python_facedars_master/demo/people/names.txt', 'r', encoding='utf-8')
        names = file.read().split(',')
        file.close()

        for dirname in names:

            base[dirname] = []
            for file in os.listdir('static/bin/python_facedars_master/demo/people/' + dirname):

                if file.endswith('.jpg'):

                    # Загрузка изображения с лицом
                    image = cv2.imread('static/bin/python_facedars_master/demo/people/' + dirname + '/' + file)

                    # Получить размеры изображения
                    image_size = numpy.asarray(image.shape)[0:2]

                    # Получение списка лиц с координатами и значением уверенности
                    faces_boxes = detector.detect_faces(image)

                    # Работа с лицами
                    if faces_boxes:
                        # Координаты лица
                        x, y, w, h = faces_boxes[0]['box']

                        # Выравнивание лица
                        d = h - w  # Разница между высотой и шириной
                        w = w + d  # Делаем изображение квадратным
                        x = numpy.maximum(x - round(d / 2), 0)
                        x1 = numpy.maximum(x, 0)
                        y1 = numpy.maximum(y, 0)
                        x2 = numpy.minimum(x + w, image_size[1])
                        y2 = numpy.minimum(y + h, image_size[0])

                        # Получение картинки с лицом
                        cropped = image[y1:y2, x1:x2, :]

                        # Сохранение суммы евклидова пространства
                        base[dirname].append(get_distance(embedder, image))

        '''
        РАСПОЗНОВАНИЕ ЛИЦ
        '''

        def faces(name_new_face):

            # Загрузка фото
            frame = cv2.imread('static/bin/python_facedars_master/demo/recognition_video/input/objects.jpg')

            # Увеличение/уменьшение наименьшей стороны изображения до 1000 пикселей
            if frame.shape[0] < frame.shape[1]:
                frame = imutils.resize(frame, height=1000)
            else:
                frame = imutils.resize(frame, width=1000)

            # Получить размеры изображения
            image_size = numpy.asarray(frame.shape)[0:2]

            # Получение списка лиц с координатами и значением уверенности
            faces_boxes = detector.detect_faces(frame)

            # Копия изображения для рисования рамок на нём
            image_detected = frame.copy()

            # Замена BGR на RGB (так находит в два раза больше лиц)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Работа с лицами
            if faces_boxes:

                face_kol1 = 0

                for face_box in faces_boxes:

                    face_kol1 += 1

                    # Увеличение счётчика файлов
                    global face_n
                    face_n += 1

                    # Координаты лица
                    x, y, w, h = face_box['box']

                    # Выравнивание лица
                    d = h - w  # Разница между высотой и шириной
                    w = w + d  # Делаем изображение квадратным
                    x = numpy.maximum(x - round(d / 2), 0)
                    x1 = numpy.maximum(x, 0)
                    y1 = numpy.maximum(y, 0)
                    x2 = numpy.minimum(x + w, image_size[1])
                    y2 = numpy.minimum(y + h, image_size[0])

                    # Получение картинки с лицом
                    cropped = frame[y1:y2, x1:x2, :]
                    face_image = cv2.resize(cropped, (160, 160), interpolation=cv2.INTER_AREA)

                    # Координаты лица
                    x, y, w, h = face_box['box']

                    # Отступы для увеличения рамки
                    d = h - w  # Разница между высотой и шириной
                    w = w + d  # Делаем изображение квадратным
                    x = numpy.maximum(x - round(d / 2), 0)
                    x1 = numpy.maximum(x - round(w / 4), 0)
                    y1 = numpy.maximum(y - round(h / 4), 0)
                    x2 = numpy.minimum(x + w + round(w / 4), image_size[1])
                    y2 = numpy.minimum(y + h + round(h / 4), image_size[0])

                    # # Отборка лиц {selected|rejected}
                    if face_box['confidence'] > 0.80:  # 0.99 - уверенность сети в процентах что это лицо

                        cv2.putText(
                            image_detected,
                            'None',
                            (x1 + 10, y2 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            1
                        )

                        # Рисует красный квадрат на картинке по координатам
                        cv2.rectangle(
                            image_detected,
                            (x1, y1),
                            (x2, y2),
                            (0, 0, 255, 1),
                            1
                        )

                        # # Сохранение изображения нового лица
                        cv2.imwrite(
                            'static/bin/python_facedars_master/demo/people/' + name_new_face + '/' + '(' + str(face_n)
                            + ')' + '.jpg', face_image)

        '''
        Захват изображение с камеры
        '''

        global face_n
        face_n = 0

        file = open('static/bin/python_facedars_master/demo/people/new_name.txt', 'r', encoding='utf-8')
        name_new_face = file.read()
        file.close()

        os.mkdir("static/bin/python_facedars_master/demo/people/" + name_new_face)

        file = open('static/bin/python_facedars_master/demo/people/names.txt', 'a', encoding='utf-8')
        file.write(',' + name_new_face)
        file.close()

        # Включаем камеру
        cap = cv2.VideoCapture(0)

        while True:
            yield 'Fuuuu'  # Нужен yield, чтобы всё работало
            # Делаем снимок
            ret, cadr = cap.read()

            # Записываем в файл
            cv2.imwrite('static/bin/python_facedars_master/demo/recognition_video/input/objects.jpg', cadr)

            faces(name_new_face)
