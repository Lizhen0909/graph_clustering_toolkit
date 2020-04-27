'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
import sys
from gct.alg.networkit_clustering import LPDegreeOrdered, CutClustering, PLP,\
    PLM
    
from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):


    def tearDown(self):
        pass

    def testLPDegreeOrdered(self):
        for data in  self.graphs: 
            alg = LPDegreeOrdered()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))
 
    def testCutClustering(self):
        for data in  self.graphs: 
            alg = CutClustering()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data,alpha=0.15).get_result())
            print (clustering.load_result(data.name, alg.name))

    def testPLP(self):
        for data in  self.graphs: 
            alg = PLP()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))


    def testPLM(self):
        for data in  self.graphs: 
            alg = PLM()
            print(sys._getframe().f_code.co_name) 
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
