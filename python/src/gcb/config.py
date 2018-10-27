'''
Created on Oct 23, 2018

@author: lizhen
'''

import os
import utils

if 'GCB_DATA' not in os.environ:
    DATA_HOME = os.path.join(os.environ['HOME'], '.gcb')
    utils.create_dir_if_not_exists(DATA_HOME)
else:
    DATA_HOME = os.environ['GCB_DATA']

assert DATA_HOME 

DATA_PATH = os.path.join(DATA_HOME, "data")

RESULT_PATH = os.path.join(DATA_HOME, "result")

[utils.create_dir_if_not_exists(directory) for directory in [ DATA_PATH, RESULT_PATH]]

if 'GCB_HOME' not in os.environ:
    GCB_HOME = os.path.join(os.environ['HOME'], 'graph_clustering_benchmark')
else:
    GCB_HOME = os.environ['GCB_HOME']

assert GCB_HOME 

LFR_PROG = os.path.join(GCB_HOME, "submodules/LFR-Benchmark_UndirWeightOvp/lfrbench_udwov")
SCAN_CONVERT_PROG = os.path.join(GCB_HOME, "submodules/ppSCAN/converter")
SCANPP_PROG  = os.path.join(GCB_HOME, "submodules/ppSCAN/scanpp")
PSCAN_PROG  = os.path.join(GCB_HOME, "submodules/ppSCAN/pscan")
ANYSCAN_PROG  = os.path.join(GCB_HOME, "submodules/ppSCAN/anyscan")
CGGC_PROG  = os.path.join(GCB_HOME, "submodules/CGGC/rgmc")

def get_data_file_path(dsname, fname=""):
    dspath = os.path.join(DATA_PATH, dsname)
    utils.create_dir_if_not_exists(dspath)
    if fname:
        return os.path.join(dspath, fname)
    else:
        return dspath 


def get_result_file_path(dsname, algname):
    dspath = os.path.join(RESULT_PATH, dsname)
    utils.create_dir_if_not_exists(dspath)
    algpath = os.path.join(dspath, algname)
    utils.create_dir_if_not_exists(algpath)
    return algpath 

