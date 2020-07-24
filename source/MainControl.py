import RPi.GPIO as GPIO  
import time
import threading
import numpy as np

GPIO.setmode(GPIO.BCM)
# GPIO.cleanup()

def close_GPIO():
    GPIO.cleanup()

class SonicCtrl:
    '''<초음파센서 컨트롤 클래스>
            out_pin : 출력 GPIO 번호
            in_pin : 입력 GPIO 번호
            
        사용 자원
            sonic_val : 초음파 센서 측정 값 150 ~ 10
            start() : 초음파 센석 측정 시작
            stop() : 초음파 센서 측정 종료
            
    '''
    def __init__(self, out_pin, in_pin):
        self.out_pin = out_pin
        self.in_pin = in_pin
        self.s_val = np.ones(20)*150 # 초음파 측정 최신값을 20개 저장
        self.sonic_val=150
        # self.start = time.time
        

        GPIO.setup(self.out_pin,GPIO.OUT)
        GPIO.setup(self.in_pin,GPIO.IN)

    def start(self):
        '''초음파 발생 설정'''
        GPIO.add_event_detect(self.in_pin, GPIO.FALLING, callback=self.get_val)
        self.sonic_wav()
    def sonic_wav(self):
        # print('wav')
        ''' 초음파 임펄스 발생 '''
        GPIO.output(self.out_pin,GPIO.HIGH)
        i = 5
        while i:
            i-= 1
        GPIO.output(self.out_pin,GPIO.LOW) 
        self.start = time.time()
        threading.Timer(0.03,self.sonic_wav).start()


    def get_val(self,dt):
        # print('get')
        '''입력핀에서 Falling 발생시 인터럽트으로부터 호출되어 측정 및 분석함 '''
        self.time_end = (time.time() - self.start) * 10000
        self.s_val = np.delete(self.s_val,0)
        self.s_val = np.append(self.s_val, int(self.time_end))
        self.sonic_val = np.mean(self.s_val)
        
        '''돌발 상황 발생시 처리 구역'''
        if self.sonic_val<40:
            
            MotorCtrl.control_Right(400,800)
            
            # print("위험")
            
        elif self.sonic_val>80:
            MotorCtrl.control_gb(1,500,500)
    def stop(self):
        ''' 초음파 종료 '''
        self.thr_wav.stop()
        GPIO.remove_event_detect(self.in_pin)

    def show(self):
        return self.sonic_val
        
class MotorPWM:
    '''pin(BOARD) : GPIO - 13(33), 16(36), 18(12), 19(37) '''
    def __init__(self, pin):
        
        self.pin = pin
        GPIO.setup(self.pin,GPIO.OUT)
        self.myPwm = GPIO.PWM(pin, 1)

    def start(self, f, duty=90):
        '''모터 제어'''
        self.myPwm.ChangeFrequency(f)
        self.myPwm.start(duty)

    def stop(self):
        self.myPwm.stop()

class MotorCtrl:
   
    # def __init__(self):
    GPIO.setup(5,GPIO.OUT)
    GPIO.setup(6,GPIO.OUT)
    GPIO.output(5,0)
    GPIO.output(6,0)
    pwm1 = MotorPWM(13)
    pwm2 = MotorPWM(19)
    l=SonicCtrl(27,22)
    r=SonicCtrl(17,4)

    def sensor_start():
        MotorCtrl.l.start()
        MotorCtrl.r.start()

    # def warning():
    #     # print('위위험')
    #     if MotorCtrl.r.sonic_val<40:
    #         print("오른쪽")
    #         MotorCtrl.control_Left(500,500)
        # elif MotorCtrl.l.sonic_val<40:
        #     MotorCtrl.control_Right(500,500)
        #     print("왼쪽")
        # elif MotorCtrl.l.sonic_val<40 and MotorCtrl.r.sonic_val<40:
        #     MotorCtrl.control_Stop()
        #     print("그만")
    def control_gb(dr, freq_R,freq_L):
        GPIO.output(5,dr)
        GPIO.output(6,dr)
        MotorCtrl.pwm1.start(freq_R)
        MotorCtrl.pwm2.start(freq_R)
    
    
    def control_Left(freq_R,freq_L):
        GPIO.output(5,0)
        GPIO.output(6,1)
        MotorCtrl.pwm1.start(freq_R)
        MotorCtrl.pwm2.start(freq_L)
   
    
    def control_Right(freq_R,freq_L):
        GPIO.output(5,1)
        GPIO.output(6,0)
        MotorCtrl.pwm1.start(freq_R)
        MotorCtrl.pwm2.start(freq_L)
        
    def control_Stop():
        MotorCtrl.pwm1.stop()
        MotorCtrl.pwm2.stop()
    