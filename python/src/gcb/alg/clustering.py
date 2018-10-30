'''
Created on Oct 27, 2018

@author: lizhen
'''
from gcb import utils, config
import os
import json
    
    
def load_rusult(dataname, algname):
    fpath = os.path.join(config.get_result_file_path(dataname, algname), 'result.txt')
    with open(fpath, 'rt') as f :
        return json.load(f)


def save_result(result):
    fpath = os.path.join(config.get_result_file_path(result['dataname'], result['algname']), 'result.txt')
    with open(fpath, 'wt') as f:
        json.dump(result, f)


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
            return self.result
        else:
            raise Exception("No result found. probably no run has been done")
                