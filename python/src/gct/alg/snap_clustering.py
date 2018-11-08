'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.dataset import convert
import snap    
from gct.alg.clustering import Clustering, save_result
from gct import utils

prefix='snap'

class Clauset_Newman_Moore(Clustering):
    '''
    A wrapper of *CommunityCNM* algorithm from SNAP 

    Arguments
    --------------------
    None 
    
    Reference
    ------------------------
    Clauset, Aaron, Mark EJ Newman, and Cristopher Moore. "Finding community structure in very large networks." Physical review E 70.6 (2004): 066111.
    '''   
    
    def __init__(self,name = "SNAP-Clauset_Newman_Moore"):
        
        super(Clauset_Newman_Moore, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"snap", "name": 'Clauset_Newman_Moore' }
    
    def run(self, data,seed =None):
        if False and (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        if seed is not None:self.logger.info("seed ignored")        
        UGraph = convert.to_snap(data)
        CmtyV = snap.TCnComV()
        timecost, modularity = utils.timeit(lambda: snap.CommunityCNM(UGraph, CmtyV))
        clusters = {}
        i = 0
        for Cmty in CmtyV:
            clusters[i] = []
            for NI in Cmty:
                clusters[i].append(NI)
            i += 1
                
        self.logger.info("Made %d clusters in %f seconds. modularity of the graph is %f" % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['modularity'] = modularity
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
    def get_result(self):
        if hasattr(self, 'result'):
            return self.result
        else:
            raise Exception("No result found. probably no run has been done")

    
class Girvan_Newman(Clustering):
    '''
    A wrapper of *CommunityGirvanNewman* algorithm from SNAP 

    Arguments
    --------------------
    None 
    
    Reference
    ------------------------
    Girvan, Michelle, and Mark EJ Newman. "Community structure in social and biological networks." Proceedings of the national academy of sciences 99.12 (2002): 7821-7826.
    '''   

    def __init__(self,name = "SNAP-Girvan_Newman"):
        
        super(Girvan_Newman, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"snap", "name": 'Girvan_Newman' }
    
    def run(self, data, seed=None):
        if False and (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        if seed is not None:self.logger.info("seed ignored")
        UGraph = convert.to_snap(data)
        CmtyV = snap.TCnComV()
        timecost, modularity = utils.timeit(lambda: snap.CommunityGirvanNewman(UGraph, CmtyV))
        clusters = {}
        i = 0
        for Cmty in CmtyV:
            clusters[i] = []
            for NI in Cmty:
                clusters[i].append(NI)
            i += 1

        self.logger.info("Made %d clusters in %f seconds. modularity of the graph is %f" % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['modularity'] = modularity
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
    def get_result(self):
        if hasattr(self, 'result'):
            return self.result
        else:
            raise Exception("No result found. probably no run has been done")

