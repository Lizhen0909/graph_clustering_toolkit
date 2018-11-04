'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os
import glob
import multiprocessing


class Scanpp(Clustering):
    '''
    A wrapper of *scan++* algorithm  

    Arguments
    --------------------
    option    arguments (Default)    description
    -e    Real number between 0 and 1 (Default: 0)    Set the epsilon parameter for the clustering.
    -m    Natural number (Default: 1)    Set the mu parameter for the clustering.
    -v    No arguments are required.    Display statistics of the clustering.
    -r    No arguments are required.    Display the clustering results.
    
    Reference
    ------------------------
    Shiokawa H, Fujiwara Y, Onizuka M. SCAN++: efficient algorithm for finding clusters, hubs and outliers on large-scale graphs[J]. Proceedings of the VLDB Endowment, 2015, 8(11): 1178-1189.
    '''   
    def __init__(self, name="scanpp"):
        super(Scanpp, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"scanpp (no code)", "name": 'scanpp' }
    
    def run(self, data, mu=1, epsilon=0):
        params = {'mu':mu, 'epsilon':epsilon}
        if (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        cmd = "{} -e {} -m {} -r {}".format(config.SCANPP_PROG, epsilon, mu, data.file_edges)
        self.logger.info("Running " + cmd)
        timecost, output = utils.timeit(lambda: utils.check_output(cmd.split(" ")))
        if not output.startswith('node'):
            raise Exception("Something wrong with scapp. output:\n" + output)

        output = [u.strip() for u in output.split("\n")][1:]
        output = [u.split("\t") for u in output if u]
        output = [[int(v) for v in u] for u in output]
        
        from collections import defaultdict
        clusters = defaultdict(list)
        for n, c in output:
            clusters[c].append(n)
        
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['algname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
    def get_result(self):
        if hasattr(self, 'result'):
            return self.result
        else:
            raise Exception("No result found. probably no run has been done")


class AnyScan(Clustering):
    '''
    A wrapper of *anyscan* algorithm  

    Arguments
    --------------------
    Usage: ./anyscan [switches] -i filename -m minpts -e epsilon -o output -t threads
            -c algorithm: algorithm used 
            -i filename     : file containing input data to be clustered
            -g gname        : file containing ground truth 
            -m minpts       : input parameter of DBSCAN, min points to form a cluster, e.g. 2
            -e epsilon      : input parameter of DBSCAN, radius or threshold on neighbourhoods retrieved, e.g. 0.8
            -o output       : clustering results, format, (each line, point id, clusterid)
            -a alpha    : block size alpha 
            -b beta     : block size beta 
            -t threads      : number of threads to be employed

    
    Reference
    ------------------------
    Mai S T, Dieu M S, Assent I, et al. Scalable and Interactive Graph Clustering Algorithm on Multicore CPUs[C]//Data Engineering (ICDE), 2017 IEEE 33rd International Conference on. IEEE, 2017: 349-360
    '''   
    def __init__(self, name="anyScan"):
        super(AnyScan, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"anyScan (no code)", "name": 'anyScan' }
    
    '''
    1) Parameters
    
        "Usage: %s [switches] -i filename -m minpts -e epsilon -o output -t threads\n"
                "    -c algorithm: algorithm used \n"
                "    -i filename    : file containing input data to be clustered\n"
                "    -g gname     : file containing ground truth \n"
                "    -m minpts    : input parameter of DBSCAN, min points to form a cluster, e.g. 2\n"
                "    -e epsilon    : input parameter of DBSCAN, radius or threshold on neighbourhoods retrieved, e.g. 0.8\n"
                "    -o output    : clustering results, format, (each line, point id, clusterid)\n"
                "    -a alpha    : block size alpha \n"
                "    -b beta     : block size beta \n"
                "    -t threads    : number of threads to be employed\n\n";
    
    Example:
    
    ./anyscan -c 5 -i test04.adj -g label.gold -o out.txt -m 4 -e 0.5 -a 32768 -b 32768 -t 8
    
    Ground truth and output can be ignored.
    
    The algorithm 
    
    c = 1 : The orginal SCAN algorithm
    c = 2 : The algorithm pSCAN
    c = 3 : The anytime SCAN algorithm (anyscan)
    c = 4 : AnySCAN in parallel
    c = 5 : Ideal parallel SCAN
    
    AnySCAN uses ltcmalloc for aiding the memory allocation. 
    '''    

    def run(self, data, algorithm=4, minpts=4, epsilon=0.5, alpha=32768 , beta=32768 , thread=-1):
        params = locals()
        del(params['self']);del(params['data'])
        if thread < 1: 
            thread = multiprocessing.cpu_count()
            params['thread'] = thread 

        if (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_anyscan):
            data.to_anyscan()
        
        cmd = "{} -c {} -i {} -m {} -e {} -o {} -a {} -b {} -t {}".format(
            config.ANYSCAN_PROG, algorithm, data.file_anyscan, minpts, epsilon, 'output', alpha, beta, thread)
        self.logger.info("Running " + cmd)

        with utils.TempDir() as tmp_dir:
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 1:  # anyscan always return 1
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as output:
                lines = [u.strip() for u in output.readlines()]
                
            n_nodes = int(lines[0])
            clusters_list = lines[1].split(" ")
            clusters_list = [int(u) for u in clusters_list ]
            
        if (n_nodes != len(clusters_list)):
            raise Exception("#node is not equals #cluster")
            
        from collections import defaultdict
        clusters = defaultdict(list)
        for n, c in enumerate(clusters_list):
            clusters[c].append(n)
        
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['algname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
    def get_result(self):
        if hasattr(self, 'result'):
            return self.result
        else:
            raise Exception("No result found. probably no run has been done")


class pScan(Clustering):
    '''
    A wrapper of *pScan, ppScan, ppScanSSE* algorithm  

    Arguments
    --------------------
    prog:         one of pScan, ppScan, ppScanSSE
    epsilon:     similarity-threshold 
    mu:         density-threshold
    
    Reference
    ------------------------
    Chang L, Li W, Qin L, et al. $\mathsf {pSCAN} $: Fast and Exact Structural Graph Clustering[J]. IEEE Transactions on Knowledge and Data Engineering, 2017, 29(2): 387-401.
    Yulin Che, Shixuan Sun, Qiong Luo. 2018. Parallelizing Pruning-based Graph Structural Clustering. In ICPP 2018: 47th International Conference on Parallel Processing, August 13–16, 2018, Eugene, OR, USA. ACM, New York, NY, USA    
    '''   

    def __init__(self, name="pScan"):
        super(pScan, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"pScan (has code)", "name": 'pScan or ppScan or ppScanSSE' }

    def run(self, data, mu=1, epsilon=0, prog='pScan'):
        assert prog in ['pScan', 'ppScan', 'ppScanSSE']
        
        params = {'mu':mu, 'epsilon':epsilon, 'prog':prog}
        if (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_scanbin):
            data.to_scanbin()
        
        with utils.TempDir() as tmp_dir:
            scanbin = data.file_scanbin 
            os.symlink(os.path.join(scanbin, 'b_degree.bin'), os.path.join(tmp_dir, 'b_degree.bin'))
            os.symlink(os.path.join(scanbin, 'b_adj.bin'), os.path.join(tmp_dir, 'b_adj.bin'))
            if prog == 'pScan':
                EXE = config.PSCAN_PROG
            elif prog == 'ppScan':
                EXE = config.PPSCAN_PROG                
            elif prog == 'ppScanSSE':
                EXE = config.PPSCANSSE_PROG                
            cmd = "{} {} {} {} {}".format(EXE, tmp_dir, epsilon, mu, 'output')
            self.logger.info("Running " + cmd)
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfile = glob.glob(tmp_dir + "/result-*-*.txt")[0]
            import pandas as pd 
            output = pd.read_csv(outputfile, sep=" ")
        
        clusters = output[output['c/n'] == 'c'][['vertex_id', 'cluster_id']]
        others = output[output['c/n'] != 'c'][['vertex_id', 'cluster_id']]
        clusters = clusters.groupby('cluster_id').apply(lambda u: list(u['vertex_id'])).to_dict()
        others = others.values.tolist()

        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['algname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 
        result['noise_or_hub'] = others 
        save_result(result)
        self.result = result 
        return self 
            
        return self 
    
    def get_result(self):
        if hasattr(self, 'result'):
            return self.result
        else:
            raise Exception("No result found. probably no run has been done")
