from gct import utils, config
from gct.dataset import edgelist2pajek
import fastparquet
import json 
import numpy as np
import pandas as pd  
import os


class Cluster(object):

    def __init__(self, cluster):
        self.logger = utils.get_logger("{}".format(type(self).__name__))
        self.cluster = None 
        self.path = None 
        if isinstance(cluster, str):
            self.path = utils.abspath(cluster)
        elif isinstance(cluster, pd.DataFrame):
            if not 'cluster' in cluster.columns or not 'node' in cluster.columns:
                raise ValueError("arg is not right")
            self.cluster = cluster[['node', 'cluster']]
        else:  
            if isinstance(cluster, list):
                arr = np.array(cluster)
            elif isinstance(cluster, np.ndarray):
                arr = cluster  
            else:
                raise ValueError("arg is not right")
            if len(arr.shape) != 2 or arr.shape[1] != 2:
                raise ValueError("arg is not right")
            self.cluster = pd.DataFrame(arr, columns=['node', 'cluster'])

    def is_persistent(self):
        return self.path is not None  and utils.file_exists(self.path)
    
    def persistent(self, filepath=None, force=False):
        assert not (self.path is  None  and filepath is None)
        if filepath is None:
            if force: 
                self.save(self.path)
            else:
                raise Exception("already persistent")
        else:
            if self.path is None:
                self.path = utils.abspath(filepath)
                self.save(self.path)
            else:
                if utils.path_equals(self.path, filepath):
                    if force: 
                        self.save(self.path)
                    else:
                        raise Exception("already persistent")
             
    def save(self, filepath, format="parq"):
        assert filepath 
        self.logger.info("Writing " + filepath)
        if format == "parq":
            fastparquet.writer.write(filepath, self.value(), compression="SNAPPY")
        elif format == "csv":
            self.value().to_csv(filepath, index=None)
        else:
            raise ValueError("Error: " + format) 
        
    def value(self):
        if self.cluster is not None: 
            return self.cluster
        else:
            self.logger.info("reading" + self.path)
            df = fastparquet.ParquetFile(self.path).to_pandas()
            self.cluster = df 
            return self.cluster

        
