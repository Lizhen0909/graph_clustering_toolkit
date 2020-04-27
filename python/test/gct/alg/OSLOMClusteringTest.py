'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
from gct.alg.OSLOM_clustering import Infomap, Infohiermap, lpm, louvain_method, \
    modopt, OSLOM, copra
import sys

from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):


    def tearDown(self):
        pass
    
    def test_infomap(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = Infomap()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = Infomap()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = Infomap()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = Infomap()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))

    def test_Infohiermap(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = Infohiermap()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = Infohiermap()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = Infohiermap()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = Infohiermap()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))

    def test_lpm(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = lpm()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = lpm()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = lpm()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = lpm()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))

    def test_louvain_method(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = louvain_method()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = louvain_method()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = louvain_method()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = louvain_method()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))
        
    def test_copra(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = copra()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = copra()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = copra()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = copra()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))
        
    def test_modopt(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = modopt()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = modopt()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = modopt()
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = modopt()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))

    def test_oslom(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = OSLOM()
        print (alg.run(self.graph_weighted_direct, fast=True).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_direct, fast=True).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_undirect, fast=True).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_weighted_undirect, fast=True).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))

    def test_oslom_with_infomap(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = OSLOM()
        print (alg.run(self.graph_weighted_direct, fast=True, infomap=True).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_direct, fast=True, infomap=True).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_undirect, fast=True, infomap=True).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_weighted_undirect, fast=True, infomap=True).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))
                
    def test_oslom_with_copra(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = OSLOM()
        print (alg.run(self.graph_weighted_direct, fast=True, copra=True).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_direct, fast=True, copra=True).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_undirect, fast=True, copra=True).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_weighted_undirect, fast=True, copra=True).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))

    def test_oslom_with_louvain(self):  
        print(sys._getframe().f_code.co_name) 
        
        alg = OSLOM()
        print (alg.run(self.graph_weighted_direct, fast=True, louvain=True).get_result())
        print (clustering.load_result(self.graph_weighted_direct.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_direct, fast=True, louvain=True).get_result())
        print (clustering.load_result(self.graph_unweighted_direct.name, alg.name)) 

        alg = OSLOM()
        print (alg.run(self.graph_unweighted_undirect, fast=True, louvain=True).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

        alg = OSLOM()
        print (alg.run(self.graph_weighted_undirect, fast=True, louvain=True).get_result())
        print (clustering.load_result(self.graph_weighted_undirect.name, alg.name))

                        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
