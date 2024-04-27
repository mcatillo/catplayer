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
import json, os
import pprint as p
from datetime import datetime
from src.language import Language
from src.utils import path


def get_past_settings():
    ''' Get the past settings saved on the previous application usage

    Returns: 
        dict: dictionary of previous settings.
    '''
    with open(path('src','config','latest_config.json'),'r') as f:
        latest_config = json.load(f)
    return latest_config

def main(arg):
    '''Define the main window of the application
    
    Args:
        arg (str): file video or music to open
    '''
    
    app = QApplication(arg)
    arg = arg[1] if len(arg)>1 else None
    config = get_past_settings() # get previous configurations
    language = Language(config)


    window = MainWindow(arg,config,language)
    window.resize(854,540)
    window.show()
    app.exec()