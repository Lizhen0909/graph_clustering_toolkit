from gcb import utils, config
import urllib
import gzip
import numpy as np 
import pandas as pd 
import dask.dataframe as dd
import fastparquet

 
class Dataset(object):

    def __init__(self, name, files, description="", with_ground_truth=False):
        self.name = name 
        self.files = files 
        self.description = description
        self.with_ground_truth = with_ground_truth
        self.logger = utils.get_logger("{}:{}".format(type(self).__name__, self.name))
        config.get_data_file_path(self.name)
    def has_ground_truth(self):
        return self.with_ground_truth 
    
    def load(self):
        raise Exception("NA")

        
class SNAPDataset(Dataset):        

    def __init__(self, name, files, graph_file, ground_truth_file, description="", with_ground_truth=False):
        super(SNAPDataset, self).__init__(name, files, description, with_ground_truth)
        self.local_files = [config.get_data_file_path(name, u.split('/')[-1]) for u in files ]
        self.graph_file = config.get_data_file_path(self.name, graph_file)
        self.ground_truth_file = config.get_data_file_path(self.name, ground_truth_file)
        
    def has_downloaded(self):
        for fname in self.local_files:
            if not utils.file_exists(fname):
                return False 
        else:
            return True

    def download(self):
        for rfile, fname in zip(self.files, self.local_files):
            self.logger.info("Dowloading {} to {} ".format(rfile, fname))
            urllib.urlretrieve (rfile, fname)
        assert self.has_downloaded()
            
    def load_graph(self):
        parqfile = config.get_data_file_path(self.name, self.graph_file + ".parq")
        if not utils.file_exists(parqfile):
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
            fastparquet.writer.write(parqfile, edges, compression="SNAPPY")
        self.logger.info("reading {}".format(parqfile))            
        self.edges = dd.read_parquet(parqfile).compute()
        self.logger.info("Loaded {} edges".format(len(self.edges)))
        self.logger.info("The graph have {} nodes".format(len(set(self.edges.values.ravel()))))
        self.logger.info("\n" + str(self.edges.head()))
        
    def load_ground_truth(self):
        parqfile = config.get_data_file_path(self.name, self.ground_truth_file + ".parq")
        if not utils.file_exists(parqfile):
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
            fastparquet.writer.write(parqfile, ground_truth, compression="SNAPPY")
        self.logger.info("reading {}".format(parqfile))            
        self.ground_truth = dd.read_parquet(parqfile).compute()
        n_node=len(set(self.ground_truth['node']))
        n_cluster=len(set(self.ground_truth['cluster']))
        self.logger.info("Loaded {} nodes that have ground truth".format(n_node))  
        self.logger.info("The graph have  {} clusters".format(n_cluster))
        self.logger.info("Mean cluster size: {}".format(float(self.ground_truth.shape[0])/n_cluster))
        self.logger.info("Mean #membership: {}".format(self.ground_truth.groupby('node').count().mean()[0]))
        self.logger.info("\n" + str(self.ground_truth.head()))
        
    def load(self):
        if not self.has_downloaded():
            self.download()
            
        self.load_graph()
        self.load_ground_truth()    
        

_DATASET_ = {
    }
        
_DATASET_['com-LiveJournal'] = SNAPDataset('com-LiveJournal',
                                       files=[
                                           'http://snap.stanford.edu/data/bigdata/communities/com-lj.ungraph.txt.gz',
                                           'http://snap.stanford.edu/data/bigdata/communities/com-lj.all.cmty.txt.gz',
                                           'http://snap.stanford.edu/data/bigdata/communities/com-lj.top5000.cmty.txt.gz'],
                                       graph_file="com-lj.ungraph.txt.gz",
                                       ground_truth_file="com-lj.all.cmty.txt.gz",
                                       with_ground_truth=True,
                                       description="SNAP: Networks with ground-truth communities: com-LiveJournal")        

_DATASET_['com-DBLP'] = SNAPDataset('com-DBLP',
                                       files=[
                                           'http://snap.stanford.edu/data/bigdata/communities/com-dblp.ungraph.txt.gz',
                                           'http://snap.stanford.edu/data/bigdata/communities/com-dblp.all.cmty.txt.gz',
                                           'http://snap.stanford.edu/data/bigdata/communities/com-dblp.top5000.cmty.txt.gz'],
                                       graph_file="com-dblp.ungraph.txt.gz",
                                       ground_truth_file="com-dblp.all.cmty.txt.gz",
                                       with_ground_truth=True,
                                       description="SNAP: Networks with ground-truth communities: com-DBLP")        



def list_datasets():
    return _DATASET_.keys()


def load_dataset(name):
    dataset = _DATASET_[name]
    dataset.load()
    return dataset 

