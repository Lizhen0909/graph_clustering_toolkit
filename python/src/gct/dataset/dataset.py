from gct import utils, config
from gct.dataset import edgelist2pajek
import dask.dataframe as dd
import fastparquet
import json 
import numpy as np
import pandas as pd  
import os


class Dataset(object):

    def __init__(self, name=None, description="", anonymous=False):
        self.name = name 
        self.description = description
        self.logger = utils.get_logger("{}:{}".format(type(self).__name__, self.name))
        
        if not anonymous:
            assert name 
            self.parq_edges = config.get_data_file_path(self.name, 'edges.parq')
            self.parq_ground_truth = config.get_data_file_path(self.name, 'ground_truth.parq')
            self.file_edges = config.get_data_file_path(self.name, 'edges.txt')
            self.file_pajek = config.get_data_file_path(self.name, 'pajek.txt')
            self.file_scanbin = config.get_data_file_path(self.name, 'scanbin')
            self.file_anyscan = config.get_data_file_path(self.name, 'anyscan.txt')
            self.file_snap = config.get_data_file_path(self.name, 'snap.bin')
        
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
 
    def to_edgelist(self, filepath=None, sep=" ", sort=False):
        if (filepath == None):
            filepath = self.file_edges
            if utils.file_exists(filepath):
                return filepath 
        self.logger.info("writing edges to " + filepath)
        with open(filepath, 'wt') as f :
            columns = ['src', 'dest', 'weight'] if self.is_weighted() else ['src', 'dest']
            df = self.get_edges()[columns]
            if sort:
                df = df.sort_values(by=['src', 'dest'])
            for i in range(df.shape[0]):
                r = df.iloc[i]
                r = ['%g' % (u) for u in r ]
                row = sep.join(r)  
                row += "\n"
                f.write(row)
        self.logger.info("finish writing " + filepath)                
        return filepath 

    def to_snapformat(self, filepath=None):
        if (filepath == None):
            filepath = self.file_snap 
            if utils.file_exists(filepath):
                return filepath
        
        import snap        
        from gct.dataset import convert
        g = convert.to_snap(self)
        self.logger.info("Writing {} to {}".format(type(g), filepath))
        FOut = snap.TFOut(filepath)
        g.Save(FOut)
        FOut.Flush()
        
        return filepath 
        
    def to_pajek(self, filepath=None):
        if (filepath == None):
            filepath = self.file_pajek
            if utils.file_exists(filepath):
                return filepath             
        if not utils.file_exists(self.file_edges): self.to_edgelist()
        edgelist2pajek.edgelist_to_pajek(self.file_edges, self.file_pajek , self.is_directed(), self.is_weighted())
        return filepath 

    def to_scanbin(self, filepath=None):
        if (filepath == None):
            filepath = self.file_scanbin
            if utils.file_exists(os.path.join(filepath, "b_degree.bin")) and utils.file_exists(os.path.join(filepath, "b_adj.bin")):
                return filepath         
            utils.create_dir_if_not_exists(filepath)    
        if not utils.file_exists(self.file_edges): self.to_edgelist()
        cmd = "{} {} {} {}".format(config.SCAN_CONVERT_PROG, self.file_edges, "b_degree.bin", "b_adj.bin")
        self.logger.info("running " + cmd)
        status = utils.shell_run_and_wait(cmd, filepath)
        if (status != 0):
            raise Exception("run command failed: " + str(status))
        return filepath 

    def to_anyscan(self, filepath=None):
        if self.is_directed():
            raise Exception("directed graph not supported")
        if (filepath == None):
            filepath = self.file_anyscan
            if utils.file_exists(filepath):
                return filepath
            
        edges1 = self.get_edges()[['src', 'dest']]
        min_node = min(edges1['src'].min(), edges1['dest'].min())
        max_node = max(edges1['src'].max(), edges1['dest'].max())
        self.logger.info("min node: {}, max node: {}".format(min_node, max_node))
        if min_node != 0  :
            self.logger.warn("node id is greater than 0, fake node will be added")

        self_edges = pd.DataFrame([[u, u] for u in range(max_node + 1)], columns=['src', 'dest'])
        edges2 = edges1[['dest', 'src']].copy();  edges2.columns = ['src', 'dest']
        edges = pd.concat([edges1, edges2, self_edges], axis=0)
        del edges1, edges2, self_edges 

        def fun(df):
            values = sorted(list(set(df['dest'])))
            return str(len(values)) + " " + " ".join([str(u) for u in values])

        grouped = edges.groupby('src').apply(fun).reset_index()
        with open(filepath, 'wt') as f:
            f.write(str(max_node + 1) + "\n")
            for i in grouped.index: 
                f.write(grouped.loc[i, 0] + "\n")
        return filepath 


