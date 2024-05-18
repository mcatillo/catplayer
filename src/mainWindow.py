#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html

Class with the main window of the application

'''

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6 import QtGui
import sys
import os
import json
import datetime
from src.videoplayer import VideoPlayer
from src.header import Header
from src.language import SelectLanguage
from src.mvars import *

#fmt = 'svg' if sys.platform=="linux" or sys.platform=="linux2" else "png"
fmt = "png"
keyListConfig = ["os","open_date","close_date","volume","folder","num_videos_opened"]

class MainWindow(QMainWindow):
    '''Main window of of the video app
    
    Attributes:
        arg (str): file video/music to open
        config (dict): dictionary of the previous configuration
        language (Language): variable of type class Language in src/language.py 
            containing the dictionary
    
    '''
    def __init__(self,arg,config,language,path):
        '''Class initialization
        
        Parameters:
            arg (str): file video/music to open
            config (dict): dictionary of the previous configuration
            language (Language): variable of type class Language in src/language.py 
                containing the dictionary
        '''
        super().__init__()
        self.setWindowTitle('catplayer')
        self.layout = QVBoxLayout()
        self.arg = arg
        self.lang = language
        self.path = path
        self.old_config = config
        self.new_config()

        self.header = Header(self.arg,self.lang)
        self.video_widget = VideoPlayer(self.arg,self.new_config,self.lang,self.path)
        self.video_widget.screen_regulator.clicked.connect(self.__toogleFullScreen)
        self.video_widget.exit_button.clicked.connect(self.close)

        self.layout.addWidget(self.header)
        self._createActions()
        self._createMenuBar()
        self._conenctAction()
        font = QFont()
        font.setPointSize(FONT_SIZE)
        self.setFont(font)

        self.layout.addWidget(self.video_widget)
        self.setWindowIcon(QtGui.QIcon(self.path.expand("logo",'data','logo','catplayer_128x128.ico')))

        # Set margins around the app to zero
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        # Define the whole as a widget to put centrally
        self.mw = QWidget()
        self.mw.setLayout(self.layout)
        self.setCentralWidget(self.mw)

    def __toogleFullScreen(self):
        '''Function for expand or reduce app view'''
        if self.isFullScreen():
            self.showNormal()
            self.video_widget.screen_regulator.setIcon(self.path.expand("r_files",'data','media',f'full_screen.{fmt}'))
            self.menuBar.show()
            self.header.show()
        else:
            self.showFullScreen()
            self.video_widget.screen_regulator.setIcon(QtGui.QIcon(self.path.expand("r_files",'data','media',f'normal_screen.{fmt}')))
            self.video_widget.screen_regulator.setToolTip(self.lang.fromKey("reduce"))
            self.menuBar.hide()
            self.header.hide()

    def _createActions(self):
        '''Create the actions for the menu bar'''
        self.openAction = QAction(self.lang.fromKey('open'), self)
        self.openAction.setShortcuts(QKeySequence.Open)
        self.openAction.setStatusTip(self.lang.fromKey("opennewvideo"))

        self.langAction = QAction(self.lang.fromKey("language"), self)
        self.langAction.setShortcuts(QKeySequence(Qt.CTRL | Qt.Key_L))
        self.langAction.setStatusTip(self.lang.fromKey("selectlanguage"))

        self.aboutAction = QAction(self.lang.fromKey("about"), self)
        self.aboutAction.setShortcuts(QKeySequence(Qt.CTRL | Qt.Key_A))
        self.aboutAction.setStatusTip(self.lang.fromKey("about"))

        self.exitAction = QAction(self.lang.fromKey("exit"), self)
        #self.exitAction.setShortcuts(QKeySequence(Qt.CTRL | Qt.Key_Q))
        self.exitAction.setShortcuts(QKeySequence.Cancel)
        self.exitAction.setStatusTip(self.lang.fromKey("exit"))
    
    def _createMenuBar(self):
        '''Create the menu bar buttons'''
        self.menuBar = self.menuBar()
        self.fileMenu = QMenu("&File",self)
        self.menuBar.addMenu(self.fileMenu)

        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.langAction)
        self.fileMenu.addAction(self.aboutAction)
        self.fileMenu.addAction(self.exitAction)

    def _conenctAction(self):
        '''Connect menu bar buttons to a specific action'''
        self.openAction.triggered.connect(self.dialog)
        self.exitAction.triggered.connect(self.close)
        self.langAction.triggered.connect(self.language)
        self.aboutAction.triggered.connect(self.about)

    def dialog(self):
        '''Create dialog window for selecting video/music to open'''
        dialog = QFileDialog(self)
        open_folder = os.path.expanduser("~") if self.new_config['folder']==0 else self.new_config['folder']
        filename = dialog.getOpenFileName(self,
                                          self.lang.fromKey("open_video"),
                                          open_folder,
                                          "Videos (*.mp4 *.mkv *.avi *.ts *.MOV);; Any files (*)"
                                          )
        try:
            if filename[0] != '':
                self.video_widget.stop()
                self.arg = filename[0]
                self.header.setHeaderTitle(self.arg)
                self.video_widget.arg = self.arg
                self.video_widget.mediaPlayer.MysetSource(self.arg)
                self.new_config['folder'] = os.path.dirname(filename[0])
                self.new_config['num_videos_opened'] += 1
            else:
                raise Exception(self.lang.fromKey('nofileselected'))
        except:
            pass
    def language(self):
        '''Select the language to use in the app from the configuration given'''
        w = SelectLanguage(self.lang,self.new_config)
        w.exec()
    
    def about(self):
        '''Window with license notes on the app'''
        w = QMessageBox(QMessageBox.Information,self.lang.fromKey("about"),
                        """
                        Copyright © 2024 Marco Catillo.\n
                        This software is distributed under the terms of 
                        the GNU General Public License v3 (GPLv3), 
                        https://www.gnu.org/licenses/gpl-3.0.html.
                        """)
        w.setStandardButtons(QMessageBox.Ok);
        w.exec()

    def new_config_init(self):
        '''Initialize the new configuration dictionary'''
        self.new_config = {}
        for k in keyListConfig:
            self.new_config[k] = 0

    def new_config(self):
        '''Set the new configuration dictionary'''
        self.new_config_init()
        for k,v in self.old_config.items():
            self.new_config[k] = v

        self.new_config['os'] = sys.platform
        self.new_config['open_date'] = datetime.datetime.today().ctime()
        self.new_config['close_date'] = 0
        self.new_config['num_videos_opened'] = 1 if self.arg else 0
        if type(self.new_config['folder']) == str:
            if self.new_config['folder'] != "":
                self.new_config['folder'] = 0 if self.new_config['folder'][0] != '/' else self.new_config['folder']
            else:
                self.new_config['folder'] = 0

    def closeEvent(self,event):
        '''Override the close event, saving the new configuration settings in a json file'''
        self.new_config['close_date'] = datetime.datetime.today().ctime()
        with open(self.path.expand('rw_files','config','config.json'),'w', encoding ='utf8') as f:
            json.dump(self.new_config,f, ensure_ascii = False)


