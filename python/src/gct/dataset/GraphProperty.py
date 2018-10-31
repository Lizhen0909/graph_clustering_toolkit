'''
Created on Oct 31, 2018

@author:  Lizhen Shi
'''

import numpy as np  
class GraphProperties(object):

    def __init__(self, data):
        self.data = data 

    def set_if_not_exists(self, name, fun):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            print ("call fun for "+name)
            value = fun()
            setattr(self, name, value)
            return value 
        
    @property    
    def directed(self):
        return self.data.directed
    
    @property
    def edges(self):
        return self.set_if_not_exists("_edges", lambda: self.data.get_edges())
    
    @property
    def weighted(self):
        return self.data.weighted    
    
    @property 
    def num_edges(self):
        return self.edges.shape[0]
    
    @property 
    def num_vectices(self):
        return self.set_if_not_exists("_num_vetices", lambda: len(set(np.unique(self.edges[['src', 'dest']].values))))

    @property
    def density1(self):
        m,n =self.num_edges,self.num_vectices
        assert n>1
        return float(m)/n
        
    @property
    def density(self):
        m,n =self.num_edges,self.num_vectices
        assert n>1
        return float(m)*2/n/(n-1)
    
    
    
    
