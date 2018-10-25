from gcb import utils, config
import dask.dataframe as dd
import fastparquet
import json 


class Dataset(object):

    def __init__(self, name, description=""):
        self.name = name 
        self.description = description
        self.logger = utils.get_logger("{}:{}".format(type(self).__name__, self.name))
        self.parq_edges = config.get_data_file_path(self.name, 'edges.parq')
        self.parq_ground_truth = config.get_data_file_path(self.name, 'ground_truth.parq')
        
    def __repr__(self, *args, **kwargs):
        return self.__str__()
    
    def get_meta(self):
        d = {'name': self.name ,
            'weighted': self.is_weighted(),
             'has_ground_truth':self.has_ground_truth(),
             'directed': self.is_directed()}
        d['parq_edges'] = self.parq_edges
        
        if self.has_ground_truth():
            d['parq_ground_truth'] = self.parq_ground_truth
        d['description'] = self.description
        return d 
    
    def __str__(self, *args, **kwargs):
        d = self.get_meta()
        return json.dumps(d)
        
    def has_ground_truth(self):
        raise Exception("NA")
    
    def is_directed(self):
        raise Exception("NA")
    
    def is_weighted(self):
        raise Exception("NA")
    
    # return edge list
    def get_edges(self):
        raise Exception("NA")
    
    # return
    def get_ground_truth(self):
        raise Exception("NA")
    
    # return the edge list parquet file 
    def edges_from_parq(self):
        fname = self.parq_edges
        if not utils.file_exists(fname):
            df = self.get_edges()
            fastparquet.writer.write(fname, df, compression="SNAPPY")
        self.logger.info("reading {}".format(fname))            
        return dd.read_parquet(fname).compute()            

    # return  ground truth files if possible 
    def ground_from_parq(self):
        if self.has_ground_truth():
            fname = self.parq_ground_truth
            if not utils.file_exists(fname):
                df = self.get_ground_truth()
                fastparquet.writer.write(fname, df, compression="SNAPPY")
            self.logger.info("reading {}".format(fname))            
            return dd.read_parquet(fname).compute()
        else:
            raise Exception("graph has no ground truth")

    # load data into memories
    def load(self):
        self.edges = self.edges_from_parq()
        if self.has_ground_truth():
            self.ground_truth = self.ground_from_parq()
 

from gcb import snap_dataset
def list_datasets():
    return snap_dataset.list_datasets()


def get_dataset(name):
    return snap_dataset.get_dataset(name)
