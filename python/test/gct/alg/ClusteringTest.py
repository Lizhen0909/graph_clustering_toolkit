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


class Test(unittest.TestCase):

    def setUp(self):
        self.graph_unweighted_undirect = random_dataset.generate_ovp_LFR("test_LFR_unw_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, a=0)
        assert not self.graph_unweighted_undirect.is_directed()
        assert not self.graph_unweighted_undirect.is_weighted()
        
        self.graph_weighted_undirect = random_dataset.generate_ovp_LFR("test_LFR_w_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True, a=0)
        assert not self.graph_weighted_undirect.is_directed()
        assert self.graph_weighted_undirect.is_weighted()
        
        self.graph_weighted_direct = random_dataset.generate_ovp_LFR("test_LFR_w_dir", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True, a=1)
        assert  self.graph_weighted_direct.is_directed()
        assert self.graph_weighted_direct.is_weighted()
        
        self.graph_unweighted_direct = random_dataset.generate_ovp_LFR("test_LFR_unw_dir", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=False, a=1)
        assert  self.graph_unweighted_direct.is_directed()
        assert not self.graph_unweighted_direct.is_weighted()
        
        self.graphs = [self.graph_unweighted_undirect, self.graph_weighted_undirect,
                       self.graph_weighted_direct, self.graph_unweighted_direct]

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
