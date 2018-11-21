'''
Created on Oct 26, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.metrics.graph_metrics import SNAPGraphMetrics
import snap


class Test(unittest.TestCase):

    def setUp(self):
        self.graph_unweighted_undirect = random_dataset.generate_ovp_LFR("test_LFR_unw_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, a=0)
        assert not self.graph_unweighted_undirect.is_directed()
        assert not self.graph_unweighted_undirect.is_weighted()

    def tearDown(self):
        pass

    def testSNAPGraphMetrics(self):
        p = SNAPGraphMetrics(self.graph_unweighted_undirect)
        print ('degree_histogram', p.degree_histogram)
        print ('degree_in_histogram', p.degree_in_histogram)
        print ('degree_out_histogram', p.degree_out_histogram)
        print ('node_degrees', p.node_degrees)
        print ('num_self_edges', p.num_self_edges)
        print ('scc_distribution', p.scc_distribution)
        print ('wcc_distribution', p.wcc_distribution)
        print ('edge_bridges', p.edge_bridges)
        print ('diameter', p.diameter())
        print ('effect_diameter', p.effect_diameter())
        print ('sample_shortest_path', p.sample_shortest_path())
        print ('sample_degree_centrality', p.sample_degree_centrality())
        btwn=p.sample_betweenness_centrality()  
        print ('sample_betweenness_centrality','#node btwn', len(btwn[0]), '#edge btwn', len(btwn[1]) )        
        print ('sample_closeness_centrality', p.sample_closeness_centrality())
        print ('sample_farness_centrality', p.sample_farness_centrality())        
        print ('page_rank_score', p.page_rank_score())
        print ('hubs_and_authorities_score', p.hubs_and_authorities_score())
        print ('sample_node_eccentricity', p.sample_node_eccentricity())
        print ('eigenvector_centrality', p.eigenvector_centrality())
        print ('average_clustering_coefficient', p.average_clustering_coefficient(False))        
        print ('distribution_clustering_coefficient', p.distribution_clustering_coefficient(False))
        print ('k_core', p.k_core(5))

                                            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
