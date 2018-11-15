from gct import utils, config
import urllib
import gzip
import pandas as pd 
import json 
from . import dataset 
import shutil
from gct.dataset.dataset import local_exists, load_local, Dataset
import os

    
class LAWDatasetConfig(object):        

    def __init__(self, name, description="", with_ground_truth=False, directed=False, weighted=False):
        self.logger = utils.get_logger("{}:{}".format(type(self).__name__, name))                
        self.with_ground_truth = with_ground_truth
        self.directed = directed
        self.weighted = weighted
        self.name = name 
        self.description = description
            
    def has_ground_truth(self):
        return self.with_ground_truth
    
    def is_directed(self):
        return self.directed
    
    def is_weighted(self):
        return self.weighted
    
    def get_remote_names(self):
        return ["{}{}".format(self.name, u) for u in ['-hc-t.properties', '.md5sums', '-hc-t.graph']]
    
    def has_downloaded(self, fname=None):
        if fname is None:
            for fname in self.get_remote_names():
                if not utils.file_exists(config.get_download_file_path(self.name, fname)):
                    return False 
            return True
        else:
            return utils.file_exists(config.get_download_file_path(self.name, fname))

    def download(self):
        for fname in self.get_remote_names():
            if not self.has_downloaded(fname):
                rfile = 'http://data.law.di.unimi.it/webdata/' + self.name + "/" + fname 
                lfile = config.get_download_file_path(self.name, fname, create=True)
                if not utils.file_exists(lfile):
                    self.logger.info("Dowloading {} to {} ".format(rfile, lfile))
                    utils.urlretrieve (rfile, lfile)
        
        assert self.has_downloaded()
        if not self.md5check():
            self.logger.error("md5 check failed")
            shutil.rmtree(config.get_download_file_path(self.name))
            raise Exception("md5 check failed")
    
    def md5check(self):
        cmd = 'md5sum --ignore-missing -c {}.md5sums'.format(self.name)
        status = utils.shell_run_and_wait(cmd, config.get_download_file_path(self.name))
        return status == 0

    @property
    def download_dir(self):
        return config.get_download_file_path(self.name)

    def get_edges(self):
        if not self.has_downloaded():
            self.download()
            
        graph_file = config.get_download_file_path(self.name, self.name + '.graph')
        self.logger.info("reading {}".format(graph_file))

        cmd = "{} -server -cp {} it.unimi.dsi.webgraph.ArcListASCIIGraph {} {}".format(
            utils.get_java_command(), config.WEBGRAPH_JAR_PATH, self.name+'-hc-t', self.name)
                    
        self.logger.info("Running " + cmd) 
        
        timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, self.download_dir))
        if status != 0:
            raise Exception("Run command with error status code {}".format(status))

        csvfile = os.path.join(self.download_dir, self.name)
        edges = pd.read_csv(csvfile, header=None, sep='\t')
        edges.columns = ['src', 'dest']
        utils.remove_if_file_exit(csvfile)
        return edges 
                         
    def get_ground_truth(self):
        return None
        

_DATASET_ = {
    }
        
_DATASET_['cnr-2000'] = LAWDatasetConfig('cnr-2000',
                                       with_ground_truth=False ,
                                       weighted=False,
                                       directed=True,
                                       description="cnr-2000")        


def list_datasets():
    return _DATASET_.keys()


def load_law_dataset(name, overide=False):
    if not overide and local_exists(name):
        return load_local(name)
    
    else:
        conf = _DATASET_[name ]
        edges = conf.get_edges()
        gt = conf.get_ground_truth()
        description = conf.description
        weighted = conf.weighted
        directed = conf.directed
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges, directed=directed, weighted=weighted, overide=overide)    

