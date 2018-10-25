'''
Created on Oct 23, 2018

@author: lizhen
'''

import os
import utils

if 'GCB_HOME' not in os.environ:
    HOME = os.path.join(os.environ['HOME'], '.gcb')
    utils.create_dir_if_not_exists(HOME)
else:
    HOME = os.environ['GCB_HOME']

assert HOME 

DATA_PATH = os.path.join(HOME, "data")

[utils.create_dir_if_not_exists(directory) for directory in [ DATA_PATH]]


def get_data_file_path(dsname, fname=""):
    dspath= os.path.join(DATA_PATH,dsname)
    utils.create_dir_if_not_exists(dspath)
    if fname:
        return os.path.join(dspath,fname)
    else:
        return dspath 



