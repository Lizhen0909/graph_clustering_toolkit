'''
Created on Oct 27, 2018
include a few algorithms mentioned at https://github.com/eXascaleInfolab/PyCABeM
@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os
import json
import glob

prefix='pycabem'

class HiReCS(Clustering):
    '''
    A wrapper of *hirecs* algorithm from http://www.lumais.com/hirecs. 

    Arguments
    --------------------
    Usage: ./hirecs [-o{t,c,j}] [-f] [-r] [-m<float>] <adjacency_matrix.hig>
      -o  - output data format. Default: t
        t  - text like representation for logs
        c  - CSV like representation for parcing
        j  - JSON represenation
        je  - extended JSON represenation (j + unwrap root clusters to nodes)
        jd  - detaile JSON represenation (je + show inter-cluster links)
      -c  - clean links, skip links validation
      -f  - fast quazy-mutual clustering (faster). Default: strictly-mutual (better)
      -r  - rand reorder (shuffle) nodes and links on nodes construction
      -m<float>  - modularity profit margin for early exit, float E [-1, 1]. Default: -0.999, but on practice >~= 0
        -1  - skip stderr tracing after each iteration. Recommended: 1E-6 or 0
        
    Reference
    ------------------------
    Cannot find any publication. Please refer to http://www.lumais.com/hirecs
    
    '''

    def __init__(self, name="HiReCS"):
        
        super(HiReCS, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"HiReCS", "name": 'HiReCS' }


    def run(self, data, f=False, m=None):
        
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params = {}
        params['f'] = f
        params['m'] = m 
        
        if not utils.file_exists(data.file_hig):
            data.to_higformat()
        cmd = ["./hirecs"]
        cmd.append("-oje")
        if f: cmd.append('-f')
        if m is not None: cmd.append("-m{}".format(m))
        cmd.append(data.file_hig)
        cmd.append("> output")
        cmd = " ".join(cmd)
        with utils.TempDir() as tmp_dir:
            with open(os.path.join(tmp_dir, "tmpcmd"), 'wt') as f: f.write(cmd)
            self.logger.info("Running " + cmd)
            cmd = "bash tmpcmd" 
            
            utils.link_file(os.path.join(config.HIRECS_PATH, 'hirecs'), tmp_dir)
            utils.link_file(os.path.join(config.HIRECS_PATH, 'libhirecs.so'), tmp_dir)
            utils.link_file(data.file_hig, tmp_dir)
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as f:
                output = json.load(f)
                
            mod = output['mod']
            communities = output['communities']
            
            clusters = {}
            for c in communities:
                clusters[int(c)] = [int(u) for u in communities[c].keys()]
        
        self.logger.info("Made %d clusters in %f seconds with modularity %f" % (len(clusters), timecost, mod))

        result = {}
        result['algname'] = self.name
        result['params'] = params
        result['overlap'] = True
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 

    
class LabelRank(Clustering):
    '''
    A wrapper of *LabelRank* algorithm from https://sites.google.com/site/communitydetectionslpa/. 

    Arguments
    --------------------
    > LabelRank netName cutoff_r inflation_in NBDisimilarity_q
    
    Reference
    ------------------------
    J. Xie, B. K. Szymanski, "LabelRank: A Stabilized Label Propagation Algorithm for Community Detection in Networks", IEEE NSW, West point, NY, 2013
    
    '''
    def __init__(self, name="LabelRank"):
        
        super(LabelRank, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"GANXiS", "name": 'LabelRank' }

    def run(self, data, cutoff_r=0.01, inflation_in=2, NBDisimilarity_q=0.3):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params = locals();del params['self'];del params['data']

        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        cmd = "{} {} {} {} {}".format(config.LABLE_RANK_PROG, "edges.txt", cutoff_r, inflation_in, NBDisimilarity_q)
        with utils.TempDir() as tmp_dir:
            utils.remove_if_file_exit(os.path.join(tmp_dir, "output"), True)
            utils.create_dir_if_not_exists(os.path.join(tmp_dir, "output"))
            self.logger.info("Running " + cmd)
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            outputfile = glob.glob(os.path.join(tmp_dir, "output/LabelRank*.icpm"))[0]
            clusters = []
            with open (os.path.join(tmp_dir, outputfile), "r") as f:
                for line in f: 
                    clusters.append([int(u) for u in line.strip().split(" ")])
            clusters = dict(enumerate(clusters))
        
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

'''
GANXiSw 3.0.2(used to be SLPAw) is for weighted (directed) networks, version=3.0.2
Usage: java -jar GANXiSw.jar -i networkfile
Options:
  -i input network file
  -d output director (default: output)
  -L set to 1 to use only the largest connected component
  -t maximum iteration (default: 100)
  -run number of repetitions
  -r a specific threshold in [0,0.5]
  -ov set to 0 to perform disjoint detection
  -W treat the input as a weighted network, set 0 to ignore the weights(default 1)
  -Sym set to 1 to make the edges symmetric/bi-directional (default 0)
  -seed user specified seed for random generator
  -help to display usage info
 -----------------------------Advanced Parameters---------------------------------
  -v weighted version in {1,2,3}, default=3
  -Oov set to 1 to output overlapping file, default=0
  -Onc set to 1 to output <nodeID communityID> format, 2 to output <communityID nodeID> format
  -minC min community size threshold, default=2
  -maxC max community size threshold
  -ev embedded SLPAw's weighted version in {1,2,3}, default=1
  -loopfactor determine the num of loops for depomposing each large com, default=1.0
  -Ohis1 set to 1 to output histgram Level1
  -Ohis2 set to 1 to output histgram Level2

  -OMem1 set to 1 to output each node's memory content at Level 1
  -EC evolution cutoff, a real value > 1.0 
