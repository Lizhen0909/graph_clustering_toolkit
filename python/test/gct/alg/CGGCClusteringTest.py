'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
from gct.alg.cggc_clustering import CGGC


from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):


    def tearDown(self):
        pass

    def testCGGC(self):
        alg = CGGC()
        print ("testCGGC")
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))
 

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
