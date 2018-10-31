'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
from gct.alg.igraph_clustering import community_fastgreedy, community_infomap, \
    community_leading_eigenvector, community_label_propagation, \
    community_multilevel, community_optimal_modularity, \
    community_edge_betweenness, community_spinglass, community_walktrap
import sys


class Test(unittest.TestCase):

    def setUp(self):
        self.graph_unweighted_undirect = random_dataset.generate_LFR("test_LFR_unw_und_small", N=16, k=4, maxk=8, muw=0.1, minc=4, beta=1, a=0)
        assert not self.graph_unweighted_undirect.is_directed()
        assert not self.graph_unweighted_undirect.is_weighted()
        
        self.graph_weighted_undirect = random_dataset.generate_LFR("test_LFR_w_und_small", N=16, k=4, maxk=8, muw=0.1, minc=4, beta=1, weighted=True, a=0)
        assert not self.graph_weighted_undirect.is_directed()
        assert self.graph_weighted_undirect.is_weighted()
        
        self.graph_weighted_direct = random_dataset.generate_LFR("test_LFR_w_dir_small", N=16, k=4, maxk=8, muw=0.1, minc=4, beta=1, weighted=True, a=1)
        assert  self.graph_weighted_direct.is_directed()
        assert self.graph_weighted_direct.is_weighted()
        
        self.graph_unweighted_direct = random_dataset.generate_LFR("test_LFR_unw_dir_small", N=16, k=4, maxk=8, muw=0.1, minc=4, beta=1, weighted=False, a=1)
        assert  self.graph_unweighted_direct.is_directed()
        assert not self.graph_unweighted_direct.is_weighted()
        
        self.graphs = [self.graph_unweighted_undirect, self.graph_weighted_undirect,
                       self.graph_weighted_direct, self.graph_unweighted_direct]

    def tearDown(self):
        pass

    def testCommunity_fastgreedy(self):
        alg = community_fastgreedy()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_fastgreedy()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

    def testCommunity_infomap(self):
        alg = community_infomap()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_infomap()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_infomap()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

    def test_community_label_propagation(self):
        alg = community_label_propagation()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_label_propagation()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_label_propagation()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = community_label_propagation()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
    def test_community_multilevel(self):
        alg = community_multilevel()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_multilevel()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
    def testCommunity_leading_eigenvector(self): 
        alg = community_leading_eigenvector()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_leading_eigenvector()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
 
    def test_community_optimal_modularity(self):  
        alg = community_optimal_modularity()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_optimal_modularity()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_optimal_modularity()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = community_optimal_modularity()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))        

    def test_community_edge_betweenness(self):  
        alg = community_edge_betweenness()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_edge_betweenness()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_edge_betweenness()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = community_edge_betweenness()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name)) 

    def test_community_spinglass(self):  
        alg = community_spinglass()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_spinglass()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_spinglass()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = community_spinglass()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name)) 
        
    def test_community_walktrap(self):  
        alg = community_walktrap()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_walktrap()
        print (alg.run(self.graph_weighted_undirect).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))
        
        alg = community_walktrap()
        print (alg.run(self.graph_weighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name))

        alg = community_walktrap()
        print (alg.run(self.graph_unweighted_direct).get_result())
        print (clustering.load_rusult(self.graph_unweighted_undirect.name, alg.name)) 

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
