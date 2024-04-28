#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html

In this python file we define the classes for playing the video/music.
    MediaPlayer -> class inherited by QMediaPlayer to be adapted for the functionalities of the app
    VideoPlayer -> 

'''

from PySide6.QtWidgets import *
from PySide6 import QtGui
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QAudio
from PySide6.QtMultimediaWidgets import QVideoWidget
import os
import sys
from src.utils import path

fmt = 'svg' if sys.platform=="linux" or sys.platform=="linux2" else "png"
dim = 28

class MediaPlayer(QMediaPlayer):
    '''Class for handling the video player'''
    def __init__(self):
        super().__init__()

        # Status bar widgets
        self.current_time = QLabel() # display the current time
        self.bar =  QSlider(Qt.Horizontal) # status bar time video
        self.total_time = QLabel() # total time 
        self.tot_time=("--:--:--",0)
        self.__default_button_style()
        self.slider_pressed = False
        self.slider_moving = False
        self.slider_changed = False
        self.sourceChanged.connect(self.source_changed)
        self.durationChanged.connect(self.__update_duration)
        self.positionChanged.connect(self.__update_position)

    def source_changed(self,media):
        '''Notify the media change and print the media location'''
        print(f"Media has been changed in {media}")

    def MysetSource(self,x):
        '''Set the new file source to be played
        
        Parameters:
            x (str): source file location
        '''
        self.thread().sleep(1)
        self.setSource(QUrl.fromLocalFile(x))
        self.__update_duration_check = False

    def __update_duration(self):
        '''Extract the duration of the video/music'''
        if not self.__update_duration_check:
            self.__update_duration_check = True
            self.tot_time = self.convertDuration(self.duration())
            self.total_time.setText(self.tot_time[0])
            self.total_time.repaint()

    def __slider_pressed(self):
        '''Set the new slider position'''
        self.slider_pressed = True
        ms_pos = int(self.tot_time[1]*(self.bar.value()/100.0))
        self.new_pos = self.convertDuration(ms_pos)
        self.current_time.setText(self.new_pos[0])
        self.current_time.repaint()
        self.setPosition(ms_pos)
    
    def __slider_moved(self,v):
        '''Notify that the slider has been moved and update the time
        
        Parameters:
            v (float): position of the slider as percentage 
        '''
        self.slider_moving = True
        ms_pos = int(self.tot_time[1]*(v/100.0))
        self.new_pos = self.convertDuration(ms_pos)
        self.current_time.setText(self.new_pos[0])
        self.current_time.repaint()

    def __slider_released(self):
        '''Set the new slider position'''
        ms_pos = int(self.tot_time[1]*(self.bar.value()/100.0))
        self.new_pos = self.convertDuration(ms_pos)
        self.current_time.setText(self.new_pos[0])
        self.current_time.repaint()
        self.setPosition(ms_pos)
        self.slider_pressed = False
        self.slider_moving = False

    def __slider_changed(self,v):
        '''Notify that slider has been changed by a large step
        
        Parameters:
            v (float): position of the slider as percentage 
        '''
        try:
            pos = 100*self.position()/self.tot_time[1]
            if abs(v - pos) > 9:
                self.slider_changed = True
            else:
                self.slider_changed = False
        except:
            pass

    def __update_position(self):
        '''Update position of the video and change the bar slider accordingly'''
        if not self.slider_moving: 
            if not self.slider_pressed:
                self.new_pos = self.convertDuration(self.position())
                self.current_time.setText(self.new_pos[0])
                self.current_time.repaint()
                if self.__update_duration_check:
                    if not self.slider_changed:
                        self.bar.setValue(100*self.new_pos[1]/self.tot_time[1])
                        self.bar.repaint()
                        self.slider_changed = False
                    else:
                        ms_pos = int(self.tot_time[1]*(self.bar.value()/100.0))
                        self.setPosition(ms_pos)
                        self.slider_changed = False

    def convertDuration(self,ms):
        '''Convert duration in milliseconds in hh:mm:ss notation
        
        Parameters:
            ms (float): duration in milliseconds
        '''
        stot = int(ms/1000.0)
        s = int(stot%60)
        m = int((stot - s)/60)%60
        h = int((stot - s - m*60)/(60*60))
        return (f"{h:02d}:{m:02d}:{s:02d}",ms)

    def __default_button_style(self):
        '''Setup styles of the buttons'''
        
        # self.current_time label
        self.current_time.setFixedHeight(dim)
        self.current_time.setFixedWidth(2*dim)
        self.current_time.setCursor(QCursor(Qt.IBeamCursor))
        self.current_time.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.current_time.setText("00:00:00")
        self.current_time.setToolTip("hh:mm:ss")

        # self.bar slider
        self.bar.setFixedHeight(dim)
        self.bar.setCursor(QCursor(Qt.PointingHandCursor))
        self.bar.setTickInterval(10)
        self.bar.setMinimum(0)
        self.bar.setMaximum(100)
        self.bar.setValue(0)
        self.bar.sliderReleased.connect(self.__slider_released)
        self.bar.sliderPressed.connect(self.__slider_pressed)
        self.bar.sliderMoved.connect(self.__slider_moved)
        self.bar.valueChanged.connect(self.__slider_changed)

        # self.total_time label
        self.total_time.setFixedHeight(dim)
        self.total_time.setFixedWidth(2*dim)
        self.total_time.setCursor(QCursor(Qt.IBeamCursor))
        self.total_time.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.total_time.setText(self.tot_time[0])
        self.total_time.setToolTip("hh:mm:ss")

class VideoPlayer(QWidget):
    '''Video widget of of the video app
    
    Attributes:
        arg (str): file video/music to open
        config (dict): dictionary of the current configuration
        language (Language): variable of type class Language in src/language.py 
            containing the dictionary
    
    '''
    def __init__(self,arg,config,language):
        '''Class initialization
        
        Parameters:
            arg (str): file video/music to open
            config (dict): dictionary of the current configuration
            language (Language): variable of type class Language in src/language.py 
                containing the dictionary
        '''
        super().__init__()
        self.arg = arg
        self.new_config = config
        self.lang = language
        
        # Main layout
        self.lvideo = QVBoxLayout()
        self.lbar = QHBoxLayout()
        self.lcontrol = QHBoxLayout()
        
        # Widget of the video
        self.videoWidget = QVideoWidget()
        self.audioOutput = QAudioOutput()
        self.mediaPlayer = MediaPlayer()
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.mediaStatusChanged.connect(self.__media_status_changed)
        self.check_mediaPlayer=False
        if self.arg:
            try:
                self.mediaPlayer.MysetSource(path(self.arg))
            except:
                pass

        # Default volume  
        self.audio_placeholder = self.new_config['volume']
        self.audioOutput.setVolume(apn(self.audio_placeholder))

        # Control button widgets
        self.player = QPushButton() # play/pause button
        self.restarter = QPushButton() # restart from the beginning button
        self.screen_regulator = QPushButton() # full/normal screen video size
        self.exit_button = QPushButton()
        self.audioplay = QPushButton() # activate or deactivate audio
        self.audiolabel = QLabel()
        self.setaudio = QSlider(Qt.Horizontal) # audio slider
        self.fillempty = QLabel() # empty widget
        self.__default_button_style()

        # Put all buttons into self.lcontrol layout
        self.lcontrol.addWidget(self.player)
        self.lcontrol.addWidget(self.mediaPlayer.current_time)
        self.lcontrol.addWidget(self.mediaPlayer.bar)
        self.lcontrol.addWidget(self.mediaPlayer.total_time)
        self.lcontrol.addWidget(self.restarter)
        self.lcontrol.addWidget(self.audioplay)
        self.lcontrol.addWidget(self.setaudio)
        self.lcontrol.addWidget(self.audiolabel)
        #self.lcontrol.addWidget(self.fillempty)
        self.lcontrol.addWidget(self.exit_button)
        self.lcontrol.addWidget(self.screen_regulator)

        # Structure of layout
        self.lvideo.addWidget(self.videoWidget)
        #self.lvideo.addLayout(self.lbar)
        self.lvideo.addLayout(self.lcontrol)
        self.setLayout(self.lvideo)

    def __default_button_style(self):
        '''Setup styles of the buttons'''

        # self.player button
        self.player.setFixedHeight(dim)
        self.player.setFixedWidth(dim)
        self.player.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.player.clicked.connect(self.play)
        self.player.setCursor(QCursor(Qt.PointingHandCursor))
        self.player.setToolTip(self.lang.fromKey("play1"))

        # self.restarter button
        self.restarter.setFixedHeight(dim)
        self.restarter.setFixedWidth(dim)
        self.restarter.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.restarter.setCursor(QCursor(Qt.PointingHandCursor))
        self.restarter.clicked.connect(self.stop)
        self.restarter.setToolTip(self.lang.fromKey("stop"))

        # self.screen_regulator button
        self.screen_regulator.setFixedHeight(dim)
        self.screen_regulator.setFixedWidth(dim)
        self.screen_regulator.setIcon(QtGui.QIcon(path('src','media',f'full_screen.{fmt}')))
        self.screen_regulator.setCursor(QCursor(Qt.PointingHandCursor))
        self.screen_regulator.setToolTip(self.lang.fromKey("expand"))

        # self.exit_button button
        self.exit_button.setFixedHeight(dim)
        self.exit_button.setFixedWidth(dim)
        self.exit_button.setIcon(QtGui.QIcon(path('src','media',f'exit.{fmt}')))
        self.exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.exit_button.setToolTip(self.lang.fromKey("exit"))

        # self.audioplay button for audio on/off
        self.audioplay.setFixedHeight(dim)
        self.audioplay.setFixedWidth(dim)
        self.audioplay.setIcon(QtGui.QIcon(path('src','media',f'audio_max.{fmt}')))
        self.audioplay.setCursor(QCursor(Qt.PointingHandCursor))
        self.audioplay.clicked.connect(self.__volume)
        self.audioplay.setToolTip(self.lang.fromKey("audioacceso"))

        self.audiolabel.setFixedHeight(dim)
        self.audiolabel.setFixedWidth(4*dim)
        self.audiolabel.setCursor(QCursor(Qt.IBeamCursor))
        self.audiolabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.audiolabel.setText(f"{self.audio_placeholder}%")
        self.audiolabel.setToolTip(f"{self.audio_placeholder}%")

        # self.setaudio slider
        self.setaudio.setFixedHeight(dim)
        self.setaudio.setFixedWidth(100)
        self.setaudio.setCursor(QCursor(Qt.PointingHandCursor))
        self.setaudio.setMinimum(0)
        self.setaudio.setMaximum(100)
        self.setaudio.setTickInterval(10)
        self.setaudio.setValue(self.audio_placeholder)
        self.setaudio.valueChanged.connect(self.__volumebar)

    def play(self):
        '''Take care of the play event, when play button is clicked'''
        if self.check_mediaPlayer:
            self.check_mediaPlayer = False
            self.mediaPlayer.pause()
            self.player.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.player.setToolTip(self.lang.fromKey("play1"))
        else:
            self.check_mediaPlayer = True
            self.mediaPlayer.play()
            self.player.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.player.setToolTip(self.lang.fromKey("pause"))

    def stop(self):
        '''Take care of the stop event, when stop button is clicked 
        or new source file has been chosen'''

        self.check_mediaPlayer = False
        #if self.mediaPlayer.isPlaying():
        self.mediaPlayer.stop()
        self.player.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay)) 

    def __volume(self):
        '''Setup volume'''
        if self.audioOutput.volume():
            self.audioplay.setIcon(QtGui.QIcon(path('src','media',f'audio_min.{fmt}')))
            self.audioplay.setToolTip(self.lang.fromKey("audiospento"))
            self.audioOutput.setVolume(0)
            self.setaudio.setValue(0)
            self.new_config['volume'] = 0
        else:
            self.audioplay.setIcon(QtGui.QIcon(path('src','media',f'audio_max.{fmt}')))
            self.audioplay.setToolTip(self.lang.fromKey("audioacceso"))
            if self.audio_placeholder:
                self.audioOutput.setVolume(apn(self.audio_placeholder))
                self.setaudio.setValue(self.audio_placeholder)
            else:
                self.audioOutput.setVolume(50)
                self.setaudio.setValue(50)
            self.setaudio.setValue(self.audio_placeholder)

    def __volumebar(self):
        '''Setup the bar of the volume'''
        self.audio_placeholder = self.setaudio.value()
        self.audiolabel.setText(f"{self.audio_placeholder}%")
        self.audiolabel.setToolTip(f"{self.audio_placeholder}%")
        
        self.audioOutput.setVolume(apn(self.audio_placeholder))
        self.new_config['volume'] = self.audio_placeholder
        if self.audio_placeholder:
            self.audioplay.setIcon(QtGui.QIcon(path('src','media',f'audio_max.{fmt}')))
            self.audioplay.setToolTip(self.lang.fromKey("audioacceso"))
        else:
            self.audioplay.setIcon(QtGui.QIcon(path('src','media',f'audio_min.{fmt}')))
            self.audioplay.setToolTip(self.lang.fromKey("audiospento"))
    
    def __media_status_changed(self,v):
        '''Function to stop media, when reached its end'''
        if v == QMediaPlayer.EndOfMedia:
            self.mediaPlayer.setPosition(0)
            self.stop()
def apn(pl):
    '''Volume conversion from linear to cubic scale'''
    linear_volume = QAudio.convertVolume(pl/100,
                                            QAudio.CubicVolumeScale,
                                            QAudio.LinearVolumeScale)
    return linear_volume*100
