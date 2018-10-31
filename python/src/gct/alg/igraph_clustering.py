'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.dataset import convert
import igraph    
from gct.alg.clustering import Clustering, save_result
from gct import utils


class community_fastgreedy(Clustering):

    def __init__(self):
        name = "igraph-community_fastgreedy"
        super(community_fastgreedy, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_fastgreedy' }
    
    def run(self, data):
        if (data.is_directed())  :
            raise Exception("only undirected is supported")
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
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 

 
class community_infomap(Clustering):

    def __init__(self):
        name = "igraph-community_infomap"
        super(community_infomap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_infomap' }
    
    def run(self, data):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
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
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
    
class community_leading_eigenvector(Clustering):

    def __init__(self):
        name = "igraph-community_leading_eigenvector"
        super(community_leading_eigenvector, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_leading_eigenvector' }
    
    def run(self, data):
        if (data.is_directed()):
            raise Exception("only undirected is supported")
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
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self     
 

class community_label_propagation(Clustering):

    def __init__(self):
        name = "igraph-community_label_propagation"
        super(community_label_propagation, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_label_propagation' }
    
    def run(self, data):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
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
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self     

    
class community_multilevel(Clustering):

    def __init__(self):
        name = "igraph-community_multilevel"
        super(community_multilevel, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_multilevel' }
    
    def run(self, data):
        if (data.is_directed()):
            raise Exception("only undirected is supported")
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
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self     
    
 
class community_optimal_modularity(Clustering):

    def __init__(self):
        name = "igraph-community_optimal_modularity"
        super(community_optimal_modularity, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_optimal_modularity' }
    
    def run(self, data):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
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
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self  

    
class community_edge_betweenness(Clustering):

    def __init__(self):
        name = "igraph-community_edge_betweenness"
        super(community_edge_betweenness, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_edge_betweenness' }
    
    def run(self, data):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
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
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
class community_spinglass(Clustering):

    def __init__(self):
        name = "igraph-community_spinglass"
        super(community_spinglass, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_spinglass' }
    
    def run(self, data):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
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
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self      

class community_walktrap(Clustering):

    def __init__(self):
        name = "igraph-community_walktrap"
        super(community_walktrap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"igraph", "name": 'community_walktrap' }
    
    def run(self, data):
        if (data.is_directed()) and False:
            raise Exception("only undirected is supported")
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
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self   
        
    
