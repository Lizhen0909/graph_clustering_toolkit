from gct import utils, config
import pandas as pd
import numpy as np  
import snap 
import os
from gct.dataset.dataset import Dataset, local_exists, load_local
 
    
class RandomGenerator():        

    def __init__(self, params=None):
        assert params is not None 
        self.params = params 
        self.logger = utils.get_logger("{}:{}".format(type(self).__name__, params["name"]))
    
    def generate(self, seed=None):
        params = self.params
        if params['name'] == 'Erdos-Renyi':
            gtype = snap.PNGraph if params['directed'] else snap.PUNGraph
            g = snap.GenRndGnm(gtype , params['n_node'], params['n_edge'])
            lst = [] 
            for EI in g.Edges():
                lst.append([EI.GetSrcNId(), EI.GetDstNId()])
            return pd.DataFrame(lst, columns=['src', 'dest']), None 
        elif params['name'] == 'ovp_LFR':
            if seed is None:
                seed = np.random.randint(999999)
            with utils.TempDir() as tmpdir:
                with open(os.path.join(tmpdir, "seed.txt"), 'wt') as seedf :
                    seedf.write(str(seed))
                program = config.LFR_PROG
                newparams = dict(self.params)
                if 'directed' in newparams: del newparams['directed']
                if 'weighted' in newparams: del newparams['weighted']
                newparams['name']='LFR'
                cmd = program + " " + " ".join([ "-" + str(u[0]) + " " + str(u[1]) for u in newparams.items() if u[1] is not None])
                self.logger.info("Runing '{}' with seed {}".format(cmd, seed))
                self.logger.info("working dir: " + tmpdir)
                status = utils.shell_run_and_wait(cmd, working_dir=tmpdir)
                if status != 0:
                    raise Exception("run command failed. status={}".format(status))

                edgefile = "LFR.nsa" if self.params['directed'] else "LFR.nse"
                edgefile = os.path.join(tmpdir, edgefile)
                if self.params['weighted']:
                    edges = pd.read_csv(edgefile, sep='\t', header=None, skiprows=1, dtype={2:np.float})
                    edges.columns = ['src', 'dest', 'weight']                    
                else:
                    edges = pd.read_csv(edgefile, sep='\t', header=None, skiprows=1, usecols=[0, 1])
                    edges.columns = ['src', 'dest']
                
                gtfile = "LFR.nmc"
                gtfile = os.path.join(tmpdir, gtfile)
                gt = pd.read_csv(gtfile, sep='\t', header=None)
                gt.columns = ['node', 'cluster']
                return self.make_offset_0(edges, gt)   
        else :
            raise Exception("unknown " + params['name'])
    
    def make_offset_0(self, edges, gt):
        min_node = edges[['src', 'dest']].min().min()
        if min_node != 0:
            self.logger.info("min node is {}. will make it 0".format(min_node))
            edges['src'] = edges['src'] - min_node
            edges['dest'] = edges['dest'] - min_node
            if gt is not None:
                gt['node'] = gt['node'] - min_node 
            return edges, gt
        else:
            return edges, gt


def generate_Erdos_Renyi(name, n_node, n_edge, directed=False, seed=None, overide=False):
    '''
    Generates an Erdos-Renyi random graph of the specified GraphType.
    '''
    if not overide and local_exists(name):
        return load_local(name)
    else:
        params = {"name":"Erdos-Renyi", 'n_node':n_node, "n_edge":n_edge, "directed": directed}
        description = "Erdos_Renyi random graph"
        weighted = False 
        gen = RandomGenerator(params=params)
        edges, gt = gen.generate(seed)    
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges, directed=directed, weighted=weighted, overide=overide)


def generate_ovp_LFR(name, N, k=None, maxk=None, mut=None, muw=None, beta=None, t1=None, t2=None, minc=None, maxc=None,
                 on=None, om=None, C=None, a=0, weighted=False, seed=None, overide=False):
    '''
    Extended version of the Lancichinetti-Fortunato-Radicchi Benchmark for Undirected Weighted Overlapping networks 
    to evaluate clustering algorithms using generated ground-truth communities.
    
    Refer https://github.com/eXascaleInfolab/LFR-Benchmark_UndirWeightOvp

    Parameter
    ----------------
   
    To set the parameters, type:
    -N        [number of nodes]
    -k        [average degree]
    -maxk        [maximum degree]
    -mut        [mixing parameter for the topology]
    -muw        [mixing parameter for the weights]
    -beta        [exponent for the weight distribution]
    -t1        [minus exponent for the degree sequence]
    -t2        [minus exponent for the community size distribution]
    -minc        [minimum for the community sizes]
    -maxc        [maximum for the community sizes]
    -on        [number of overlapping nodes]
    -om        [number of memberships of the overlapping nodes]
    -C        [Average clustering coefficient]
    -cnl        [output communities as strings of nodes (input format for NMI evaluation)]
    -name        [base name for the output files]. It is used for the network, communities and statistics; files extensions are added automatically:
        .nsa  - network, represented by space/tab separated arcs
        .nse  - network, represented by space/tab separated edges
        {.cnl, .nmc}  - communities, represented by nodes lists '.cnl' if '-cnl' is used, otherwise as a nodes membership in communities '.nmc')
        .nst  - network statistics
    -seed        [file name of the random seed, default: seed.txt]
    -a        [{0, 1} yield directed network (1 - arcs) rather than undirected (0 - edges), default: 0 - edges]
    
    Reference
    -------------
    Lancichinetti, Andrea, and Santo Fortunato. "Benchmarks for testing community detection algorithms on directed and weighted graphs with overlapping communities." Physical Review E 80.1 (2009): 016118.
    '''    
    if not overide and local_exists(name):
        return load_local(name)
    else:
        params = locals()
        del params['overide']
        params['a'] = int(a)
        params['name'] = 'ovp_LFR'
        description = "overlap LFR random graph"
        directed = (a > 0)
        params['directed'] = directed
        gen = RandomGenerator(params=params)
        edges, gt = gen.generate(seed)    
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges, directed=directed, weighted=weighted, overide=overide)

