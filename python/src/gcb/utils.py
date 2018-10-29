'''
Created on Apr 6, 2018

@author: lizhen
'''

import os
import logging
import pandas as pd 
import tempfile
import shutil
import time
import sys
import subprocess


def file_exists(file_path):
    return os.path.exists(file_path)


def create_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def remove_if_file_exit(fname, is_dir=False):
    if os.path.exists(fname):
        if is_dir: 
            shutil.rmtree(fname) 
        else:
            os.remove(fname)
        
            
def basename(path):        
    return os.path.basename(path)


def touch(filepath):
    with open(filepath, 'a'):
        os.utime(filepath, None)


_LOGGERS = {}


def get_logger(name):
    if name not in _LOGGERS:
        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        logger.addHandler(ch)
        _LOGGERS[name] = logger 
    return _LOGGERS[name]


class TempDir():

    def __init__(self):
        self.dirpath = None  
        
    def __enter__(self):
        self.dirpath = tempfile.mkdtemp()
        return self.dirpath

    def __exit__(self, type, value, traceback):
        if self.dirpath is not None:
            shutil.rmtree(self.dirpath)

        
def shell_run_and_wait(command, working_dir=None):
    curr_dir = os.getcwd()
    if working_dir is not None:
        os.chdir(working_dir)
    command = command.split(" ")
    import subprocess
    # process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process = subprocess.Popen(command)
    process.wait()
    if working_dir is not None:
        os.chdir(curr_dir)
    return process.returncode


def timeit(fun):
    t0 = time.time()
    ret = fun()
    t1 = time.time()
    return t1 - t0, ret

def pandas_show_all(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)  

def urlretrieve(src,dst):
    if sys.version_info[0] >= 3:
        from urllib.request import urlretrieve
    else:
        # Not Python 3 - today, it is most likely to be Python 2
        # But note that this might need an update when Python 4
        # might be around one day
        from urllib import urlretrieve
    return urlretrieve(src, dst)

def check_output(lst):
    if sys.version_info[0] >= 3:
        return subprocess.getoutput((" ".join (lst)))
    else:
        return subprocess.check_output(lst)        



