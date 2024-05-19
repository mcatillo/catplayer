#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html

Entry point of the application

'''

__author__ = "Marco Catillo"
__version__ = "0.0.0"
__maintainer__ = "Marco Catillo"
__status__ = "Production"

from src.main import main
import argparse
import sys
import os
from src.setup import *


parser = argparse.ArgumentParser(description='Basic video/music player app.',prog='catplayer')
parser.add_argument('filename',default=None,nargs='?',help='Video/Music input file')

class ParseArgs:
    def __init__(self,parser):
        self.parser=parser
        self.list = sys.argv
  
if __name__ == "__main__":
    arg = parser.parse_args() # file video/music to open
    arg = ParseArgs(parser.parse_args())
    arg.parser.filename = arg.parser.filename if len(arg.list)>1 else None
    main(arg)
