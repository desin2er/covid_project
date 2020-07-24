# COVID-19 Project


주제
* 펭수 로봇의 카메라를 이용하여 사람을 찰영하여 체온을 측정, 분석하는 로봇 개발

팀 역할
* 로봇 , 카메라, 열상카메라 등을 이용하여 

개발 환경
* Raspbarry pi 3, 4
* 언어 : python, kivy
##
#### Tkinter
![](/images/tk0.png)
얼굴 인식 코드
```
class Func_Class:
#https://github.com/opencv/opencv/tree/master/data/haarcascades xml페이지 - 라이브러리  
###카메라 관련 처리######################################    
    def cam_init(cls):#카메라 관련 초기화
        Func_Class.cap = cv2.VideoCapture(0)
        Func_Class.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 450)
        Func_Class.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)
        Func_Class.detector = dlib.get_frontal_face_detector()
        # 얼굴 인식용 클래스 생성 (기본 제공되는 얼굴 인식 모델 사용)
        Func_Class.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        # 인식된 얼굴에서 랜드마크 찾기위한 클래스 생성 
    cam_init = classmethod(cam_init)     
    def off_show(cls):
        cv2.VideoCapture(0, cv2.CAP_DSHOW)
    off_show = classmethod(off_show)
    #카메라 컬러 출력 
    def live_show(self):              
        _, frame = Func_Class.cap.read()            
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk
    # 카메라 이진화 변경
    def live_black(self): 
        _, frame = Func_Class.cap.read()            
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)#gray test
        ret, dst = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)#gray test
        img = PIL.Image.fromarray(dst)#gray test
        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk
    def face_search(self):
        ret, img_frame = Func_Class.cap.read()
        #캠 이미지를 frame으로 자른다.
        
        img_gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)
        #이미지를 그래이 스케일로 변환
        dets = Func_Class.detector(img_gray, 1)
        ALL = list(range(0, 68)) 
        RIGHT_EYEBROW = list(range(17, 22))  
        LEFT_EYEBROW = list(range(22, 27))  
        RIGHT_EYE = list(range(36, 42))  
        LEFT_EYE = list(range(42, 48))  
        NOSE = list(range(27, 36))  
        MOUTH_OUTLINE = list(range(48, 61))  
        MOUTH_INNER = list(range(61, 68)) 
        JAWLINE = list(range(0, 17))
        index = ALL
        for face in dets:
            shape = Func_Class.predictor(img_frame, face) #얼굴에서 68개 점 찾기
            list_points = []
            for p in shape.parts():
                list_points.append([p.x, p.y])
            list_points = np.array(list_points)#배열형태로 바꾸어준다.

            for i,pt in enumerate(list_points[index]):#각 지정한 포인트에 맞게 랜드마크 점을 찾는다(밑에서 찾을 것을 지정해줌)
                pt_pos = (pt[0], pt[1])
                cv2.circle(img_frame, pt_pos, 1, (0, 255, 0), -1)
            cv2.rectangle(img_frame, (face.left(), face.top()), (face.right(), face.bottom()),
                (0, 0, 255), 2)
        cv2image = cv2.cvtColor(img_frame, cv2.COLOR_BGR2RGBA)#color 배열 변경
        img = PIL.Image.fromarray(cv2image)#
        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk
```

#### kivy
![](/images/main0.png)
![](/images/music0.png)
![](/images/setting0.png)
#### 얼굴 인식, 라즈베리파이에서 실행한 결과
![](/images/face0.jpg)

#### 얼굴 인식, 라즈베리파이에서 실행한 결과
![](/images/ps_image1.jpg)

