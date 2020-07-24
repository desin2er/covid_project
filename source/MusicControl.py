import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty,ObservableList
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.label import Label

import os
from pygame import mixer
import pygame


class MyMusic:

    file_list = None
    file_list_w = None
    MUSIC_VOL = 0.5
    WAV_VOL = 1
    
    def __init__(self):
        ''' 초기화'''
        self.play_loop = 0  # 음악 반복 재생 정지: 0 , 반복실행 : 1
        self._m_index = 0   # 설정된 음악 인덱스
        self.music_len = 0  # 음악 리스트 갯수


        '''음악파일 list'''
        '''음악파일 .mp3 가져오기'''
        self.path_dir = os.path.dirname(os.path.realpath(__file__)) + '/music/' #mp3 root 위치 변수
        MyMusic.file_list = os.listdir(self.path_dir) #폴더내의 파일 list 생성
        self.music_len = len(MyMusic.file_list)
        MyMusic.file_list.sort() #리스트내 이름정렬
        print(MyMusic.file_list)
        ''' wav 파일 가져오기 '''
        MyMusic.path_dir_w = os.path.dirname(os.path.realpath(__file__)) + '/sound/' #wav
        MyMusic.file_list_w = os.listdir(MyMusic.path_dir_w)

        ''' mixer 설정 '''
        mixer.init()
        mixer.music.set_volume(MyMusic.MUSIC_VOL)   
        MyMusic.mx = mixer.Channel(1)  # .wav 파일 채널 설정
        MyMusic.mx.set_volume(MyMusic.WAV_VOL)

    '''음악 플레이 메인'''
    def music_play(self, index):
        """
        음악 재생
        """
        self._m_index = index
        self._play(self._m_index)
        self.clock_event1 = Clock.schedule_interval(self._loop_play,2)
        self.play_loop = 1


    def _loop_play(self,dt):
        ''' 음악 반복 재생 '''
        if mixer.music.get_busy() == 0 and self.play_loop:
            if self._m_index < self.music_len-1:
                print(self._m_index,self.music_len)
                self._m_index += 1
            else:
                self._m_index = 0
            self._play(self._m_index)

    ''' 인덱스된 음악 재생 '''
    def _play(self, index):
            
            mixer.music.load(self.path_dir + MyMusic.file_list[index])
            mixer.music.play()
            file_name = MyMusic.file_list[index]
            return file_name

    ''' 음악 정지 '''
    def music_stop(self):
        '''
        mix_stop( self ) \n
        mp3 음악 재생 정지 (재생 정지 및 반복 정지)
        '''
        print('cancel')
        self.clock_event1.cancel()
        self.play_loop = 0
        mixer.music.stop()

    def music_vol(vol):
        '''음악 파일 재생 볼륨 조절 0 ~ 1'''
        mixer.music.set_volume(vol)

    ''' wav 파일 재생 '''
    def wav_play(index = 0, loop = 0):
        """
        wav 파일 재생 할 때 사용
            def wav_play(index = 0, loop = 0):
            index = 0 실행할 목록번호
            loop = 반복 횟수(무한반복: -1)
        """
        file_name_w = MyMusic.file_list_w[index]
        MyMusic.mx_song = mixer.Sound(MyMusic.path_dir_w + file_name_w)
        MyMusic.mx.play(MyMusic.mx_song, loop)

    def wav_stop(self):
        '''wav 파일 재생 [정지] 시킴'''
        MyMusic.mx.stop()

    def wav_vol(vol):
        '''wav 파일 재생 볼륨 조절 0 ~ 1'''
        MyMusic.mx.set_volume(vol)

#------------------------------------------------------------------------#

'''J_coding'''
class SongPopup(Popup,ToggleButtonBehavior):
    my_music = MyMusic()
    '''song popup 창, 초기화'''
    rv = ObjectProperty()
    t_btn_text ='▶'
    play_tog = 0    # 재생:1 정지:0 상태
    play_index = 0  # 재생 할 index
    t_select = BooleanProperty(False)
    t_selectable = BooleanProperty(True)
    c_btn = ''
    def __init__(self, c_self, **kwargs):
        super().__init__(**kwargs)
        my_music = c_self
        SongPopup.c_btn = self.c_btn

    '''song popup 창에 플레이 버튼'''
    def btn_change(self, rv):
        if SongPopup.play