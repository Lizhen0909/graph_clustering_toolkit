'''
Created on Oct 26, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset, convert
from gct.metrics.metrics import GraphMetrics, GraphClusterMetrics, \
    ClusterComparator
import numpy as np 
from gct.alg.OSLOM_clustering import Infomap, OSLOM
from gct.alg import clustering
from gct.alg.cggc_clustering import CGGC


class Test(unittest.TestCase):

    def setUp(self):
        self.graph_unweighted_undirect = random_dataset.generate_LFR("test_LFR_unw_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, a=0)
        assert not self.graph_unweighted_undirect.is_directed()
        assert not self.graph_unweighted_undirect.is_weighted()

    def tearDown(self):
        pass

    def testGraphMetrics(self):
        p = GraphMetrics(self.graph_unweighted_undirect)
        print ('num_edges', p.num_edges)
        print ('num_vectices', p.num_vectices)
        print ('density', p.density)
        print ('density1', p.density1)
        print ('weighted_degrees', p.weighted_degrees)
        print ('unweighted_degrees', p.unweighted_degrees)

    def testClustersProperties(self):
        g = self.graph_unweighted_undirect
        assert not g.is_weighted()
        p = GraphClusterMetrics(g, list(g.get_ground_truth().values())[0])
        self.assertEqual(p.num_edges * 2, p.sum_weight)
        self.assertEqual(np.sum(list(p.cluster_out_sum_weights.values())) + np.sum(list(p.cluster_sum_intra_weights.values())), p.sum_weight)
        print ('num_edges', p.num_edges)
        print ('num_vectices', p.num_vectices)
        print ('num_clusters', p.num_clusters)
        print ('cluster_sizes', p.cluster_sizes)
        print ('cluster_indexes', p.cluster_indexes)
        print ('cluster_edge_sizes', p.cluster_edge_sizes)
        print ('cluster_sum_intra_weights', p.cluster_sum_intra_weights)
        print ('unweighted_intra_cluster_densities', p.unweighted_intra_cluster_densities)
        print ('cluster_sum_weighted_degrees', p.cluster_sum_weighted_degrees)
        
        print ('intra_cluster_densities', p.intra_cluster_densities)
        print ('intra_cluster_density', p.intra_cluster_density)
        print ('inter_cluster_density', p.inter_cluster_density)
        print ('relative_cluster_densities', p.relative_cluster_densities)
        print ("modularity2", p.modularity2)
        print ("cluster_expansions", p.cluster_expansions)
        print ("cluster_cut_ratios", p.cluster_cut_ratios)
        
        print ("conductance", p.conductance)  
        print ("normalized_cut", p.normalized_cut)
              
        print ("cluster_max_out_degree_fraction", p.cluster_max_out_degree_fraction)
        print ("cluster_avg_out_degree_fraction", p.cluster_avg_out_degree_fraction)
        print ("cluster_flake_out_degree_fraction", p.cluster_flake_out_degree_fraction)
        print ("separability", p.separability)
        
        print ("cluster_clustering_coefficient", p.cluster_clustering_coefficient)
        print ("cluster_local_clustering_coefficient", p.cluster_local_clustering_coefficient) 
        
        print ("AAA", convert.to_igraph(self.graph_unweighted_undirect).transitivity_local_undirected())       
        print ("AAA", convert.to_igraph(self.graph_unweighted_undirect).transitivity_undirected())       

    def testClusterComparator(self):
        g = self.graph_unweighted_undirect

        def make_cluter_if_not_exists():
            alg = CGGC()
            if not clustering.has_result(g.name, alg.name):
                alg.run(g).get_result()
            return clustering.load_result(g.name, alg.name)

        assert not g.is_weighted()
        gt = list(g.get_ground_truth().values())[0]
        cluster = make_cluter_if_not_exists()
        
        p = ClusterComparator(gt, cluster)
        print ('sklean_nmi', p.sklean_nmi)
        print ('sklean_ami', p.sklean_ami)
        print ('sklean_ars', p.sklean_ars)
        print ('sklean_completeness', p.sklean_completeness)        
        print ('GenConvNMI', p.GenConvNMI(sync=True, membership=1))
        print ('OvpNMI', p.OvpNMI(sync=True, allnmi=True, omega=True))
        print ('xmeasure_nmi', p.xmeasure_nmi(sync=True, all=False))
        print ('xmeasure_nmi_all', p.xmeasure_nmi(sync=True, all=True))
        print ('xmeasure_f1_omega', p.xmeasure(sync=True, f1="p", omega=True ))
        print ('xmeasure_f1', p.xmeasure(sync=True, f1="p"))
        print ('xmeasure_omega', p.xmeasure(sync=True, omega=True, extended=True))
        
        
    def testClusterComparator2(self):
        g = self.graph_unweighted_undirect

        def make_cluter_if_not_exists():
            alg = OSLOM()
            if not clustering.has_result(g.name, alg.name):
                alg.run(g).get_result()
            return clustering.load_result(g.name, alg.name)

        assert not g.is_weighted()
        gt = list(g.get_ground_truth().values())[0]
        cluster = make_cluter_if_not_exists()
        
        p = ClusterComparator(gt, cluster)
        print ('sklean_nmi', p.sklean_nmi)
        print ('sklean_ami', p.sklean_ami)
        print ('sklean_ars', p.sklean_ars)
        print ('sklean_completeness', p.sklean_completeness)        
        print ('GenConvNMI', p.GenConvNMI(sync=True))
        print ('xmeasure_nmi', p.xmeasure_nmi(sync=True, all=False))
        print ('xmeasure_nmi_all', p.xmeasure_nmi(sync=True, all=True))
        print ('xmeasure_f1_omega', p.xmeasure(sync=True, f1="p", omega=True ))
        print ('xmeasure_f1', p.xmeasure(sync=True, f1="p"))
        print ('xmeasure_omega', p.xmeasure(sync=True, omega=True, extended=True))

                                            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
