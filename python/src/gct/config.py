'''
Created on Oct 23, 2018

@author: lizhen
'''

import os
from gct import utils

if 'GCT_DATA' not in os.environ:
    DATA_HOME = os.path.join(os.environ['HOME'], '.gct')
    utils.create_dir_if_not_exists(DATA_HOME)
else:
    DATA_HOME = os.environ['GCT_DATA']

assert DATA_HOME 

DATA_PATH = os.path.join(DATA_HOME, "data")
DOWNLOAD_PATH = os.path.join(DATA_HOME, "download")
RESULT_PATH = os.path.join(DATA_HOME, "result")

[utils.create_dir_if_not_exists(directory) for directory in [ DATA_PATH, DOWNLOAD_PATH, RESULT_PATH]]

if 'GCT_HOME' not in os.environ:
    GCT_HOME = os.path.join(os.environ['HOME'], 'graph_clustering_toolkit')
else:
    GCT_HOME = os.environ['GCT_HOME']

assert GCT_HOME 

LFR_PROG = os.path.join(GCT_HOME, "submodules/LFR-Benchmark_UndirWeightOvp/lfrbench_udwov")
SCAN_CONVERT_PROG = os.path.join(GCT_HOME, "submodules/ppSCAN/converter")
HIG_CONVERT_PROG = os.path.join(GCT_HOME, "submodules/hirecs/pajek_hig.py")
SCANPP_PROG = os.path.join(GCT_HOME, "submodules/ppSCAN/scanpp")
PSCAN_PROG = os.path.join(GCT_HOME, "submodules/ppSCAN/pscan")
PPSCAN_PROG = os.path.join(GCT_HOME, "submodules/ppSCAN/pSCANParallel")
PPSCANSSE_PROG = os.path.join(GCT_HOME, "submodules/ppSCAN/pSCANParallelSSE")
ANYSCAN_PROG = os.path.join(GCT_HOME, "submodules/ppSCAN/anyscan")
CGGC_PROG = os.path.join(GCT_HOME, "submodules/CGGC/rgmc")
STREAMCOM_PROG = os.path.join(GCT_HOME, "submodules/graph-streaming/streamcom")
MCL_PROG = os.path.join(GCT_HOME, "submodules/local/bin/mcl")
HIRECS_PATH = os.path.join(GCT_HOME, "submodules/hirecs")
LSO_CLUSTER_PROG = os.path.join(GCT_HOME, "submodules/graph-cluster/lso-cluster")
LABLE_RANK_PROG = os.path.join(GCT_HOME, "submodules/GANXiS/LabelRank")
GANXISW_PROG = os.path.join(GCT_HOME, "submodules/GANXiS/GANXiSw.jar")
GECMI_PROG = os.path.join(GCT_HOME, "submodules/GenConvNMI/gecmi")
ONMI_PROG = os.path.join(GCT_HOME, "submodules/OvpNMI/onmi")
XMEASURES_PROG = os.path.join(GCT_HOME, "submodules/xmeasures/xmeasures")
MODULE_PARIS_PATH = os.path.join(GCT_HOME, "submodules/paris")


def get_data_file_path(dsname, fname="", create=False):
    dspath = os.path.join(DATA_PATH, dsname)
    if create:
        utils.create_dir_if_not_exists(dspath)
    if fname:
        return os.path.join(dspath, fname)
    else:
        return dspath 


def get_download_file_path(dsname, fname="", create=False):
    dspath = os.path.join(DOWNLOAD_PATH, dsname)
    if create: utils.create_dir_if_not_exists(dspath)
    if fname:
        return os.path.join(dspath, fname)
    else:
        return dspath 


def get_result_file_path(dsname, runname="", create=False):
    dspath = os.path.join(RESULT_PATH, dsname)
    if create: utils.create_dir_if_not_exists(dspath)
    if runname:
        algpath = os.path.join(dspath, runname)
        if create: utils.create_dir_if_not_exists(algpath)
        return algpath
    else:
        return dspath 


def get_dct_prog(name, directed=False):
    if name == 'seq_louvain':
        prog = os.path.join(GCT_HOME, "submodules/distributed_clustering_thrill/build/seq_louvain")
        return prog
    elif name == 'infomap':
        prog = os.path.join(GCT_HOME, "submodules/distributed_clustering_thrill/build/infomap")
        if directed: prog += '_directed'
        return prog 
    elif name.startswith('dlslm') or name in ['dlplm']:
        prog = os.path.join(GCT_HOME, "submodules/distributed_clustering_thrill/build/" + name)
        return prog             
    else:
        raise Exception("Unknown " + name)

    
def get_powergraph_prog(name, directed=False):
    if name in ['label_propagation']:
        prog = os.path.join(GCT_HOME, "submodules/PowerGraph/release/apps/label_propagation/label_propagation")
        return prog             
    elif name in ['GossipMap']:
        prog = os.path.join(GCT_HOME, "submodules/PowerGraph/release/apps/GossipMap/GossipMap")
        return prog
    elif name in ['RelaxMap']:
        prog = os.path.join(GCT_HOME, "submodules/RelaxMap/ompRelaxmap")
        return prog                 
    else:
        raise Exception("Unknown " + name)


def get_OSLOM_prog(name, is_directed):
    if name == 'infomap':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM2/infomap")
        # prog += '_dir' if is_directed else "_undir"
        prog += '_dir'  # undir has bug        
        return prog
    elif name == 'Infohiermap':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM/infohiermap")
        prog += '_dir' if is_directed else "_undir"
        return prog 
    elif name == 'oslom':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM2/oslom")
        prog += '_dir' if is_directed else "_undir"
        return prog    
    elif name == 'copra':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM2/copra.jar")
        return prog           
    elif name == 'lpm':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM/lpm")
        return prog     
    elif name == 'louvain_method':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM/louvain_method")
        return prog         
    elif name == 'louvain_script':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM2/louvain_script")
        return prog 
    elif name == 'convert':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM2/convert")
        return prog   
    elif name == 'community':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM2/community")
        return prog   
    elif name == 'hierarchy':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM2/hierarchy")
        return prog                  
    elif name == 'infomap_script':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM2/infomap")
        prog += '_dir' if is_directed else "_undir"
        prog += '_script'
        return prog              
    elif name == 'modopt':
        prog = os.path.join(GCT_HOME, "submodules/OSLOM/modopt")
        return prog             
    else:
        raise Exception("Unknown " + name)


def get_LFR_prog(weighted, directed, hier=False):
    if hier:
        if weighted or directed:
            raise ValueError("Only undirected and unweighted supported for hierarchical graph")
        return os.path.join(GCT_HOME, "submodules/CommunityDetectionCodes/lfr_hierarchical_net")
    
    if weighted:
        if directed:
            return os.path.join(GCT_HOME, "submodules/CommunityDetectionCodes/lfr_weighted_dir_net")
        else:
            return os.path.join(GCT_HOME, "submodules/CommunityDetectionCodes/lfr_weighted_net")
    else:
        if directed:
            return os.path.join(GCT_HOME, "submodules/CommunityDetectionCodes/lfr_dir_net")
        else:
            return os.path.join(GCT_HOME, "submodules/CommunityDetectionCodes/lfr_undir_net")

