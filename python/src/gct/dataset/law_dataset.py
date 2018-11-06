from gct import utils, config
import urllib
import gzip
import pandas as pd 
import json 
from . import dataset 
import shutil
    
class LAWDatasetConfig(object):        

    def __init__(self, name, with_ground_truth=False, directed=False, weighted=False):
        self.with_ground_truth = with_ground_truth
        self.directed = directed
        self.weighted = weighted

 
            
    def has_ground_truth(self):
        return self.with_ground_truth
    
    def is_directed(self):
        return self.directed
    
    def is_weighted(self):
        return self.weighted
    
    def get_remote_uris(self):
        return ["{}-hc{}".format(self.name, u) for u in ['.properties', '.md5sums', '.graph']]
    
    def has_downloaded(self):
        for fname in self.get_remote_uris():
            if not utils.file_exists(config.get_data_file_path(self.name, fname)):
                return False 
        return True

    def download(self):
        for fname in self.get_remote_uris():
            rfile = 'http://law.di.unimi.it/webdata/' + fname 
            lfile = config.get_data_file_path(self.name, fname)
            if not utils.file_exists(lfile):
                self.logger.info("Dowloading {} to {} ".format(rfile, lfile))
                utils.urlretrieve (rfile, lfile)
        
        assert self.has_downloaded()
        if not self.md5check():
            shutil.rmtree(config.get_data_file_path(self.name))
    
    def md5check(self):
        cmd = 'md5sum -c {}-hc.md5sums'.format(self.name)
        status = utils.shell_run_and_wait(cmd, config.get_data_file_path(self.name))
        return status == 0

    def get_edges(self):
        fname = self.parq_edges
        if utils.file_exists(fname):
            return self.edges_from_parq()
        else:
            if not self.has_downloaded():
                self.download()
            graph_file = self.name+"-hc.graph"
            self.logger.info("reading {}".format(graph_file))
            edges = []
            with gzip.open(self.graph_file, 'rt') as f:
                for line in f:
                    if not line.startswith("#"):
                        a, b = line.split("\t")
                        edges.append([int(a), int(b)])
                    else:
                        self.logger.info(line)  
            edges = pd.DataFrame(edges, columns=['src', 'dest'])
            self.logger.info("Loaded {} edges".format(len(edges)))
            self.logger.info("The graph have {} nodes".format(len(set(edges.values.ravel()))))
            self.logger.info("\n" + str(edges.head()))
            return edges 
                         
    # return
    def get_ground_truth(self):
        if self.has_ground_truth():
            fname = self.parq_ground_truth
            if utils.file_exists(fname):
                return self.ground_from_parq()
            else:
                if not self.has_downloaded():
                    self.download()
            
                raise Exception("NA")
                        
        else:
            raise Exception("graph has no ground truth")
        

_DATASET_ = {
    }
        
_DATASET_['cnr-2000'] = LAWDatasetConfig('cnr-2000',
                                       with_ground_truth=False ,
                                       weighted=False,
                                       directed=False)        


def list_datasets():
    return _DATASET_.keys()


def get_dataset(name):
    ds = _DATASET_[name]
    return ds 

