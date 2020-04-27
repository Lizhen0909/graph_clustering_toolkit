'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import ClusteringAlg, save_result
from gct import utils, config
import os
import glob
import numpy as np 

prefix = 'alg'


class pg_label_propagation(ClusteringAlg):
    '''
    A wrapper of *LPA* algorithm from PowerGraph. 

    Arguments
        Label Propagation algorithm:
        
        ================================ =======================================================
          --help                         Print this help message.
          --graph arg                    The graph file. Required 
          --execution arg (=synchronous) Execution type (synchronous or asynchronous)
          --saveprefix arg               If set, will save the resultant pagerank to a 
                                         sequence of files with prefix saveprefix
          --ncpus arg (=6)               Number of cpus to use per machine. Defaults to
                                         (#cores - 2)
          --scheduler arg                Supported schedulers are: fifo, sweep, 
                                         priority, queued_fifo. Too see options for 
                                         each scheduler, run the program with the 
                                         option ---schedhelp=[scheduler_name]
          --engine_opts arg              string of engine options i.e., "timeout=100"
          --graph_opts arg               String of graph options i.e., "ingress=random"
          --scheduler_opts arg           String of scheduler options i.e., 
                                         "strict=true"
          --engine_help arg              Display help for engine options.
          --graph_help arg               Display help for the distributed graph.
          --scheduler_help arg           Display help for schedulers.
        ================================ =======================================================
        
    Reference
        Gonzalez, Joseph E., et al. "Powergraph: distributed graph-parallel computation on natural graphs." OSDI. Vol. 12. No. 1. 2012.
    '''    

    def __init__(self, name="powergraph_label_propagation"):
        super(pg_label_propagation, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"powergraph", "name": 'label_propagation' }
    
    def run(self, data, execution='async', ncpus=None, scheduler=None, engine_opts=None, graph_opts=None, scheduler_opts=None, seed=None):
        if seed is not None:self.logger.info("seed ignored")        
        params = locals();del params['self'];del params['data'];del params['seed']
        params = {u:v for u, v in params.items() if v is not None}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        ncpus=utils.get_num_thread(ncpus)
        params['ncpus']=ncpus        
        params['weighted'] =  data.is_weighted()*1
        params['directed'] =  data.is_directed()*1
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            pajek = os.path.join(tmp_dir, 'edges.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_edges, pajek)
            args = " ".join (["--{} {}".format(u, v) for u, v in params.items()])
            cmd = "{} --graph {} --saveprefix=output.cluster {}".format(config.get_powergraph_prog('label_propagation', data.is_directed()), pajek, args)
                        
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
        
            outputfiles = glob.glob(tmp_dir + "/output.cluster.*")
            import pandas as pd 
            df_from_each_file = (pd.read_csv(f, sep="\t", header=None) for f in outputfiles)
            output = pd.concat(df_from_each_file, ignore_index=True)
            output.columns = ['node', 'cluster']
            
        clusters = output[['cluster', 'node']]
        clusters = clusters.groupby('cluster').apply(lambda u: list(u['node'])).to_dict()
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 
        save_result(result)
        self.result = result 
        return self 


class GossipMap(ClusteringAlg):
    '''
    A wrapper of *GossipMap* algorithm from https://github.com/uwescience/GossipMap. 

    Arguments
        GossipMap Algorithm:
        
        ================================ =======================================================
          --help                              Print this help message.
          --graph arg                         The graph file. Required.
          --format arg (=snap)                The graph file format.
          --thresh arg (=0.001)               The threshold for convergence condition.
          --tol arg (=1.00e-15)               The threshold for pagerank (ergodic 
                                              state) convergence condition.
          --maxiter arg (=10)                 The maximum of the iteration for finding 
                                              community.
          --maxspiter arg (=3)                The maximum of the iteration of sp-graph 
                                              for finding community.
          --trials arg (=1)                   The number of trials for finding 
                                              community repeatedly.
          --interval arg (=3)                 The time interval for checking whether 
                                              the received message is valid or not.
          --mode arg (=1)                     The running mode of finding community: 1 
                                              - coreOnce, 2 - coreRepeat.
          --outmode arg (=2)                  The running outerloop mode of finding 
                                              community: 1 - outerOnce, 2 - 
                                              outerRepeat.
          --prefix arg                        If set, this app will save the community 
                                              detection result.
          --ncpus arg (=6)                    Number of cpus to use per machine. 
                                              Defaults to (#cores - 2)
          --scheduler arg                     Supported schedulers are: fifo, sweep, 
                                              priority, queued_fifo. Too see options 
                                              for each scheduler, run the program with 
                                              the option ---schedhelp=[scheduler_name]
          --engine_opts arg                   string of engine options i.e., 
                                              "timeout=100"
          --graph_opts arg                    String of graph options i.e., 
                                              "ingress=random"
          --scheduler_opts arg                String of scheduler options i.e., 
                                              "strict=true"
          --engine_help arg                   Display help for engine options.
          --graph_help arg                    Display help for the distributed graph.
          --scheduler_help arg                Display help for schedulers.
        ================================ =======================================================

    Reference
        Bae, Seung-Hee, and Bill Howe. "GossipMap: A distributed community detection algorithm for billion-edge directed graphs." High Performance Computing, Networking, Storage and Analysis, 2015 SC-International Conference for. IEEE, 2015.
    '''    

    def __init__(self, name="powergraph_GossipMap"):
        super(GossipMap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"powergraph", "name": 'GossipMap' }
    
    def run(self, data, thresh=None, tol=None, maxiter=None, maxspiter=None, trials=None, interval=None, outmode=None, 
            ncpus=None, scheduler=None, engine_opts=None, graph_opts=None, scheduler_opts=None, seed=None):
        if seed is not None:self.logger.info("seed ignored")
        params = locals();del params['self'];del params['data']; del params['seed']
        params = {u:v for u, v in params.items() if v is not None}
        ncpus=utils.get_num_thread(ncpus)
        params['ncpus']=ncpus
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            pajek = os.path.join(tmp_dir, 'edges.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_edges, pajek)
            args = " ".join (["--{} {}".format(u, v) for u, v in params.items()])
            cmd = "{} --graph {} --prefix output.cluster {}".format(config.get_powergraph_prog('GossipMap', data.is_directed()),
                                                                    pajek, args).strip()
                        
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
        
            outputfiles = glob.glob(tmp_dir + "/output.cluster*")
            import pandas as pd 
            df_from_each_file = [pd.read_csv(f, sep="\t", header=None) for f in outputfiles]
            output = pd.concat(df_from_each_file, ignore_index=True)
            output.columns = ['node', 'cluster', 'score']
            
        clusters = output[['cluster', 'node']]
        clusters = clusters.groupby('cluster').apply(lambda u: list(u['node'])).to_dict()
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 
        save_result(result)
        self.result = result 
        return self 


class RelaxMap(ClusteringAlg):
    '''
    A wrapper of *RelaxMap* algorithm from https://github.com/uwescience/RelaxMap. 

    Arguments
    
        ==========   =======================================================
    
        args[0]:     seed - random seed value for generating random sequential order of vertices for each iteration.
        args[1]:     network data - the input graph data.
                     RelaxMap supports 1) pajek format (.net) and 2) edge list format (.txt).
        args[2]:     # thread - the number of threads
        args[3]:     # attempts - the number of attempts.
                     (this is not applied yet, so it only return with 1 attempt.)
        args[4]:     threshold - the stop condition threshold (recommended 1e-3 or 1e-4)
        args[5]:     vThresh - the threshold value for each vertex movement (recommended 0.0) 
        args[6]:     maxIter - the number of maximum iteration for each super-step.
        args[7]:     outDir - the directory where the output files will be located.
        args[8]:     prior/normal flag - apply the prioritized search for efficient runs (prior) or not (normal).
        ==========   =======================================================
        
    Reference
        Seung-Hee Bae, Daniel Halperin, Jevin West, Martin Rosvall, and Bill Howe, 
        "Scalable Flow-Based Community Detection for Large-Scale Network Analysis,"
        In Proceedings of IEEE 13th International Conference on Data Mining Workshop (ICDMW), 2013
    '''    

    def __init__(self, name="RelaxMap"):
        super(RelaxMap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"RelaxMap", "name": 'RelaxMap' }
    
    def run(self, data, seed=None, thread=None, threshold=1e-3, vThresh=0.0, maxIter=10, prior=True):
        if seed is None:
            seed = np.random.randint(999999)
        params = locals();del params['self'];del params['data']
        params = {u:v for u, v in params.items() if v is not None}                    
        thread = utils.get_num_thread(thread)
        params['thread'] = thread 
        
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            pajek = utils.link_file(data.file_edges, tmp_dir, 'edges.txt')
            cmd = "{prog} {seed} {graph} {thread} 1 {threshold} {vThresh} {maxIter} {output_dir} {prior}"\
                .format(prog=config.get_powergraph_prog('RelaxMap', data.is_directed()), seed=seed,
                        graph=pajek, thread=thread, threshold=threshold, vThresh=vThresh, output_dir=tmp_dir,
                        maxIter=maxIter, prior='prior' if prior else 'normal').strip()
                        
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
        
            outputfile = os.path.join(tmp_dir , "edges.tree")
            import pandas as pd 
            output = pd.read_csv(outputfile, sep=" ", header=None, skiprows=1)
            output['node'] = output.loc[:, 2].astype(np.int)
            output['cluster'] = output.loc[:, 0].map(lambda u: u.split(':')[0]).astype(np.int)
            
        clusters = output[['cluster', 'node']]
        clusters = clusters.groupby('cluster').apply(lambda u: list(u['node'])).to_dict()
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 
        save_result(result)
        self.result = result 
        return self 
