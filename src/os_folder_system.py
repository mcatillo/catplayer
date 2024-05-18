import sys
import os
from os.path import join as p
import json
import datetime

class Path:
    def __init__(self,installation_type,prog_owner,prog_dir):
        self.installation_type = installation_type
        self.os = sys.platform
        self.prog_owner = prog_owner
        self.prog_dir = prog_dir
        self.user = os.environ['USER'] if self.os == "linux" else os.environ['USERNAME']

        self.blist = os.environ['PATH'].split(":")
        self.linux_local=f'/home/{self.user}/.local/bin'
        self.linux_global='/usr/bin'
        self.home = os.environ["HOME"] if self.os == "linux" else os.environ['HOMEPATH']
        self.local = os.path.abspath(".")
        self.setup_fs()
        self.create_rw_dirs()
        self.create_rw_files()


    def setup_fs(self):
        '''Setup the folders for a given filesystem

        We have three types of installation:
            1. global       => the application will be visible to all users in the system
            2. local         => the application will be visible only to a given user
            3. local_dir     => the program find the data in its source directory
        For each of them we categorize 5 types of files which go in these folders respectively:
            1. exe          => executable folder
            2. r_files      => read-only folders
            3. rw_files     => read-write folders
            4. logo         => folder containing the logo app
        '''
        if self.os == "win32":
            self.fs = {
                "global":{
                    "exe" : p(os.environ['PROGRAMFILES(X86)'],self.prog_owner,self.prog_dir),
                    "r_files": p(os.environ['PROGRAMFILES(X86)'],self.prog_owner,self.prog_dir),
                    "rw_files": p(os.environ['LOCALAPPDATA'],self.prog_owner,self.prog_dir),
                    "logo": p(os.environ['PROGRAMFILES(X86)'],self.prog_owner,self.prog_dir)
                },
                "local":{
                    "exe" : p(os.environ['LOCALAPPDATA'],'Programs',self.prog_owner,self.prog_dir),
                    "r_files": p(os.environ['LOCALAPPDATA'],self.prog_owner,self.prog_dir),
                    "rw_files": p(os.environ['LOCALAPPDATA'],self.prog_owner,self.prog_dir),
                    "logo": p(os.environ['LOCALAPPDATA'],self.prog_owner,self.prog_dir)
                    },
                "local_dir":{
                    "exe" : self.local,
                    "r_files": self.local,
                    "rw_files": self.local,
                    "logo": self.local,
                }
            }
        elif self.os == "linux":
            self.fs = {
                "global":{
                    "exe" : p(self.linux_global),
                    "r_files": p(self.linux_global,'..','share',self.prog_dir),
                    "rw_files": p(self.home,'.config',self.prog_dir),
                    "logo": p(self.linux_global,'..','share',self.prog_dir)
                },
                "local":{
                    "exe" : p(self.linux_local),
                    "r_files": p(self.linux_local,'..','share',self.prog_dir),
                    "rw_files": p(self.home,'.config',self.prog_dir),
                    "logo": p(self.linux_local,'..','share',self.prog_dir)
                },
                "local_dir":{
                    "exe" : self.local,
                    "r_files": self.local,
                    "rw_files": self.local,
                    "logo": self.local,
                }
            }
        else:
            raise Exception("Operating system not recognized")

    def expand(self,thetype,*arg):
        return p(self.fs[self.installation_type][thetype],*arg)
    
    def create_rw_dirs(self):
        if self.os == "linux":
            if self.installation_type == "global" or self.installation_type == "local_folder":

                self.config_folder = os.path.join(self.home,".config",self.prog_dir,"config")
                self.tmp_folder = os.path.join(self.home,".config",self.prog_dir,"tmp")
                self.prog_folder = os.path.join(self.home,".config",self.prog_dir)

                if not os.path.exists(self.prog_folder):
                    os.mkdir(self.prog_folder)
                if not os.path.exists(self.tmp_folder):
                    os.mkdir(self.tmp_folder)
                if not os.path.exists(self.config_folder):
                    os.mkdir(self.config_folder)
        elif self.os == "win32":
            if self.installation_type == "global" or self.installation_type == "local_folder":

                self.config_folder = p(os.environ['LOCALAPPDATA'],self.prog_owner,self.prog_dir,"config")
                self.tmp_folder = p(os.environ['LOCALAPPDATA'],self.prog_owner,self.prog_dir,"tmp")
                self.prog_folder = p(os.environ['LOCALAPPDATA'],self.prog_owner,self.prog_dir)
                self.prog_owner = p(os.environ['LOCALAPPDATA'],self.prog_owner)

                if not os.path.exists(self.prog_owner):
                    os.mkdir(self.prog_owner)
                if not os.path.exists(self.prog_folder):
                    os.mkdir(self.prog_folder)
                if not os.path.exists(self.tmp_folder):
                    os.mkdir(self.tmp_folder)
                if not os.path.exists(self.config_folder):
                    os.mkdir(self.config_folder)
        else:
            raise Exception(f"Error in {__file__}: operating system not recognized.")

    def create_rw_files(self):
        if self.os == "linux":
            if self.installation_type == "global" or self.installation_type == "local_folder":
                self.setup_config_json()
        elif self.os == "win32":
            if self.installation_type == "global" or self.installation_type == "local_folder":
                self.setup_config_json()
        else:
            raise Exception(f"Error in {__file__}: operating system not recognized.")

    def setup_config_json(self):
        config_json = {"os":self.os,
                       "open_date":datetime.datetime.today().ctime(),
                       "close_date":"",
                       "language":"en",
                       "num_videos_opened":0,
                       "volume":50,
                       "folder":os.path.abspath(".")}

        config_file = os.path.join(self.config_folder,"config.json")

        if not os.path.exists(config_file):
            with open(config_file,"w") as f:
                json.dump(config_json,f)





