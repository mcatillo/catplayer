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
import sys

if __name__ == "__main__":
    arg = sys.argv # file video/music to open
    main(arg)
