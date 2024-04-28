import os
import sys

'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html

Functions for managing path across different operating systems

'''

def lpath(*arg):
    '''Return os.path.join of a serie of strings
    
    Args:
        *args (str ellipsis): list of strings
    Returns
        str: path
    '''
    relative = os.path.join(*arg)
    return relative

def path(*arg):
    '''Return a path based on the operating system
    Args:
        *args (str ellipsis): list of strings
    Returns
        str: path
    '''

    homepath = os.path.expanduser('~')

    if sys.platform=="linux" or sys.platform=="linux2":
        lp = os.path.join(homepath,'.local','share','catplayer',*arg)
        gp = os.path.join('/','usr','share','catplayer',*arg)

        if os.path.exists(lp) and os.access(lp,os.R_OK | os.W_OK):
            return lp
        elif os.path.exists(gp) and os.access(gp,os.R_OK | os.W_OK):
            return gp
        else:
            rp = lpath(*arg)
            return rp

    elif sys.platform=='win32':
        gp = "C:\\Program Files (x86)\\mcatillo\\catplayer"
        if os.path.exists(gp) and os.access(gp,os.R_OK | os.W_OK):
            return lpath(gp,*arg)
        else:
            return lpath(*arg)
    else:
        return lpath(*arg)

def gpath(*arg):
    '''Return absolute path
    
    Args:
        *args (str ellipsis): list of strings
    Returns
        str: pat
    '''
    relative = os.path.join(*arg)
    absolute = os.path.abspath(relative)
    return absolute
