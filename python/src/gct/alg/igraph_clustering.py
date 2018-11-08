'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.dataset import convert
import igraph    
from gct.alg.clustering import Clustering, save_result
from gct import utils

prefix='igraph'

class community_fastgreedy(Clustering):
    '''
    A wrapper of *community_fastgreedy* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    A Clauset, MEJ Newman and C Moore: Finding community structure in very large networks. Phys Rev E 70, 066111 (2004).
    '''
    def __init__(self,name = "igraph-community_fastgreedy"):
        super(community_fastgreedy, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_fastgreedy' }
    
    def run(self, data,seed=None):
        if False and (data.is_directed())  :
            raise Exception("only undirected is supported")
        if seed is not None:self.logger.info("seed ignored")
        g = convert.to_igraph(data)
        timecost, ret = utils.timeit(lambda: g.community_fastgreedy(weights='weight' if data.is_weighted() else None))
        vc = ret.as_clustering()
        clusters = {}
        for i, a in enumerate(vc):
            clusters[i] = a
            
        modularity = vc.modularity
        self.logger.info("Made %d clusters in %f seconds. modularity=%f " % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['modularity'] = modularity        
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 

 
class community_infomap(Clustering):
    '''
    A wrapper of *community_infomap* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    M. Rosvall and C. T. Bergstrom: Maps of information flow reveal community structure in complex networks, PNAS 105, 1118 (2008). http://dx.doi.org/10.1073/pnas.0706851105, http://arxiv.org/abs/0707.0609.
    M. Rosvall, D. Axelsson, and C. T. Bergstrom: The map equation, Eur. Phys. J. Special Topics 178, 13 (2009). http://dx.doi.org/10.1140/epjst/e2010-01179-1, http://arxiv.org/abs/0906.1405.
    '''
    def __init__(self,name = "igraph-community_infomap"):
        super(community_infomap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_infomap' }
    
    def run(self, data, seed=None):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
        if seed is not None:self.logger.info("seed ignored")        
        g = convert.to_igraph(data)
        timecost, ret = utils.timeit(lambda: g.community_infomap(edge_weights='weight' if data.is_weighted() else None))
        vc = ret
        clusters = {}
        for i, a in enumerate(vc):
            clusters[i] = a
            
        modularity = vc.modularity
        self.logger.info("Made %d clusters in %f seconds. modularity=%f " % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['modularity'] = modularity        
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
    
class community_leading_eigenvector(Clustering):
    '''
    A wrapper of *community_leading_eigenvector* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    MEJ Newman: Finding community structure in networks using the eigenvectors of matrices, arXiv:physics/0605087
    '''

    def __init__(self,name = "igraph-community_leading_eigenvector"):
        super(community_leading_eigenvector, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_leading_eigenvector' }
    
    def run(self, data,seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        if seed is not None:self.logger.info("seed ignored")        
        g = convert.to_igraph(data)
        timecost, ret = utils.timeit(lambda: g.community_leading_eigenvector(weights='weight' if data.is_weighted() else None))
        vc = ret
        clusters = {}
        for i, a in enumerate(vc):
            clusters[i] = a
            
        modularity = vc.modularity
        self.logger.info("Made %d clusters in %f seconds. modularity=%f " % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['modularity'] = modularity        
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self     
 

class community_label_propagation(Clustering):
    '''
    A wrapper of *community_label_propagation* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    Raghavan, U.N. and Albert, R. and Kumara, S. Near linear time algorithm to detect community structures in large-scale networks. Phys Rev E 76:036106, 2007. http://arxiv.org/abs/0709.2938.
    '''

    def __init__(self,name = "igraph-community_label_propagation"):
        super(community_label_propagation, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_label_propagation' }
    
    def run(self, data, seed=None):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
        if seed is not None:self.logger.info("seed ignored")
        g = convert.to_igraph(data)
        timecost, ret = utils.timeit(lambda: g.community_label_propagation(weights='weight' if data.is_weighted() else None))
        vc = ret
        clusters = {}
        for i, a in enumerate(vc):
            clusters[i] = a
            
        modularity = -1 if vc.modularity is None  else vc.modularity 
        self.logger.info("Made %d clusters in %f seconds. modularity=%f " % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['modularity'] = modularity        
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self     

    
class community_multilevel(Clustering):
    '''
    A wrapper of *community_multilevel* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    VD Blondel, J-L Guillaume, R Lambiotte and E Lefebvre: Fast unfolding of community hierarchies in large networks, J Stat Mech P10008 (2008), http://arxiv.org/abs/0803.0476
    '''
    def __init__(self,name = "igraph-community_multilevel"):
        super(community_multilevel, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_multilevel' }
    
    def run(self, data, seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        if seed is not None:self.logger.info("seed ignored")
        g = convert.to_igraph(data)
        timecost, ret = utils.timeit(lambda: g.community_multilevel(weights='weight' if data.is_weighted() else None))
        vc = ret
        clusters = {}
        for i, a in enumerate(vc):
            clusters[i] = a
            
        modularity = -1 if vc.modularity is None  else vc.modularity 
        self.logger.info("Made %d clusters in %f seconds. modularity=%f " % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['modularity'] = modularity        
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self     
    
 
class community_optimal_modularity(Clustering):
    '''
    A wrapper of *community_optimal_modularity* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    TBD
    '''
    def __init__(self,name = "igraph-community_optimal_modularity"):
        
        super(community_optimal_modularity, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_optimal_modularity' }
    
    def run(self, data, seed=None):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
        if seed is not None:self.logger.info("seed ignored")
        g = convert.to_igraph(data)
        timecost, ret = utils.timeit(lambda: g.community_optimal_modularity(weights='weight' if data.is_weighted() else None))
        vc = ret
        clusters = {}
        for i, a in enumerate(vc):
            clusters[i] = a
            
        modularity = -1 if vc.modularity is None  else vc.modularity 
        self.logger.info("Made %d clusters in %f seconds. modularity=%f " % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['modularity'] = modularity        
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self  

    
class community_edge_betweenness(Clustering):
    '''
    A wrapper of *community_edge_betweenness* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
     M Girvan and MEJ Newman: Community structure in social and biological networks, Proc. Nat. Acad. Sci. USA 99, 7821-7826 (2002)
    '''
    def __init__(self,name = "igraph-community_edge_betweenness"):
        
        super(community_edge_betweenness, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_edge_betweenness' }
    
    def run(self, data, seed=None):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
        if seed is not None:self.logger.info("seed ignored")
        g = convert.to_igraph(data)
        timecost, ret = utils.timeit(lambda: g.community_edge_betweenness(weights='weight' if data.is_weighted() else None))
        vc = ret.as_clustering()
        clusters = {}
        for i, a in enumerate(vc):
            clusters[i] = a
            
        modularity = -1 if vc.modularity is None  else vc.modularity 
        self.logger.info("Made %d clusters in %f seconds. modularity=%f " % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['modularity'] = modularity        
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
class community_spinglass(Clustering):
    '''
    A wrapper of *community_spinglass* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    Reichardt J and Bornholdt S: Statistical mechanics of community detection. Phys Rev E 74:016110 (2006). http://arxiv.org/abs/cond-mat/0603718.
    Traag VA and Bruggeman J: Community detection in networks with positive and negative links. Phys Rev E 80:036115 (2009). http://arxiv.org/abs/0811.2329.
    '''
    def __init__(self,name = "igraph-community_spinglass"):
        super(community_spinglass, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_spinglass' }
    
    def run(self, data,seed=None):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
        if seed is not None:self.logger.info("seed ignored")
        g = convert.to_igraph(data)
        timecost, ret = utils.timeit(lambda: g.community_spinglass(weights='weight' if data.is_weighted() else None))
        vc = ret 
        clusters = {}
        for i, a in enumerate(vc):
            clusters[i] = a
            
        modularity = -1 if vc.modularity is None  else vc.modularity 
        self.logger.info("Made %d clusters in %f seconds. modularity=%f " % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['modularity'] = modularity        
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self      

class community_walktrap(Clustering):
    '''
    A wrapper of *community_walktrap* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    Pascal Pons, Matthieu Latapy: Computing communities in large networks using random walks, http://arxiv.org/abs/physics/0512106
    '''

    def __init__(self,name = "igraph-community_walktrap"):
        super(community_walktrap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_walktrap' }
    
    def run(self, data, seed=None):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
        if seed is not None:self.logger.info("seed ignored")
        g = convert.to_igraph(data)
        timecost, ret = utils.timeit(lambda: g.community_walktrap(weights='weight' if data.is_weighted() else None))
        vc = ret.as_clustering()
        clusters = {}
        for i, a in enumerate(vc):
            clusters[i] = a
            
        modularity = -1 if vc.modularity is None  else vc.modularity 
        self.logger.info("Made %d clusters in %f seconds. modularity=%f " % (len(clusters), timecost, modularity))
        
        result = {}
        result['timecost'] = timecost
        result['modularity'] = modularity        
        result['runname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self   
        
    
