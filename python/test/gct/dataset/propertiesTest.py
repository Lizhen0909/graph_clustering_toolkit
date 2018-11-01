'''
Created on Oct 26, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.dataset.properties import GraphProperties, GraphClustersProperties


class Test(unittest.TestCase):

    def setUp(self):
        self.graph_unweighted_undirect = random_dataset.generate_LFR("test_LFR_unw_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, a=0)
        assert not self.graph_unweighted_undirect.is_directed()
        assert not self.graph_unweighted_undirect.is_weighted()

    def tearDown(self):
        pass

    def testGraphProperties(self):
        p = GraphProperties(self.graph_unweighted_undirect)
        print ('num_edges', p.num_edges)
        print ('num_vectices', p.num_vectices)
        print ('density', p.density)
        print ('density1', p.density1)
        print ('weighted_degrees', p.weighted_degrees)
        print ('unweighted_degrees', p.unweighted_degrees)

    def testClustersProperties(self):
        g = self.graph_unweighted_undirect
        assert not g.is_weighted()
        p = GraphClustersProperties(g, g.get_ground_truth())
        print ('num_edges', p.num_edges)
        print ('num_vectices', p.num_vectices)
        print ('num_clusters', p.num_clusters)
        print ('cluser_sizes', p.cluser_sizes)
        print ('cluser_indexes', p.cluser_indexes)
        print ('cluser_edge_sizes', p.cluser_edge_sizes)
        print ('cluser_sum_intra_weights',p.cluser_sum_intra_weights)
        print ('unweighted_intra_cluster_densities', p.unweighted_intra_cluster_densities)
        print ('cluser_sum_weighted_degrees', p.cluser_sum_weighted_degrees)
        
        print ('intra_cluster_densities', p.intra_cluster_densities)
        print ('intra_cluster_density', p.intra_cluster_density)
        print ('inter_cluster_density', p.inter_cluster_density)
        print ('relative_cluser_densities', p.relative_cluser_densities)
        print ("modularity1", p.modularity1)
        print ("modularity2", p.modularity2)
        # print ("snap_modularities", p.snap_modularities)        
        # print ("snap_modularity", p.snap_modularity)
        
                                    
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
