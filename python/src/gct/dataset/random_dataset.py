from gct import utils, config
import pandas as pd
import numpy as np  
import snap 
import os
from gct.dataset.dataset import local_exists, load_local
 
    
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
                newparams['name'] = 'LFR'
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
        elif params['name'] == 'LFR':
            if seed is None:
                seed = np.random.randint(999999)
            with utils.TempDir() as tmpdir:
                with open(os.path.join(tmpdir, "time_seed.dat"), 'wt') as seedf :
                    seedf.write(str(seed))
                program = config.get_LFR_prog(weighted=params['weighted'], directed=params['directed'], hier='hier' in params and params['hier'])
                newparams = dict(self.params)
                if 'directed' in newparams: del newparams['directed']
                if 'weighted' in newparams: del newparams['weighted']
                if 'name' in newparams: del newparams['name']
                if 'hier' in newparams: del newparams['hier']
                cmd = program + " " + " ".join([ "-" + str(u[0]) + " " + str(u[1]) for u in newparams.items() if u[1] is not None])
                self.logger.info("Runing '{}'  with seed {}".format(cmd, seed))
                self.logger.info("working dir: " + tmpdir)
                status = utils.shell_run_and_wait(cmd, working_dir=tmpdir)
                if status != 0:
                    raise Exception("run command failed. status={} with seed {}".format(status, seed))

                edgefile = "network.dat"
                edgefile = os.path.join(tmpdir, edgefile)
                if self.params['weighted']:
                    edges = pd.read_csv(edgefile, sep='\t', header=None, skiprows=1, dtype={2:np.float})
                    edges.columns = ['src', 'dest', 'weight']                    
                else:
                    edges = pd.read_csv(edgefile, sep='\t', header=None, skiprows=1)
                    edges.columns = ['src', 'dest']
                
                def read_comm(fname):
                    gtfile = fname
                    gtfile = os.path.join(tmpdir, gtfile)
                    gt = pd.read_csv(gtfile, sep='\t', header=None)
                    gt.columns = ['node', 'cluster']
                    return gt

                if 'hier' in params and  params['hier']:
                    gt = read_comm("community_first_level.dat"), read_comm("community_second_level.dat")
                else: 
                    gt = read_comm("community.dat")
                
                return self.make_offset_0(edges, gt)   
               
        else :
            raise Exception("unknown " + params['name'])
    
    def make_offset_0(self, edges, gt):
        min_node = edges[['src', 'dest']].min().min()
        if min_node != 0:
            self.logger.info("min node is {}. will make it 0".format(min_node))
            edges['src'] = edges['src'] - min_node
            edges['dest'] = edges['dest'] - min_node

            def f(df):
                df['node'] = df['node'] - min_node
                return df 

            if gt is not None:            
                if isinstance(gt, tuple):
                    gt = tuple([f(u) for u in gt])
                else:
                    gt = f(gt) 
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
        from .dataset import Dataset 
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges, \
                       directed=directed, weighted=weighted, overide=overide, additional_meta={'genopts': params})


