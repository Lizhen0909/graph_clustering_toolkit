'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gcb.ds import random_dataset
from gcb.alg import clustering
from gcb.alg.OSLOM_clustering import Infomap, Infohiermap, lpm, louvain_method, \
    modopt, OSLOM, copra
import sys


class Test(unittest.TestCase):

    def setUp(self):
        self.graph_unweighted_undirect = random_dataset.generate_LFR("test_LFR_unw_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, a=0)
        assert not self.graph_unweighted_undirect.is_directed()
        assert not self.graph_unweighted_undirect.is_weighted()
        
        self.graph_weighted_undirect = random_dataset.generate_LFR("test_LFR_w_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True, a=0)
        assert not self.graph_weighted_undirect.is_directed()
        assert self.graph_weighted_undirect.is_weighted()
        
        self.graph_weighted_direct = random_dataset.generate_LFR("test_LFR_w_dir", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True, a=1)
        assert  self.graph_weighted_direct.is_directed()
        assert self.graph_weighted_direct.is_weighted()
        
        self.graph_unweighted_direct = random_dataset.generate_LFR("test_LFR_unw_dir", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=False, a=1)
        assert  self.graph_unweighted_direct.is_directed()
        assert not self.graph_unweighted_direct.is_weighted()
        
        self.graphs = [self.graph_unweighted_undirect, self.graph_weighted_undirect,
                       self.graph_weighted_direct, self.graph_unweighted_direct]

    def tearDown(self):
        pass
    
    def test_infomap(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = Infomap()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = Infomap()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = Infomap()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = Infomap()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))

    def test_Infohiermap(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = Infohiermap()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = Infohiermap()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = Infohiermap()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = Infohiermap()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))

    def test_lpm(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = lpm()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = lpm()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = lpm()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = lpm()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))

    def test_louvain_method(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = louvain_method()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = louvain_method()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = louvain_method()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = louvain_method()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))
        
    def test_copra(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = copra()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = copra()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = copra()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = copra()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))
        
    def test_modopt(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = modopt()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = modopt()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = modopt()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = modopt()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))

    def test_oslom(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = OSLOM()
        print (alg.run(self.graph_weighted_direct, fast=True).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_direct, fast=True).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_undirect, fast=True).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_weighted_undirect, fast=True).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))

    def test_oslom_with_infomap(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = OSLOM()
        print (alg.run(self.graph_weighted_direct, fast=True, infomap=True).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_direct, fast=True, infomap=True).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_undirect, fast=True, infomap=True).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_weighted_undirect, fast=True, infomap=True).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))
                
    def test_oslom_with_copra(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = OSLOM()
        print (alg.run(self.graph_weighted_direct, fast=True, copra=True).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_direct, fast=True, copra=True).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_undirect, fast=True, copra=True).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_weighted_undirect, fast=True, copra=True).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))

    def test_oslom_with_louvain(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = OSLOM()
        print (alg.run(self.graph_weighted_direct, fast=True, louvain=True).get_result())
        print (clustering.load_rusult(self.graph_weighted_direct.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_direct, fast=True, louvain=True).get_result())
        print (clustering.load_rusult(self.graph_unweighted_direct.name, alg.name)) 

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_undirect, fast=True, louvain=True).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_weighted_undirect, fast=True, louvain=True).get_result())
        print (clustering.load_rusult(self.graph_weighted_undirect.name, alg.name))

                        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