NOTE: 1. more parameters refer to Readme.pdf
      2. parameters are *CASE-SENSITIVE*, e.g., -Onc is not -onc

'''


class GANXiSw(Clustering):
    '''
    
    A wrapper of *GANXiSw* algorithm from https://sites.google.com/site/communitydetectionslpa/. 

    Arguments
    --------------------
    GANXiSw 3.0.2(used to be SLPAw) is for weighted (directed) networks, version=3.0.2
    Usage: java -jar GANXiSw.jar -i networkfile
    Options:
      -i input network file
      -d output director (default: output)
      -L set to 1 to use only the largest connected component
      -t maximum iteration (default: 100)
      -run number of repetitions
      -r a specific threshold in [0,0.5]
      -ov set to 0 to perform disjoint detection
      -W treat the input as a weighted network, set 0 to ignore the weights(default 1)
      -Sym set to 1 to make the edges symmetric/bi-directional (default 0)
      -seed user specified seed for random generator
      -help to display usage info
     -----------------------------Advanced Parameters---------------------------------
      -v weighted version in {1,2,3}, default=3
      -Oov set to 1 to output overlapping file, default=0
      -Onc set to 1 to output <nodeID communityID> format, 2 to output <communityID nodeID> format
      -minC min community size threshold, default=2
      -maxC max community size threshold
      -ev embedded SLPAw's weighted version in {1,2,3}, default=1
      -loopfactor determine the num of loops for depomposing each large com, default=1.0
      -Ohis1 set to 1 to output histgram Level1
      -Ohis2 set to 1 to output histgram Level2
    
      -OMem1 set to 1 to output each node's memory content at Level 1
      -EC evolution cutoff, a real value > 1.0 
    NOTE: 1. more parameters refer to Readme.pdf
          2. parameters are *CASE-SENSITIVE*, e.g., -Onc is not -onc
          
    
    Reference
    ------------------------
    J. Xie, B. K. Szymanski and X. Liu, "SLPA: Uncovering Overlapping Communities in Social Networks via A Speaker-listener Interaction Dynamic Process"
    
    '''

    def __init__(self, name="GANXiSw"):
        
        super(GANXiSw, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"GANXiS", "name": 'GANXiSw' }

    '''
       pass args with key=val. Don't use i, d, Sym.
    '''
    def run(self, data, **kwargs):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params = dict(kwargs)
        params = {k:v for k, v in params.items() if v is not None }
        if not data.is_directed():
            params['Sym'] = 1
        params['d'] = "output"
        if "r" not in params: params['r'] = 0.1

        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        txt_params = " ".join(["-{} {}".format(k, v) for k, v in params.items()]) 
        cmd = "java -jar {} -i {} {} ".format(config.GANXISW_PROG, "edges.txt", txt_params)
        with utils.TempDir() as tmp_dir:
            utils.remove_if_file_exit(os.path.join(tmp_dir, "output"), True)
            utils.create_dir_if_not_exists(os.path.join(tmp_dir, "output"))
            self.logger.info("Running " + cmd)
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            outputfile = glob.glob(os.path.join(tmp_dir, "output/SLPAw*.icpm"))[0]
            clusters = []
            with open (os.path.join(tmp_dir, outputfile), "r") as f:
                for line in f: 
                    clusters.append([int(u) for u in line.strip().split(" ")])
            clusters = dict(enumerate(clusters))
        
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
    
