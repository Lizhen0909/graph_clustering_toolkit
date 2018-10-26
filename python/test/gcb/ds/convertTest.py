'''
Created on Oct 26, 2018

@author: lizhen
'''
import unittest
import networkx as nx 
from gcb.ds import random_dataset, convert
from gcb import utils, config


class Test(unittest.TestCase):

    def setUp(self):
        self.graph_unweighted_undirect = ds = random_dataset.generate_LFR("test_LFR_unw_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1)
        self.graph_weighted_undirect = random_dataset.generate_LFR("test_LFR_w_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True)
        self.graph_weighted_direct = random_dataset.generate_LFR("test_LFR_w_dir", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True, a=1)
        self.graph_unweighted_direct = random_dataset.generate_LFR("test_LFR_unw_dir", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=False, a=1)
        self.graphs = [self.graph_unweighted_undirect, self.graph_weighted_undirect,
                       self.graph_weighted_direct, self.graph_unweighted_direct]

    def tearDown(self):
        pass

    def testToNextworkx(self):
        for data in self.graphs: 
            g = convert.to_networkx(data)

    def testFromNextworkx(self):
        name = "test"

        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = nx.complete_graph(5)
        d = convert.from_networkx(name, G, weighted=False)
        d.load()
        print d 

        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = nx.complete_graph(5).to_directed()
        d = convert.from_networkx(name, G, weighted=False)
        d.load()
        print d
        
        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = nx.complete_graph(5).to_directed()
        G.add_weighted_edges_from((u, v, 1) for u, v in nx.complete_graph(5).edges())
        d = convert.from_networkx(name, G, weighted=True)
        d.load()
        print d 
            

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
