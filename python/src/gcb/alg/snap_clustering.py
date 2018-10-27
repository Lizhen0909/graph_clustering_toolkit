'''
Created on Oct 27, 2018

@author: lizhen
'''
from gcb.ds import convert
import snap    
from gcb.alg.clustering import Clustering, save_result


class Clauset_Newman_Moore(Clustering):

    def __init__(self):
        name = "SNAP-Clauset_Newman_Moore"
        super(Clauset_Newman_Moore, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"snap", "name": 'Clauset_Newman_Moore' }
    
    def run(self, data):
        if (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        UGraph = convert.to_snap(data)
        CmtyV = snap.TCnComV()
        modularity = snap.CommunityCNM(UGraph, CmtyV)
        clusters = {}
        i = 0
        for Cmty in CmtyV:
            clusters[i] = []
            for NI in Cmty:
                clusters[i].append(NI)
            i += 1
                
        print "Made %d clusters. modularity of the graph is %f" % (len(clusters), modularity)
        
        result = {}
        result['algname'] = self.name
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

    def __init__(self):
        name = "SNAP-Girvan_Newman"
        super(Girvan_Newman, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"snap", "name": 'Girvan_Newman' }
    
    def run(self, data):
#         if (data.is_directed() or data.is_weighted()):
#             raise Exception("only undirected and unweighted graph is supported")
        UGraph = convert.to_snap(data)
        CmtyV = snap.TCnComV()
        modularity = snap.CommunityGirvanNewman(UGraph, CmtyV)
        clusters = {}
        i = 0
        for Cmty in CmtyV:
            clusters[i] = []
            for NI in Cmty:
                clusters[i].append(NI)
            i += 1
                
        print "Made %d clusters. modularity of the graph is %f" % (len(clusters), modularity)
        
        result = {}
        result['algname'] = self.name
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
    

