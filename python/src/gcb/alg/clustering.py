'''
Created on Oct 27, 2018

@author: lizhen
'''
from gcb.ds import convert
from gcb import utils, config
import os
import json
    
    
def load_rusult(dataname, algname):
    fpath = os.path.join(config.get_result_file_path(dataname, algname), 'result.txt')
    return json.load(open(fpath, 'rt'))


def save_result(result):
    fpath = os.path.join(config.get_result_file_path(result['dataname'], result['algname']), 'result.txt')
    json.dump(result, open(fpath, 'wt'))


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
                