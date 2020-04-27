'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
import sys
from gct.alg.powergraph_clustering import pg_label_propagation, GossipMap, RelaxMap

from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):

    def tearDown(self):
        pass

    def test_label_propagation(self):
        for data in  self.graphs: 
            alg = pg_label_propagation()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data,execution='sync',ncpus=4).get_result())
            print (clustering.load_result(data.name, alg.name))
 
    def test_GossipMap(self):
        for data in  self.graphs: 
            alg = GossipMap()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))
            
    def test_RelaxMap(self):
        for data in  self.graphs: 
            alg = RelaxMap()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))            


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
