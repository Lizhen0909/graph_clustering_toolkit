'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
from gct.alg.cggc_clustering import CGGC
from gct.alg.OSLOM_clustering import OSLOM
from gct.dataset.dataset import load_local
from gct.alg.clustering import load_result
from gct.alg.cdc_clustering import ParCPM


from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):

    def tearDown(self):
        pass

    def testResult(self):
        data=self.graph_unweighted_undirect
        alg = CGGC()
        result = alg.run(data).get_result()
        print (result.runname)
        print (result.dataname)
        print (result.meta)
        print (result.params) 
        print (result.timecost)
        print (result.clustering())
        print (result.clustering(as_dataframe=True))
        
        result=load_result(data.name,result.runname)
        print (result.runname)
        print (result.dataname)
        print (result.meta)
        print (result.params) 
        print (result.timecost)
        print (result.clustering())
        print (result.clustering(as_dataframe=True))
        
    def testResult_multilevel(self):
        data=self.graph_unweighted_undirect
        alg = OSLOM()
        result = alg.run(data).get_result()
        print (result.runname)
        print (result.dataname)
        print (result.meta)
        print (result.params) 
        print (result.timecost)
        print (result.clustering())
        print (result.clustering(as_dataframe=True))
        
        result=load_result(data.name,result.runname)
        print (result.runname)
        print (result.dataname)
        print (result.meta)
        print (result.params) 
        print (result.timecost)
        print (result.clustering())
        print (result.clustering(as_dataframe=True))
        
    def testResult_multiclusters(self):
        data=self.graph_unweighted_undirect
        alg = ParCPM()
        result = alg.run(data).get_result()
        print (result.runname)
        print (result.dataname)
        print (result.meta)
        print (result.params) 
        print (result.timecost)
        print (result.clustering())
        print (result.clustering(as_dataframe=True))
        
        result=load_result(data.name,result.runname)
        print (result.runname)
        print (result.dataname)
        print (result.meta)
        print (result.params) 
        print (result.timecost)
        print (result.clustering())
        print (result.clustering(as_dataframe=True))
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
