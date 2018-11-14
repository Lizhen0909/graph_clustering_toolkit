'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct import utils, config
import os
import json
import collections
import pandas as pd     


def has_result(dataname, runname):
    fpath = os.path.join(config.get_result_file_path(dataname, runname), 'result.txt')
    return utils.file_exists(fpath)

        
def load_result(dataname, runname):
    fpath = os.path.join(config.get_result_file_path(dataname, runname), 'result.txt')
    with open(fpath, 'rt') as f :
        return Result(json.load(f))


def save_result(result):
    if isinstance(result, Result): 
        result.save()
    else:
        filepath = config.get_result_file_path(result['dataname'], result['runname'], create=True)
        try:
            fpath = os.path.join(filepath, 'result.txt')
            with open(fpath, 'wt') as f:
                json.dump(result, f)
        except:
            utils.remove_if_file_exit(fpath, is_dir=False)
            raise

        
class Result(collections.MutableMapping):
    """
    The result after running a clustering algorithm. An algorithm may result one or multiple clusters. 
    """

    def __init__(self, result):
        if isinstance(result, Result):
            self.store = result.store
        elif isinstance(result, dict):
            self.store = result 
        else:
            raise Exception("failed")
        
    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

    def __str__(self):
        return str(self.store) 
    
    def __repr__(self):
        return str(self.store)
            
    def save(self):
        save_result(self.store)
        return self 
        
    @property
    def result(self): 
        return self.store

    def clusters(self, as_dataframe=False, key=None):
        '''
        Get a cluster. 
        
        :param as_dataframe: return a Pandas dataframe instread of dict
        :param key:     if multiple clusters exists, the one with the key is returned.
        
        :rtype: A Pandas dataframe or a :meth:`gct.Clustering` 
        '''
        if self.get("multilevel") or self.get("multiclusters"):
            akey = list(self.get('clusters').keys())[0]
            default_level = key
            if key is None: default_level = self.get('max_level')
            if default_level is None: default_level = akey
            if isinstance(akey, str): 
                default_level = str(default_level)
                d = self.get('clusters')[default_level]
                d = {int(u):v for u, v in d.items()}
            else:
                d = self.get('clusters')[default_level]
        else:
            d = self.get('clusters') 
        if as_dataframe:
            lst = [] 
            for k, vs in d.items():
                for v in vs: 
                    lst.append([v, k])
            return pd.DataFrame(lst, columns=['node', 'cluster'])
        else:
            return Clustering(d)

    @property
    def cluster_keys(self):
        '''
        keys for multiclusters. 
        '''
        if self.is_multiclusters:
            return self.get('clusters').keys()
        return None 
    
    @property     
    def is_multilevel(self):
        """
        True when the algorithm returns hierarchical clustering. A multiclusters result may not be hierarchical. 
        """
        return "multilevel" in self
    
    @property     
    def is_multiclusters(self):
        """
        True when the algorithm returns multiple clustering. 
        """
        
        return "multiclusters" in self  or self.is_multilevel
        
    @property     
    def runname(self):
        '''
        runname for the result
        '''
        return self.get("runname")

    @property     
    def params(self):
        '''
        parameters when the algorithm ran.
        '''
        return self.get("params")

    @property             
    def dataname(self):
        '''
        dataset name for the run
        '''
        return self.get("dataname")

    @property       
    def meta(self):
        '''
        meta data
        '''
        return self.get("meta", None)

    @property     
    def timecost(self):
        '''
        Time (in second) to run the algorithm.
        '''
        return self.get("timecost")        


class Clustering(object):

    def __init__(self, name):
        self.name = name 
        self.logger = utils.get_logger(self.name)
        self.result_file = config

    def get_meta(self):
        raise Exception("NA")
    
    def run(self, data):
        raise Exception("NA")
        
    def get_result(self):
        if hasattr(self, 'result'):
            return Result(self.result)
        else:
            raise Exception("No result found. probably no run has been done")
