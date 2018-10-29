'''
Created on Oct 23, 2018

@author: lizhen
'''

import os
from gcb import utils

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
    GCB_HOME = os.path.join(os.environ['HOME'], 'graph_clustering_toolkit')
else:
    GCB_HOME = os.environ['GCB_HOME']

assert GCB_HOME 

LFR_PROG = os.path.join(GCB_HOME, "submodules/LFR-Benchmark_UndirWeightOvp/lfrbench_udwov")
SCAN_CONVERT_PROG = os.path.join(GCB_HOME, "submodules/ppSCAN/converter")
SCANPP_PROG = os.path.join(GCB_HOME, "submodules/ppSCAN/scanpp")
PSCAN_PROG = os.path.join(GCB_HOME, "submodules/ppSCAN/pscan")
PPSCAN_PROG = os.path.join(GCB_HOME, "submodules/ppSCAN/pSCANParallel")
PPSCANSSE_PROG = os.path.join(GCB_HOME, "submodules/ppSCAN/pSCANParallelSSE")
ANYSCAN_PROG = os.path.join(GCB_HOME, "submodules/ppSCAN/anyscan")
CGGC_PROG = os.path.join(GCB_HOME, "submodules/CGGC/rgmc")
STREAMCOM_PROG = os.path.join(GCB_HOME, "submodules/graph-streaming/streamcom")
MCL_PROG = os.path.join(GCB_HOME, "submodules/local/bin/mcl")


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


def get_OSLOM_prog(name, is_directed):
    if name == 'infomap':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM2/infomap")
        #prog += '_dir' if is_directed else "_undir"
        prog += '_dir'  # undir has bug        
        return prog
    elif name == 'Infohiermap':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM/infohiermap")
        prog += '_dir' if is_directed else "_undir"
        return prog 
    elif name == 'oslom':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM2/oslom")
        prog += '_dir' if is_directed else "_undir"
        return prog    
    elif name == 'copra':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM2/copra.jar")
        return prog           
    elif name == 'lpm':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM/lpm")
        return prog     
    elif name == 'louvain_method':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM/louvain_method")
        return prog         
    elif name == 'louvain_script':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM2/louvain_script")
        return prog 
    elif name == 'convert':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM2/convert")
        return prog   
    elif name == 'community':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM2/community")
        return prog   
    elif name == 'hierarchy':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM2/hierarchy")
        return prog                  
    elif name == 'infomap_script':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM2/infomap")
        prog += '_dir' if is_directed else "_undir"
        prog += '_script'
        return prog              
    elif name == 'modopt':
        prog = os.path.join(GCB_HOME, "submodules/OSLOM/modopt")
        return prog             
    else:
        raise Exception("Unknown " + name)