class AnonymousDataset(Dataset):        

    def __init__(self, edges, description="", ground_truth=None, directed=False, weighted=False):
        super(AnonymousDataset, self).__init__(name=None , description=description, anonymous=True)
        self.with_ground_truth = ground_truth is not None 
        self.directed = directed
        self.weighted = weighted
        
        columns = ['src', 'dest', 'weight'] if weighted else ['src', 'dest']
        self.edges = self.to_dataframe(edges, columns) 
        self.ground_truth = None if ground_truth is None else self.to_dataframe(ground_truth, ["node", "cluster"])

    def to_dataframe(self, obj, columns):
        if isinstance(obj, pd.DataFrame):
            assert obj.shape[1] == len(columns) 
            obj.columns = columns
            return obj 
        elif isinstance(obj, list) or isinstance(obj, np.ndarray):
            arr = np.array(obj) 
            assert arr.shape[1] == len(columns)
            return pd.DataFrame(arr, columns=columns)
        else:
            raise Exception("type not supported: " + str(type(obj)))
        
    def has_ground_truth(self):
        return self.with_ground_truth
    
    def is_directed(self):
        return self.directed
    
    def is_weighted(self):
        return self.weighted
    
    def get_edges(self):
        return self.edges             

    # return
    def get_ground_truth(self):
        if self.has_ground_truth():
            return self.ground_truth
        else:
            raise Exception("graph has no ground truth")


class DefaultDataset(Dataset):        

    def __init__(self, name, edges, description="", ground_truth=None, directed=False, weighted=False):
        super(DefaultDataset, self).__init__(name, description=description)
        self.with_ground_truth = ground_truth is not None 
        self.directed = directed
        self.weighted = weighted
        
        columns = ['src', 'dest', 'weight'] if weighted else ['src', 'dest']
        self.edges = self.to_dataframe(edges, columns) 
        self.ground_truth = None if ground_truth is None else self.to_dataframe(ground_truth, ["node", "cluster"])
        
        meta_file = config.get_data_file_path(self.name, 'meta.info')
        if not utils.file_exists(meta_file):
            json.dump(self.get_meta(), open(meta_file, 'wt')) 

    def to_dataframe(self, obj, columns):
        if isinstance(obj, pd.DataFrame):
            assert obj.shape[1] == len(columns) 
            obj.columns = columns
            return obj 
        elif isinstance(obj, list) or isinstance(obj, np.ndarray):
            arr = np.array(obj) 
            assert arr.shape[1] == len(columns)
            return pd.DataFrame(arr, columns=columns)
        else:
            raise Exception("type not supported: " + str(type(obj)))
        
    def has_ground_truth(self):
        return self.with_ground_truth
    
    def is_directed(self):
        return self.directed
    
    def is_weighted(self):
        return self.weighted
    
    def get_edges(self):
        return self.edges             

    # return
    def get_ground_truth(self):
        if self.has_ground_truth():
            return self.ground_truth
        else:
            raise Exception("graph has no ground truth")
        
                    
from gct.dataset import snap_dataset


def list_datasets():
    return snap_dataset.list_datasets()


def get_dataset(name):
    return snap_dataset.get_dataset(name)
