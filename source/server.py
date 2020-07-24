import cv2
import numpy as np
# from kivy.graphics.texture import Texture
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow import keras
import PIL
from PIL import Image,ImageTk,ImageDraw,ImageFont
import time

class Cam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.face_classifier = cv2.CascadeClassifier('socket/haarcascade_frontalface_default.xml')
        self.m = self.create_model()
        self.m.load_weights('socket/cp_face.ckpt')
        self.name_class = ['반장님!~!ㅋㅋ','김영수','남상민','정효균']
        ## 0~100에서 90의 이미지 품질로 설정 (default = 95)
        Cam.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        
    def cam_live(self):
        # while 1:
        ret, frame = self.cap.read()
        
        if ret:
            
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #얼굴 찾기
            faces = self.face_classifier.detectMultiScale(gray_img,1.2,8)#1.3 스케일링, 5 : 가장가까운 이웃의수(숫자가 낮을수록 막찾는다.)
            copy_img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)
            
            for (x,y,w,h) in faces:
                # print(x,y,w,h)
                cv2.rectangle(frame,(x, y), (x+w, y+h),(255,0,0),2)
                ############tensor flow##################
                crop_img = gray_img[y:y + h, x:x + w] # 이미지 크롭
                re_img = cv2.resize(crop_img,dsize=(28,28),interpolation=cv2.INTER_LINEAR)#이미지 크기를줄인다.
                #imㅎ_blur = cv2.GaussianBlur(im,(5,5),0)#노이즈 제거를 위해 가오시안 블러처리 
                test_img = re_img/255
                train_img = test_img.reshape(1,28,28,1)
                prediction = self.m.predict(train_img)
                # print(prediction[0])
                n_predict = self.m.predict(train_img)
                num = (((n_predict[0,np.argmax(n_predict[0])]) * 1000)//1) # percent 출력
                try:
                    if (n_predict[0,np.argmax(n_predict[0])] * 100) > 80.0:
                        img_pil = Image.fromarray(frame)
                        draw = ImageDraw.Draw(img_pil)
                        text = self.name_class[np.argmax(n_predict[0])]
                        text = text +' : ' + str(num/10) + ' %'
                        draw.text((x - 10, y - 25), text, font = ImageFont.truetype(("socket/HiMelody-Regular.ttf"), 25), fill = (0, 255, 0, 0))
                        frame = np.array(img_pil)                        
                except Exception as e:
                    print('sksj')
            
            rt, buf_img = cv2.imencode('.jpg', frame, Cam.encode_param)#전송을 위해 이미지  엔코딩
            send_img = np.array(buf_img)#넘파이 배열로 변경
            
            stringData = send_img.tostring()#전송을 위한 String으로 변환(소켓에서전송 할때 byte 타입이어야함)
            
            # time.sleep(1/10)
            return  stringData

    def create_model(self):#학습 모델 만들기
        model = tf.keras.models.Sequential([
            #컨볼루션층
            tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1),padding='same'),#3x3필터(w)- kernel을 32개 적용 후 relu 활성함수를 걸쳐 출력(relu : 0보다 큰값은 원값, 0보다 작으면 0)
            # Conv2D(필터의 개수, kernel 사이즈, strides=kernel의 이동량, activation=활성함수,input shape = 입력 모양,padding=이미지의 테두리에 padding을 두른다.) #패턴을 찾아낸다.(입력값ㄴ)
            tf.keras.layers.MaxPooling2D((2,2),padding='same'),#2x2에서 가장 큰값만 나온다(압축)
            tf.keras.layers.Conv2D(64, (3,3), activation='relu',padding='same'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.MaxPooling2D((2,2),padding='same'),
            tf.keras.layers.Conv2D(128,(3,3), activation='relu'),
            #Flatten층
            tf.keras.layers.Flatten(),
            #선형회귀층
            tf.keras.layers.Dense(128,activation='relu'),        
            tf.keras.layers.Dense(10,activation='softmax')
        ])
        return model
