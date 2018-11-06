'''
Created on Oct 23, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct import utils, config
import snap 


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
    
    def testRandomDataset8(self):
        ds = self.graph_unweighted_undirect
        utils.remove_if_file_exit(ds.file_hig)
        print (ds.to_higformat())
        
        ds = self.graph_weighted_undirect
        utils.remove_if_file_exit(ds.file_hig)
        print (ds.to_higformat())
                
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
        ds = random_dataset.generate_Erdos_Renyi("testRandomDataset1", 100, 1000, False)
        print (ds)

    def testRandomDataset0(self):
        ds = random_dataset.generate_ovp_LFR("testRandomDataset0", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, a=0, overide=True)
        print (ds)
        
    def testRandomDataseLFRUndirUnw(self):
        ds = random_dataset.generate_undirected_unweighted_random_graph_LFR('testRandomDataseLFRUndirUnw', N=128, k=16,
            maxk=16, mu=0.1, minc=32, overide=True)
        print (ds)        
        
    def testRandomDataseLFRUndirW(self):
        ds = random_dataset.generate_undirected_weighted_random_graph_LFR('testRandomDataseLFRUndirW', N=128, k=16,
            maxk=16, mut=0.1, muw=0.1, minc=32, overide=True)
        print (ds)        
    
    def testRandomDataseLFRDirUnw(self):
        ds = random_dataset.generate_directed_unweighted_random_graph_LFR('testRandomDataseLFRDirUnw', N=128, k=16,
            maxk=16, mu=0.1, minc=32, overide=True)
        print (ds)        
        
    def testRandomDataseLFRDirW(self):
        ds = random_dataset.generate_directed_weighted_random_graph_LFR('testRandomDataseLFRDirW', N=128, k=16,
            maxk=16, mut=0.1, muw=0.1, minc=32, overide=True)
        print (ds)         
         
    def testRandomDataseLFRHier(self):
        ds = random_dataset.generate_undirected_unweighted_hier_random_graph_LFR('testRandomDataseLFRHier', N=128, k=16,
            maxk=16, mu1=0.1, mu2=0.3, minc=32, minC=30, maxC=50, overide=True)
        print (ds)          

          
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoadSNAPDataset']
    unittest.main()
