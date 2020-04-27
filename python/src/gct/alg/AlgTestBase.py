'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset,dataset

class AlgTestBase(unittest.TestCase):

    def get_dataset(self, name, fun):
        if dataset.local_exists(name):
            return dataset.load_local(name)
        else:
            return fun(name)
        
    def setUp(self):
        overide=False
        def f(name):
            overide=False
            return random_dataset.generate_ovp_LFR(name, N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, a=0, overide=overide)

        name = "test_LFR_unw_und"                        
        self.graph_unweighted_undirect = self.get_dataset(name,f)
        assert not self.graph_unweighted_undirect.is_directed()
        assert not self.graph_unweighted_undirect.is_weighted()
        
        def f2(name):
            return random_dataset.generate_ovp_LFR("test_LFR_w_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True, a=0, overide=overide)

        name = "test_LFR_w_und"                        
        self.graph_weighted_undirect = self.get_dataset(name,f)
        assert not self.graph_weighted_undirect.is_directed()
        assert self.graph_weighted_undirect.is_weighted()

        name = "test_LFR_w_dir"
        if dataset.local_exists(name):
            self.graph_weighted_direct = dataset.load_local(name)
        else:        
            self.graph_weighted_direct = random_dataset.generate_ovp_LFR(name, N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True, a=1, overide=overide)
            assert  self.graph_weighted_direct.is_directed()
            assert self.graph_weighted_direct.is_weighted()
        
        name = "test_LFR_unw_dir"
        if dataset.local_exists(name):
            self.graph_unweighted_direct = dataset.load_local(name)
        else:
            self.graph_unweighted_direct = random_dataset.generate_ovp_LFR(name, N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=False, a=1, overide=overide)
            assert  self.graph_unweighted_direct.is_directed()
            assert not self.graph_unweighted_direct.is_weighted()
        
        self.graphs = [self.graph_unweighted_undirect, self.graph_weighted_undirect,
                       self.graph_weighted_direct, self.graph_unweighted_direct]
