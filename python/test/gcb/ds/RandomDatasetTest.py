'''
Created on Oct 23, 2018

@author: lizhen
'''
import unittest
from gcb.ds import random_dataset
from gcb import utils
import snap 


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

    def testRandomDataset7(self):
        ds = self.graph_unweighted_undirect
        utils.remove_if_file_exit(ds.file_snap)
        print (ds.to_snapformat())
        FIn = snap.TFIn(ds.file_snap)
        Graph = snap.TUNGraph.Load(FIn)

        ds = self.graph_unweighted_direct
        self.assertTrue(ds.is_directed())
        utils.remove_if_file_exit(ds.file_snap)
        print (ds.to_snapformat())
        FIn = snap.TFIn(ds.file_snap)
        Graph = snap.TNGraph.Load(FIn)
        
    def testRandomDataset6(self):
        ds = self.graph_unweighted_undirect
        utils.remove_if_file_exit(ds.file_anyscan)
        print (ds.to_anyscan())
            
    def testRandomDataset5(self):
        ds = self.graph_unweighted_direct
        print (ds.to_scanbin())
        
    def testRandomDataset4(self):
        ds = self.graph_weighted_direct
        print (ds.to_pajek())
        
    def testRandomDataset3(self):
        ds = self.graph_weighted_direct
        print (ds.to_edgelist())

        ds = self.graph_unweighted_undirect        
        print (ds.to_edgelist())  
        
    def testRandomDataset1(self):
        ds = random_dataset.generate_Erdos_Renyi("test1", 100, 1000, False)
        print (ds)
        ds.load()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoadSNAPDataset']
    unittest.main()
