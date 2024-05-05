#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

catplayer: app for video player

Copyright (C) 2024 Marco Catillo

Distribuited under GPLv3 license
https://www.gnu.org/licenses/gpl-3.0.html

In this python file we have two classes:
    Language -> for handling words to be translated with different languages
    SelectLanguage -> window for selecting a given language

'''

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6 import QtCore
import json
from src.utils import Rpath

class Language:
    '''This class handles words to be translated with different languages
    
    Attributes:
        config (dict): dictionary containing the current configuration
    '''
    def __init__(self,config):
        '''Class initialization

        Parameters:
            config (dict): dictionary containing the current configuration
        '''
        self.selected = 'en'
        self.config = config
        self.__take_language()
        self.select()

    def fromKey(self,key):
        '''Function for getting the word from its id (key)
        
        Parameters:
            key (str): id of a given word
        Returns:
            str: word of the correspective key
        '''
        try:
            word = self.data[key][self.selected]
        except:
            word = '--'
        return word
    
    def getKey(self,word):
        '''Function for getting the id (key) from a given word
        
        Parameters:
            word (str): word from which we want to get the id (key)
        Returns:
            str: id of word
        '''
        for k,v in self.data.items():
            for value in v.values():
                if value == word:
                    return k
        return 'id'

    def select(self,el=None):
        '''Function for seeting up self.select
        
        Parameters:
            el (str): language we want to select
        '''
        self.old_selected = self.selected
        if el is None:
            if "language" in self.config.keys():
                if self.config["language"] in self.list_languages:
                    self.selected = self.config["language"]
                else:
                    self.selected = self.list_languages[0]
            else:
                self.selected = None
        else:
            if el in self.list_languages:
                self.selected = el
            else:
                self.selected = None

    def __take_language(self):
        '''Read the word vocabulary and put it in self.data'''
        with open(Rpath('config','vocabulary.json'),"r") as f:
            self.data = json.load(f)
        self.list_languages = list(self.data[list(self.data)[0]].keys())

class SelectLanguage(QDialog):
    '''This class is for displaying the window for selecting a language
    
    Attributes:
        language (str): selected language to translate words
        config (dict): dictionary containing the current configuration
    '''
    def __init__(self,language,config):
        '''Class initialization
        
        Parameters:
            language (str): selected language to translate words
            config (dict): dictionary containing the current configuration
        '''
        super().__init__()
        self.language = language
        self.config = config

        self.setWindowTitle(self.language.fromKey("language"))
        self.setFixedWidth(180)
        self.setFixedHeight(160)

        main_layout = QVBoxLayout()
        list_layout = QVBoxLayout()
        for el in self.language.list_languages:
            w = self.button(el)
            list_layout.addWidget(w)

        self.decision()

        decision_layout = QHBoxLayout()
        decision_layout.addWidget(self.okay)
        decision_layout.addWidget(self.canc)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(decision_layout)

        self.setLayout(main_layout)

    def button(self,el):
        '''Button widget for selecting a language
        
        Parameters:
            el (str): selected language
        '''
        w = QPushButton()
        w.clicked.connect(lambda : self.__select(el))
        w.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        w.setText(self.language.fromKey(el))
        return w
    
    def decision(self):
        '''Define Ok and Cancel buttons for implementing the language changes or not'''
        self.okay = QDialogButtonBox(QDialogButtonBox.Ok)
        self.okay.setToolTip(self.language.fromKey("okaylingua"))
        self.okay.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.okay.clicked.connect(self.commit_language_changes)

        self.canc = QDialogButtonBox(QDialogButtonBox.Cancel)
        self.canc.setToolTip(self.language.fromKey("canclingua"))
        self.canc.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.canc.clicked.connect(self.back_previous_language)

    def back_previous_language(self):
        '''Function activated when button Canc is chosen'''
        self.language.select(self.language.old_selected)
        self.config["language"] = self.language.selected
        self.updateLanguage(self.language.old_selected)
        self.close()

    def commit_language_changes(self):
        '''Function activated when button Ok is chosen'''
        self.close()

    def __select(self,el):
        '''Select language el
        
        Parameters:
            el (str): selected language
        '''
        self.language.select(el)
        self.config["language"] = self.language.selected
        self.updateLanguage(el)

    def __update_widget(self,el):
        '''Update all widgets of the app with the new selected language
        
        Parameters:
            el (str): selected language
        '''
        list_methods = dir(type(el))
        ktxt = None
        ktip = None
        ktit = None
        if 'windowTitle' in list_methods:
            ktit = self.language.getKey(el.windowTitle())
        if 'setWindowTitle' in list_methods:
            if ktit!=None and ktit!='id':
                el.setWindowTitle(self.language.fromKey(ktit))
        if 'text' in list_methods:
            ktxt = self.language.getKey(el.text())
        if 'setText' in list_methods:
            if ktxt!=None and ktxt!='id':
                el.setText(self.language.fromKey(ktxt))
        if 'toolTip' in list_methods:
            ktip = self.language.getKey(el.toolTip())
        if 'setToolTip' in list_methods:
            if ktip!=None and ktip!='id':
                el.setToolTip(self.language.fromKey(ktip))
        if 'repaint' in list_methods:
            el.repaint()

    def updateLanguage(self,el):
        '''Update language
        
        Parameters:
            el (str): selected language
        '''
        all_widg = QApplication.allWidgets()
        for el in all_widg:
            self.__update_widget(el)
            children = el.findChildren(QAction)
            for child in children:
                self.__update_widget(child)


        


    