class Dataset(object):

    def __init__(self, name=None, description="", groundtruthObj=None, edgesObj=None, directed=False, weighted=False, overide=False):
        assert edgesObj is not None 
        self.name = name 
        self.description = description
        self.logger = utils.get_logger("{}:{}".format(type(self).__name__, self.name))
        self.directed = directed 
        self.weighted = weighted
         
        self.parq_edges = None
         
        if name:
            assert name 
            self.file_edges = config.get_data_file_path(self.name, 'edges.txt')
            self.file_pajek = config.get_data_file_path(self.name, 'pajek.txt')
            self.file_hig = config.get_data_file_path(self.name, 'pajek.hig')
            self.file_scanbin = config.get_data_file_path(self.name, 'scanbin')
            self.file_anyscan = config.get_data_file_path(self.name, 'anyscan.txt')
            self.file_snap = config.get_data_file_path(self.name, 'snap.bin')
        
        self.set_ground_truth(groundtruthObj)
        self.set_edges(edgesObj)
        
        if name:
            is_persistent = self.is_edges_persistent() and self.is_ground_truth_persistent()
            self.home = config.get_data_file_path(name)
            if utils.file_exists(self.home):
                if overide:
                    utils.remove_if_file_exit(self.home, is_dir=True)
                    utils.create_dir_if_not_exists(self.home)
                elif is_persistent:
                    pass 
                else:
                    raise Exception("Dataset {} exists at {}. Use overide=True or use load it locally.".format(name, self.home))
        
            if not is_persistent:
                self.persistent()
                self.update_meta()
        
    def is_edges_persistent(self):
        return hasattr(self, "parq_edges") and self.parq_edges is not None and utils.file_exists(self.parq_edges)        
    
    def persistent(self):
        if not self.is_edges_persistent():
            filepath = config.get_data_file_path(self.name, 'edges.parq')
            self.persistent_edges(filepath)
        if self.has_ground_truth():
            for k, v in self.get_ground_truth().items():
                if not v.is_persistent():
                    filepath = config.get_data_file_path(self.name, 'gt_{}.parq'.format(k))                
                    v.persistent(filepath)
                
    def persistent_edges(self, filepath=None, force=False):
        assert not (self.parq_edges is  None  and filepath is None)
        if filepath is None:
            if force: 
                self.save_edges(self.path)
            else:
                raise Exception("already persistent")
        else:
            if self.parq_edges is None:
                self.parq_edges = utils.abspath(filepath)
                self.save_edges(self.parq_edges)
            else:
                if utils.path_equals(self.parq_edges, filepath):
                    if force: 
                        self.save_edges(self.parq_edges)
                    else:
                        raise Exception("already persistent")
        
    def save_edges(self, filepath, format="parq"):
        assert filepath 
        self.logger.info("writing" + filepath)
        if format == "parq":
            fastparquet.writer.write(filepath, self.get_edges(), compression="SNAPPY")
        elif format == "csv":
            self.value().to_csv(filepath, index=None)
        else:
            raise ValueError("Error: " + format)
                
    def __repr__(self, *args, **kwargs):
        return self.__str__()
    
    def get_meta(self):
        d = {'name': self.name ,
            'weighted': self.is_weighted(),
             'has_ground_truth':self.has_ground_truth(),
             'directed': self.is_directed()}
        d['parq_edges'] = self.parq_edges
        
        if self.has_ground_truth():
            d['parq_ground_truth'] = {u:v.path for u, v in self.get_ground_truth().items()}
        d['description'] = self.description
        return d 
    
    def is_anonymous(self):
        return False if self.name else True
    
    def update_meta(self):
        if not self.is_anonymous():
            meta_file = config.get_data_file_path(self.name, 'meta.info')
            json.dump(self.get_meta(), open(meta_file, 'wt')) 

    def is_ground_truth_persistent(self):
        if self.has_ground_truth():
            for v in self.get_ground_truth().values():
                if not v.is_persistent():
                    return False 
        return True 

    def set_ground_truth(self, obj):
        if obj is None: return 

        def to_cluster(v):
            if isinstance(v, Cluster):
                return v 
            else:
                return Cluster(v)
        
        if isinstance(obj, dict):
            self.ground_truth = {u:to_cluster(v) for u, v in obj.items()}
        else:
            self.ground_truth = {"default_ground_truth":to_cluster(obj)}

    def set_edges(self, obj):
        v = obj
        if isinstance(v, str):
            self.parq_edges = utils.abspath(v)
            return self 
        else:
            if isinstance(v, pd.DataFrame):
                if not 'src' in v.columns or not 'dest' in v.columns or (self.is_weighted() and 'weight' not in v.columns):
                    raise ValueError("arg is not right")
                if self.is_weighted():
                    self.edges = v[['src', 'dest', 'weight']]
                else:
                    self.edges = v[['src', 'dest']]
            else:  
                if isinstance(v, list):
                    arr = np.array(v)
                elif isinstance(v, np.ndarray):
                    arr = v
                else:
                    raise ValueError("arg is not right")
                if len(arr.shape) != 2  or arr.shape[1] != 2 + int(self.is_weighted()):
                    raise ValueError("arg is not right")
                if self.is_weighted():
                    self.edges = pd.DataFrame(arr, columns=['src', 'dest', 'weight'])
                else:
                    self.edges = pd.DataFrame(arr, columns=['src', 'dest'])
            return self 
                    
    def __str__(self, *args, **kwargs):
        d = self.get_meta()
        return json.dumps(d)
        
    def has_ground_truth(self):
        return hasattr(self, 'ground_truth') and self.ground_truth is not None 
    
    def is_directed(self):
        return  self.directed 
    
    def is_weighted(self):
        return self.weighted
    
    # return edge list
    def get_edges(self):
        if not hasattr(self, 'edges'):
            self.logger.info("reading" + self.parq_edges)
            self.edges = fastparquet.ParquetFile(self.parq_edges).to_pandas() 
        return self.edges            
    
    # return
    def get_ground_truth(self):
        if self.has_ground_truth():
            return self.ground_truth
        return None 
 
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

    def to_higformat(self, filepath=None):
        if (filepath == None):
            filepath = self.file_hig
            if utils.file_exists(filepath):
                return filepath         
        if not utils.file_exists(self.file_pajek): self.to_pajek()
        
        cmd = "python {} {}".format(config.HIG_CONVERT_PROG, self.file_pajek)
        self.logger.info("running " + cmd)
        status = utils.shell_run_and_wait(cmd)
        if (status != 0):
            raise Exception("run command failed: " + str(status))
        return filepath 


def local_exists(name):
    path = config.get_data_file_path(name)
    return  utils.file_exists(path)


def load_local(name):
    path = config.get_data_file_path(name)
    if not utils.file_exists(path):
        raise Exception("path not exists: " + path)
    with open(os.path.join(path, 'meta.info')) as f:
        meta = json.load(f)
    edges = meta['parq_edges']
    gt = None 
    if meta["has_ground_truth"]:
        gt = {k:Cluster(v) for k, v in meta['parq_ground_truth'].items()}
    return Dataset(name=meta['name'], description=meta['description'], groundtruthObj=gt, edgesObj=edges, directed=meta['directed'],
                    weighted=meta['weighted'], overide=False)
    
