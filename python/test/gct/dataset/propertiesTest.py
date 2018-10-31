'''
Created on Oct 26, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.dataset.properties import GraphProperties, GraphClustersProperties


class Test(unittest.TestCase):

    def setUp(self):
        self.graph_unweighted_undirect = random_dataset.generate_LFR("test_LFR_unw_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1,a=0)
        assert not self.graph_unweighted_undirect.is_directed()
        assert not self.graph_unweighted_undirect.is_weighted()
        

    def tearDown(self):
        pass

    def testGraphProperties(self):
        p = GraphProperties(self.graph_unweighted_undirect)
        print (p.num_edges)
        print (p.num_vectices)
        print (p.density)
        print (p.density1)
        print (p.degrees)

    def testClustersProperties(self):
        g=self.graph_unweighted_undirect
        p = GraphClustersProperties(g,g.get_ground_truth())
        print (p.num_edges)
        print (p.num_vectices)
        print (p.num_clusters)
        print (p.cluser_sizes)
        print (p.cluser_indexes)
        print (p.cluser_edge_sizes)
        print (p.intra_cluster_densities)
        print (p.intra_cluster_density)
        print (p.inter_cluster_density)
        
                                    
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
