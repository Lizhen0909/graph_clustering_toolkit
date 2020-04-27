'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
import sys
from gct.alg.sklearn_clustering import AffinityPropagation, SpectralClustering,\
    DBSCAN

from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):

    def tearDown(self):
        pass

    def testAffinityPropagation(self):
        for data in  self.graphs: 
            alg = AffinityPropagation()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))

    def testSpectralClustering(self):
        for data in  self.graphs: 
            alg = SpectralClustering()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))
            
    def testDBSCAN(self):
        for data in  self.graphs: 
            alg = DBSCAN()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))
            
            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
