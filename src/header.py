#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html

Description:
    class Header implemented

'''

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from src.language import *

class Header(QLabel):
    '''Class for path video on the top of the app

    Attributes:
        arg (str): file video/music to open
        lang (Language): variable of type class Language in src/language.py 
            containing the dictionary
    '''
    def __init__(self,arg,lang):
        '''Class initialization
        
        Parameters:
            arg (str): file video/music to open
            lang (Language): variable of type class Language in src/language.py 
                containing the dictionary
        '''
        super().__init__()
        self.lang = lang
        self.setHeaderTitle(arg)
        self.setFixedHeight(20)
        self.setAlignment(Qt.AlignHCenter)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(QCursor(Qt.IBeamCursor))

    def setHeaderTitle(self,arg):
        '''Set title of the header

        Parameters:
            arg (str): file video/music to open
        '''
        self.arg = arg if arg else self.lang.fromKey('nofileselected')
        self.setText(self.arg)
        self.setToolTip(self.arg)

