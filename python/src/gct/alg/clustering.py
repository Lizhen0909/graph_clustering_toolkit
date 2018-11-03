'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct import utils, config
import os
import json
import collections
import pandas as pd     


def has_result(dataname, algname):
    fpath = os.path.join(config.get_result_file_path(dataname, algname), 'result.txt')
    return utils.file_exists(fpath)

        
def load_result(dataname, algname):
    fpath = os.path.join(config.get_result_file_path(dataname, algname), 'result.txt')
    with open(fpath, 'rt') as f :
        return Result(json.load(f))


def save_result(result):
    if isinstance(result, Result): 
        result.save()
    else:
        fpath = os.path.join(config.get_result_file_path(result['dataname'], result['algname']), 'result.txt')
        with open(fpath, 'wt') as f:
            json.dump(result, f)


class Result(collections.MutableMapping):

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

    def clusters(self, as_dataframe=False):
        if self.get("multilevel"):
            max_level = self.get('max_level')
            if isinstance(list(self.keys())[0], str): 
                max_level = str(max_level)
                d = self.get('clusters')[max_level]
                d={int(u):v for u,v in d.items()}
            else:
                d = self.get('clusters')[max_level]
        else:
            d = self.get('clusters') 
        if as_dataframe:
            lst = [] 
            for k, vs in d.items():
                for v in vs: 
                    lst.append([v, k])
            return pd.DataFrame(lst, columns=['node', 'cluster'])
        else:
            return d
        
    @property     
    def algname(self):
        return self.get("algname")

    @property     
    def params(self):
        return self.get("params")

    @property             
    def dataname(self):
        return self.get("dataname")

    @property       
    def meta(self):
        return self.get("meta", None)

    @property     
    def timecost(self):
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
                
