'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html

Functions for managing path across different operating systems

'''

import os
import sys

def lpath(*arg):
    '''Return os.path.join of a serie of strings
    
    Args:
        *args (str ellipsis): list of strings
    Returns
        str: path
    '''
    relative = os.path.join(*arg)
    return relative

def Rpath(*arg):
    '''Return a path based on the operating system 
    and check if the path is readable

    Args:
        *args (str ellipsis): list of strings
    Returns
        str: path
    '''
    homepath = os.path.expanduser('~')
    if sys.platform=="linux" or sys.platform=="linux2":
        local = lpath(*arg)
        gp = os.path.join('/','usr','share','catplayer',*arg)
        if os.path.exists(local) and os.access(local,os.R_OK):
            return local
        elif os.path.exists(gp) and os.access(gp,os.R_OK):
            return gp
        else:
            raise Exception(f"Path {gp} not found or not readable")

    elif sys.platform=='win32':
        local = lpath(*arg)
        r = os.path.join(os.environ['PROGRAMFILES(X86)'],'mcatillo','catplayer',*arg)
        if os.path.exists(local) and os.access(local,os.R_OK):
            return lpath(*arg)
        elif os.path.exists(r) and os.access(r,os.R_OK):
            return lpath(r,*arg)
        else:
            raise Exception(f"Path {lp} not found or not readable")
    else:
        return lpath(*arg)

def RWpath(*arg):
    '''Return a path based on the operating system 
    and check if the path is readable and writable

    Args:
        *args (str ellipsis): list of strings
    Returns
        str: path
    '''
    homepath = os.path.expanduser('~')
    if sys.platform=="linux" or sys.platform=="linux2":
        local = lpath(*arg)
        lp = os.path.join(homepath,'.config','catplayer',*arg)
        if os.path.exists(local) and os.access(local,os.R_OK) and os.access(local,os.W_OK):
            return local
        elif os.path.exists(lp) and os.access(lp,os.R_OK) and os.access(lp,os.W_OK):
            return lp
        else:
            raise Exception(f"Path {lp} not found or not readable or not writable")

    elif sys.platform=='win32':
        local = lpath(*arg)
        w = os.path.join(os.environ['LOCALAPPDATA'],'mcatillo','catplayer',*arg)
        if os.path.exists(local) and os.access(local,os.R_OK) and os.access(local,os.W_OK):
            return lpath(*arg)
        elif os.path.exists(w) and os.access(w,os.R_OK) and os.access(w,os.W_OK):
            return lpath(w,*arg)
        else:
            raise Exception(f"Path {lp} not found or not readable or not writable")
    else:
        return lpath(*arg)

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

        if os.path.exists(lp) and os.access(lp,os.R_OK):
            return lp
        elif os.path.exists(gp) and os.access(gp,os.R_OK):
            return gp
        else:
            rp = lpath(*arg)
            return rp

    elif sys.platform=='win32':
        r = os.path.join(os.environ['PROGRAMFILES(X86)'],'mcatillo','catplayer',*arg)
        if os.path.exists(r) and os.access(r,os.R_OK):
            return lpath(r,*arg)
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
