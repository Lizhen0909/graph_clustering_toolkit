'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
from gct.alg.mcl_clustering import MCL

from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):


    def tearDown(self):
        pass

    def testMCL(self):
        alg = MCL()
        print ("testMCL")
        print (alg.run(self.graph_unweighted_undirect, I=2).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))
 

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
