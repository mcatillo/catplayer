#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html


'''

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from src.language import *

class Header(QLabel):
    def __init__(self,arg,lang):
        super().__init__()
        self.lang = lang
        self.setHeaderTitle(arg)
        self.setFixedHeight(20)
        self.setAlignment(Qt.AlignHCenter)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(QCursor(Qt.IBeamCursor))

    def setHeaderTitle(self,arg):
        self.arg = arg if arg else self.lang.fromKey('nofileselected')
        self.setText(self.arg)
        self.setToolTip(self.arg)

