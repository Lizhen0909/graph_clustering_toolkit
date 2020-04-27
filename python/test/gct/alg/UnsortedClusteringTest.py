'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
from gct.alg.unsorted_clustering import streamcom, Paris, \
    lso_cluster
import sys

from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):

    def tearDown(self):
        pass

    def testSteramcom(self):
        for data in  self.graphs: 
            alg = streamcom()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))

    def testPairs(self):
        for data in  self.graphs: 
            alg = Paris()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))
 
    def testLSOCluster(self):
        for data in  self.graphs: 
            alg = lso_cluster()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))
    
    def testLSOCluster_pmod(self):
        for data in  self.graphs: 
            alg = lso_cluster()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data, loss='pmod', pmod=3).get_result())
            print (clustering.load_result(data.name, alg.name))
            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
