from gct import utils, config
import urllib
import gzip
import pandas as pd 
import json 
from . import dataset 
from gct.dataset.dataset import local_exists, load_local, Dataset
 
    
class SNAPConfig(object):        

    def __init__(self, name, files, graph_file, ground_truth_file, description="",
                 with_ground_truth=False, directed=False, weighted=False):
        self.logger = utils.get_logger("{}:{}".format(type(self).__name__, name ))        
        self.name=name 
        self.description=description
        self.files = files 
        self.with_ground_truth = with_ground_truth
        self.directed = directed
        self.weighted = weighted
        self.local_files = [config.get_download_file_path(name, u.split('/')[-1]) for u in files ]
        self.graph_file = config.get_download_file_path(self.name, graph_file)
        self.ground_truth_file = config.get_download_file_path(self.name, ground_truth_file) 

    def has_downloaded(self):
        for fname in self.local_files:
            if not utils.file_exists(fname):
                return False 
        else:
            return True

    def download(self):
        for rfile, fname in zip(self.files, self.local_files):
            self.logger.info("Dowloading {} to {} ".format(rfile, fname))
            utils.urlretrieve (rfile, fname)
        assert self.has_downloaded()

    def get_edges(self):
        if not self.has_downloaded():
            self.download()

        self.logger.info("reading {}".format(self.graph_file))
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
        if self.with_ground_truth:
            if not self.has_downloaded():
                self.download()
        
            self.logger.info("reading {}".format(self.ground_truth_file))
            ground_truth = []
            i = 1
            with gzip.open(self.ground_truth_file, 'rt') as f:
                for line in f:
                    if not line.startswith("#"):
                        for node in  line.split("\t"):
                            ground_truth.append([int(node), i])
                        i = i + 1
                    else:
                        self.logger.info(line)
            ground_truth = pd.DataFrame(ground_truth, columns=['node', 'cluster'])
            n_node = len(set(ground_truth['node']))
            n_cluster = len(set(ground_truth['cluster']))
            self.logger.info("Loaded {} nodes that have ground truth".format(n_node))  
            self.logger.info("The graph have  {} clusters".format(n_cluster))
            self.logger.info("Mean cluster size: {}".format(float(ground_truth.shape[0]) / n_cluster))
            self.logger.info("Mean #membership: {}".format(ground_truth.groupby('node').count().mean()[0]))
            self.logger.info("\n" + str(ground_truth.head()))
            return ground_truth
                        
        else:
            return None 
        

_DATASET_ = {
    }
        
_DATASET_['com-LiveJournal'] = SNAPConfig('com-LiveJournal',
                                       files=[
                                           'http://snap.stanford.edu/data/bigdata/communities/com-lj.ungraph.txt.gz',
                                           'http://snap.stanford.edu/data/bigdata/communities/com-lj.all.cmty.txt.gz',
                                           'http://snap.stanford.edu/data/bigdata/communities/com-lj.top5000.cmty.txt.gz'],
                                       graph_file="com-lj.ungraph.txt.gz",
                                       ground_truth_file="com-lj.all.cmty.txt.gz",
                                       with_ground_truth=True,
                                       weighted=False,
                                       directed=False,
                                       description="SNAP: Networks with ground-truth communities: com-LiveJournal")        

_DATASET_['com-DBLP'] = SNAPConfig('com-DBLP',
                                       files=[
                                           'http://snap.stanford.edu/data/bigdata/communities/com-dblp.ungraph.txt.gz',
                                           'http://snap.stanford.edu/data/bigdata/communities/com-dblp.all.cmty.txt.gz',
                                           'http://snap.stanford.edu/data/bigdata/communities/com-dblp.top5000.cmty.txt.gz'],
                                       graph_file="com-dblp.ungraph.txt.gz",
                                       ground_truth_file="com-dblp.all.cmty.txt.gz",
                                       with_ground_truth=True,
                                       weighted=False,
                                       directed=False,
                                       description="SNAP: Networks with ground-truth communities: com-DBLP")        


def load_snap_dataset(name, overide=False):
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


def list_datasets():
    return _DATASET_.keys()

