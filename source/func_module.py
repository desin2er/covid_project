# -*- coding: utf-8 -*-
from kivy.config import Config
# Config.set('graphics','width',100)
# Config.set('graphics','height',100)
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty,ObservableList
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.label import Label
#리스트 생성 관련
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.actionbar import ActionBar
import threading
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.modalview import ModalView
from kivy.graphics.texture import Texture
import numpy as np
from kivy.lang import Builder
import time
import server as sv
from MusicControl import *
import cv2

# from MainControl import *

Builder.load_file('./Switch.kv') 
global chk_vid
global chk_time
class CamLive(Image):
    def __init__(self, **kwargs):        
        super(CamLive,self).__init__(**kwargs)
        self.fps = 12 #카메라 프레임 설정
        self.sd = sv.SocketServer()
        Clock.schedule_interval(self.update,1.0/self.fps)
        self.chk = 0

       
    def update(self,dt):
        buf = ''
        emg_buf = ''
        buf = sv.SocketServer.img_kivy
        emg_buf = sv.SocketServer.emg_kivy
        if buf == '':
            pass
        else:
            # print(buf.shape)
            test = buf.tostring()
            
            # print('왜 안되니')
            textimg= Texture.create(size=(buf.shape[1], buf.shape[0]), colorfmt='rgba')
            textimg.blit_buffer(test, colorfmt='rgba', bufferfmt='ubyte')
            self.texture = textimg
        if emg_buf == '':
            pass
        else:
            print(sv.SocketServer.emg_kivy)
            w = WarningPopup()
            w.open()
            sv.SocketServer.emg_kivy = ''
class Tmpl_cam(Image):
    def __init__(self,**kwargs):
        super(Tmpl_cam,self).__init__(**kwargs)
        Clock.schedule_interval(self.update,1.0/12)
        self.sd = sv.SocketServer()
    def update(self,dt):
        buf = ''
        buf = sv.SocketServer.tmpl_kivy 
        if buf != '':            
            test = buf.tostring()       
            textimg= Texture.create(size=(buf.shape[1], buf.shape[0]), colorfmt='rgba')
            textimg.blit_buffer(test, colorfmt='rgba', bufferfmt='ubyte')
            self.texture = textimg

class StatusBar(ActionBar):
    pass
    

class ScreenMain(Screen):#main page
    
    def __init__(self, **kw):
        global chk_time
        global chk_vid
        chk_vid = 0
        super(ScreenMain,self).__init__(**kw)
        Clock.schedule_interval(self.vid_play, 10)
        chk_time = time.time()  
    def cam_p(self):#사진 찍기
        cam_pic = Picture_popup()
        cam_pic.open()
    def update_(self,dt):
        self.aa= self.im.update()
    def song_popup(self):#노래 리스트 팝업
        song_pop = SongPopup(SwitchApp.my_mix)
        song_pop.open()
    def on_touch_up(self, touch):
        global chk_time
        chk_time = time.time()
    def vid_play(self, dt):
        global chk_time
        global chk_vid
        if (time.time() - chk_time) > 30 and chk_vid == 0:
            c