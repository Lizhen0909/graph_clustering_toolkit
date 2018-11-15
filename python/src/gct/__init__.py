from . import alg, dataset, utils
from .config import get_data_file_path, get_download_file_path, get_result_file_path
from .alg import *
from .alg.function import __ALG_LIST__
from .dataset import *
from .dataset.dataset import Dataset, Clustering
from .alg.clustering import Result
from .metrics import *
from .dataset.convert import *

__all__ = __ALG_LIST__  



def remove_results(data_pattern='*', run_pattern='*', dry_run=True):
    '''
    remove data and algorithm run results by patterns.  
    '''
    from fnmatch import fnmatch
    for dataname, lst in gct.list_all_clustering_results().items():
        for runname in lst:
            if fnmatch(dataname, data_pattern) and fnmatch(runname, run_pattern):
                filepath = gct.config.get_result_file_path(dataname, runname)
                print ("Removing {}".format(filepath))
                if not dry_run:
                    utils.remove_if_file_exit(filepath, is_dir=True)
    if dry_run:
        print ("No files were deleted. Use dry_run=False to truly remove them.")


def remove_data(data_pattern='*', with_results=True, dry_run=True):
    '''
    remove data (and algorithm run results) by data name pattern.  
    '''
        
    from fnmatch import fnmatch
    for dataname in gct.list_local_graph():
        if fnmatch(dataname, data_pattern):
            filepath = gct.config.get_data_file_path(dataname)
            print ("Removing {}".format(filepath))
            if not dry_run:
                utils.remove_if_file_exit(filepath, is_dir=True)
            
            if with_results:
                filepath = gct.config.get_result_file_path(dataname)
                print ("Removing {}".format(filepath))
                if not dry_run:
                    utils.remove_if_file_exit(filepath, is_dir=True)
    if dry_run:
        print ("No files were deleted. Use dry_run=False to truly remove them.")


def to_cluster(obj):
    from gct.dataset.dataset import Clustering
    return Clustering(obj)


def to_result(obj):
    from gct.alg.clustering import Result
    return Result(obj)

