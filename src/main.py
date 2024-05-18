#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html


Creating the main window of the application

'''

from PySide6.QtWidgets import *
from src.mainWindow import MainWindow
import json
from src.language import Language
from src.os_folder_system import Path
from src.mvars import *
from src.utils import get_past_settings
from src.setup import *

def main(arg):
    '''Define the main window of the application
    
    Args:
        arg (str): file video or music to open
    '''

    path = Path(INSTALLATION_TYPE,APP_OWNER,APP_NAME)
    config = get_past_settings(path) # get previous configurations
    language = Language(config,path)

    app = QApplication()

    window = MainWindow(arg,config,language,path)
    window.resize(WIN_SIZE[0],WIN_SIZE[1])
    window.show()
    app.exec()