def generate_ovp_LFR(name, N, k=None, maxk=None, mut=None, muw=None, beta=None, t1=None, t2=None, minc=None, maxc=None,
                 on=None, om=None, C=None, a=0, weighted=False, seed=None, overide=False):
    '''
    Extended version of the Lancichinetti-Fortunato-Radicchi Benchmark for Weighted Overlapping networks 
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
        from .dataset import Dataset 
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges, \
                       directed=directed, weighted=weighted, overide=overide, additional_meta={'genopts': params})


def generate_undirected_unweighted_random_graph_LFR(name, N, k=None, maxk=None, mu=None, t1=None, t2=None, minc=None, \
                maxc=None, on=None, om=None, C=None, seed=None, overide=False):
    '''
    Lancichinetti-Fortunato-Radicchi Benchmark geneartor. Original from https://sites.google.com/site/andrealancichinetti/files  
    
    Parameter:
    ------------------
    To set the parameters, type:
    
    -N              [number of nodes]
    -k              [average degree]
    -maxk           [maximum degree]
    -mu             [mixing parameter]
    -t1             [minus exponent for the degree sequence]
    -t2             [minus exponent for the community size distribution]
    -minc           [minimum for the community sizes]
    -maxc           [maximum for the community sizes]
    -on             [number of overlapping nodes]
    -om             [number of memberships of the overlapping nodes]
    -C              [Average clustering coefficient]
    ----------------------
    
    It is also possible to set the parameters writing flags and relative numbers in a file. To specify the file, use the option:
    -f      [filename]
    You can set the parameters both writing some of them in the file, and using flags from the command line for others.
    
    -N, -k, -maxk, -mu have to be specified. For the others, the program can use default values:
    t1=2, t2=1, on=0, om=0, minc and maxc will be chosen close to the degree sequence extremes.
    If you don't specify -C the rewiring process for raising the average clustering coefficient will not be performed
    If you set a parameter twice, the latter one will be taken.
    
    -------------------- Other options ---------------------------
    
    To have a random network use:
    -rand
    Using this option will set mu=0, and minc=maxc=N, i.e. there will be one only community.
    Use option -sup (-inf) if you want to produce a benchmark whose distribution of the ratio of external degree/total degree is superiorly (inferiorly) bounded by the mixing parameter.
    
    -------------------- Examples ---------------------------
    
    Example1:
    ./benchmark -N 1000 -k 15 -maxk 50 -mu 0.1 -minc 20 -maxc 50 -C 0.7
    Example2:
    ./benchmark -f flags.dat -t1 3
      
    '''
    if not overide and local_exists(name):
        return load_local(name)
    else:
        params = locals()
        del params['overide']
        
        description = "LFR random graph"
        directed = False
        weighted = False 
        params['directed'] = directed
        params['weighted'] = weighted
        params['name'] = 'LFR'
        gen = RandomGenerator(params=params)
        edges, gt = gen.generate(seed)    
        from .dataset import Dataset
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges,\
                        directed=directed, weighted=weighted, overide=overide, additional_meta={'genopts': params})


def generate_directed_unweighted_random_graph_LFR(name, N, k=None, maxk=None, mu=None, t1=None, t2=None, minc=None, \
                maxc=None, on=None, om=None, C=None, seed=None, overide=False):
    '''
    Lancichinetti-Fortunato-Radicchi Benchmark geneartor. Original from https://sites.google.com/site/andrealancichinetti/files  
    
    Parameter:
    ----------------------
    
    To set the parameters, type:
    
    -N              [number of nodes]
    -k              [average in-degree]
    -maxk           [maximum in-degree]
    -mu             [mixing parameter]
    -t1             [minus exponent for the degree sequence]
    -t2             [minus exponent for the community size distribution]
    -minc           [minimum for the community sizes]
    -maxc           [maximum for the community sizes]
    -on             [number of overlapping nodes]
    -om             [number of memberships of the overlapping nodes]
    ----------------------
    
    It is also possible to set the parameters writing flags and relative numbers in a file. To specify the file, use the option:
    -f      [filename]
    You can set the parameters both writing some of them in the file, and using flags from the command line for others.
    
    -N, -k, -maxk, -mu have to be specified. For the others, the program can use default values:
    t1=2, t2=1, on=0, om=0, minc and maxc will be chosen close to the degree sequence extremes.
    If you set a parameter twice, the latter one will be taken.
    
    -------------------- Other options ---------------------------
    
    To have a random network use:
    -rand
    Using this option will set mu=0, and minc=maxc=N, i.e. there will be one only community.
    Use option -sup (-inf) if you want to produce a benchmark whose distribution of the ratio of external in-degree/total in-degree is superiorly (inferiorly) bounded by the mixing parameter.
    
    -------------------- Examples ---------------------------
    
    Example1:
    ./benchmark -N 1000 -k 15 -maxk 50 -mu 0.1 -minc 20 -maxc 50
    Example2:
    ./benchmark -f flags.dat -t1 3

      
    '''
    if not overide and local_exists(name):
        return load_local(name)
    else:
        params = locals()
        del params['overide']
        
        description = "LFR random graph"
        directed = True 
        weighted = False 
        params['directed'] = directed
        params['weighted'] = weighted
        params['name'] = 'LFR'
        gen = RandomGenerator(params=params)
        edges, gt = gen.generate(seed)
        from .dataset import Dataset    
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges, \
                       directed=directed, weighted=weighted, overide=overide, additional_meta={'genopts': params})


def generate_undirected_weighted_random_graph_LFR(name, N, k=None, maxk=None, mut=None, muw=None, t1=None, t2=None, \
                minc=None, maxc=None, on=None, om=None, C=None, seed=None, overide=False):
    '''
    Lancichinetti-Fortunato-Radicchi Benchmark geneartor. Original from https://sites.google.com/site/andrealancichinetti/files  
    
    Parameter:
    ------------------
    To run the program type 
    ./benchmark [FLAG] [P]
    
    ----------------------
    
    To set the parameters, type:
    
    -N              [number of nodes]
    -k              [average degree]
    -maxk           [maximum degree]
    -mut            [mixing parameter for the topology]
    -muw            [mixing parameter for the weights]
    -beta           [exponent for the weight distribution]
    -t1             [minus exponent for the degree sequence]
    -t2             [minus exponent for the community size distribution]
    -minc           [minimum for the community sizes]
    -maxc           [maximum for the community sizes]
    -on             [number of overlapping nodes]
    -om             [number of memberships of the overlapping nodes]
    -C              [Average clustering coefficient]
    ----------------------
    
    It is also possible to set the parameters writing flags and relative numbers in a file. To specify the file, use the option:
    -f      [filename]
    You can set the parameters both writing some of them in the file, and using flags from the command line for others.
    
    -N, -k, -maxk, -muw have to be specified. For the others, the program can use default values:
    t1=2, t2=1, on=0, om=0, beta=1.5, mut=muw, minc and maxc will be chosen close to the degree sequence extremes.
    If you don't specify -C the rewiring process for raising the average clustering coefficient will not be performed
    If you set a parameter twice, the latter one will be taken.
    
    -------------------- Other options ---------------------------
    
    To have a random network use:
    -rand
    Using this option will set muw=0, mut=0, and minc=maxc=N, i.e. there will be one only community.
    Use option -sup (-inf) if you want to produce a benchmark whose distribution of the ratio of external degree/total degree is superiorly (inferiorly) bounded by the mixing parameter.
    
    -------------------- Examples ---------------------------
    
    Example1:
    ./benchmark -N 1000 -k 15 -maxk 50 -muw 0.1 -minc 20 -maxc 50
    Example2:
    ./benchmark -f flags.dat -t1 3
    
    -------------------- Other info ---------------------------
    
    Read file ReadMe.txt for more info.

      
    '''
    if not overide and local_exists(name):
        return load_local(name)
    else:
        params = locals()
        del params['overide']
        
        description = "LFR random graph"
        directed = False
        weighted = True
        params['directed'] = directed
        params['weighted'] = weighted
        params['name'] = 'LFR'
        gen = RandomGenerator(params=params)
        edges, gt = gen.generate(seed)
        from .dataset import Dataset    
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges, directed=directed, \
                       weighted=weighted, overide=overide, additional_meta={'genopts': params})


def generate_directed_weighted_random_graph_LFR(name, N, k=None, maxk=None, mut=None, muw=None, beta=None, t1=None, t2=None, \
                minc=None, maxc=None, on=None, om=None, C=None, seed=None, overide=False):
    '''
    Lancichinetti-Fortunato-Radicchi Benchmark geneartor. Original from https://sites.google.com/site/andrealancichinetti/files  
    
    Parameter:
    ----------------------
    
    To set the parameters, type:
    
    -N              [number of nodes]
    -k              [average in-degree]
    -maxk           [maximum in-degree]
    -mut            [mixing parameter for the topology]
    -muw            [mixing parameter for the weights]
    -beta           [exponent for the weight distribution]
    -t1             [minus exponent for the degree sequence]
    -t2             [minus exponent for the community size distribution]
    -minc           [minimum for the community sizes]
    -maxc           [maximum for the community sizes]
    -on             [number of overlapping nodes]
    -om             [number of memberships of the overlapping nodes]
    ----------------------
    
    It is also possible to set the parameters writing flags and relative numbers in a file. To specify the file, use the option:
    -f      [filename]
    You can set the parameters both writing some of them in the file, and using flags from the command line for others.
    
    -N, -k, -maxk, -muw have to be specified. For the others, the program can use default values:
    t1=2, t2=1, on=0, om=0, beta=1.5, mut=muw, minc and maxc will be chosen close to the degree sequence extremes.
    If you set a parameter twice, the latter one will be taken.
    
    -------------------- Other options ---------------------------
    
    To have a random network use:
    -rand
    Using this option will set muw=0, mut=0, and minc=maxc=N, i.e. there will be one only community.
    Use option -sup (-inf) if you want to produce a benchmark whose distribution of the ratio of external in-degree/total in-degree is superiorly (inferiorly) bounded by the mixing parameter.
    
    -------------------- Examples ---------------------------
    
    Example1:
    ./benchmark -N 1000 -k 15 -maxk 50 -muw 0.1 -minc 20 -maxc 50
    Example2:
    ./benchmark -f flags.dat -t1 3
    
    -------------------- Other info ---------------------------
    
    Read file ReadMe.txt for more info.

      
    '''
    if not overide and local_exists(name):
        return load_local(name)
    else:
        params = locals()
        del params['overide']
        
        description = "LFR random graph"
        directed = True
        weighted = True
        params['directed'] = directed
        params['weighted'] = weighted
        params['name'] = 'LFR'
        gen = RandomGenerator(params=params)
        edges, gt = gen.generate(seed)
        from .dataset import Dataset    
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges, directed=directed, weighted=weighted, overide=overide)


def generate_undirected_unweighted_hier_random_graph_LFR(name, N, k=None, maxk=None, mu1=None, mu2=None, t1=None, t2=None, minc=None, \
                maxc=None, on=None, om=None, minC=None, maxC=None, seed=None, overide=False):
    '''
    Lancichinetti-Fortunato-Radicchi Benchmark geneartor. Original from https://sites.google.com/site/andrealancichinetti/files  
    
    Parameter:
    ----------------------
    
    To set the parameters, type:
    
    -N              [number of nodes]
    -k              [average degree]
    -maxk           [maximum degree]
    -t1             [minus exponent for the degree sequence]
    -t2             [minus exponent for the community size distribution]
    -minc           [minimum for the micro community sizes]
    -maxc           [maximum for the micro community sizes]
    -on             [number of overlapping nodes]
    -om             [number of memberships of the overlapping nodes]
    -minC           [minimum for the macro community size]
    -maxC           [maximum for the macro community size]
    -mu1            [mixing parameter for the macro communities (see Readme file)]
    -mu2            [mixing parameter for the micro communities (see Readme file)]
    ----------------------
    
    It is also possible to set the parameters writing flags and relative numbers in a file. To specify the file, use the option:
    -f      [filename]
    
    -------------------- Examples ---------------------------
    
    Example2:
    ./hbenchmark -f flags.dat
    ./hbenchmark -N 10000 -k 20 -maxk 50 -mu2 0.3 -minc 20 -maxc 50 -minC 100 -maxC 1000 -mu1 0.1
    
    -------------------- Other info ---------------------------
    
    Read file ReadMe.txt for more info.

      
    '''
    if not overide and local_exists(name):
        return load_local(name)
    else:
        params = locals()
        del params['overide']
        
        description = "LFR random graph"
        directed = False
        weighted = False 
        params['directed'] = directed
        params['hier'] = True
        params['weighted'] = weighted
        params['name'] = 'LFR'
        gen = RandomGenerator(params=params)
        edges, gt = gen.generate(seed)
        from .dataset import Dataset    
        return Dataset(name, description=description, groundtruthObj=gt, edgesObj=edges, directed=directed, 
                       weighted=weighted, overide=overide, additional_meta={'genopts': params})
