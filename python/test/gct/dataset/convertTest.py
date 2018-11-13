'''
Created on Oct 26, 2018

@author: lizhen
'''
import unittest
import networkx as nx 
from gct.dataset import random_dataset, convert
from gct import utils, config
import igraph
import snap
import sys
import numpy as np 
from gct.dataset.dataset import load_local
import pandas as pd 


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

    def testAsMirror(self):
        name = sys._getframe().f_code.co_name 

        lst = [[1, 2], [2, 2], [2, 3], [2, 3], [3, 2]]
        d = convert.from_edgelist(name, lst, directed=False, overide=True)
        print (d.get_edges())
        self.assertTrue(not d.is_edge_mirrored)
        self.assertEqual(3, d.num_node)
        self.assertEqual(3, d.num_edge)
        edges = d.get_edges()
        assert edges['src'].dtype == np.int
        assert edges['dest'].dtype == np.int
        
        self.assertTrue(not load_local(name).is_edge_mirrored)
        
        newname = name + "_new"
        d = d.as_mirror_edges(newname=newname, overide=True)
        edges = d.get_edges()
        print (d.get_edges())
        self.assertTrue(d.is_edge_mirrored)        
        assert edges['src'].dtype == np.int
        assert edges['dest'].dtype == np.int
        self.assertEqual(3, d.num_node)
        self.assertEqual(5, d.num_edge)
        self.assertTrue(load_local(newname).is_edge_mirrored)

    def testAsUndirect(self):
        name = sys._getframe().f_code.co_name 

        lst = [[1, 2], [2, 2], [2, 3], [2, 3], [3, 2]]
        d = convert.from_edgelist(name, lst, directed=True)
        print (d.get_edges())
        self.assertEqual(3, d.num_node)
        self.assertEqual(4, d.num_edge)
        edges = d.get_edges()
        assert edges['src'].dtype == np.int
        assert edges['dest'].dtype == np.int
        
        d = d.as_undirected(newname=None)
        edges = d.get_edges()
        print (d.get_edges())
        assert edges['src'].dtype == np.int
        assert edges['dest'].dtype == np.int
        self.assertEqual(3, d.num_node)
        self.assertEqual(3, d.num_edge)
                
    def testFromEdgelist(self):
        name = "testFromEdgelist"
        
        lst = [[1, 2], [2, 2], [2, 3]]
        d = convert.from_edgelist(name, lst, overide=True)

        lst = [[1, 2, 0.4], [2, 2, 2], [2, 3, 12]]
        d = convert.from_edgelist(name, lst, overide=True)
        edges = d.get_edges()
        assert edges['src'].dtype == np.int
        assert edges['dest'].dtype == np.int
        assert edges['weight'].dtype == np.float32

    def testFromEdgelist_tuple(self):
        name = "testFromEdgelist_tuple"
        
        lst = [[1, 2], [2, 2], [2, 3]]
        lst = [tuple(u) for u in lst]
        d = convert.from_edgelist(name, lst, overide=True)

        lst = [[1, 2, 0.4], [2, 2, 2], [2, 3, 12]]
        lst = [tuple(u) for u in lst]
        d = convert.from_edgelist(name, lst, overide=True)
        edges = d.get_edges()
        assert edges['src'].dtype == np.int
        assert edges['dest'].dtype == np.int
        assert edges['weight'].dtype == np.float32

    def testFromEdgelist_ndarray(self):
        name = "testFromEdgelist_tuple"
        
        lst = np.array([[1, 2], [2, 2], [2, 3]])
        d = convert.from_edgelist(name, lst, overide=True)

        lst = np.array([[1, 2, 0.4], [2, 2, 2], [2, 3, 12]])
        d = convert.from_edgelist(name, lst, overide=True)
        edges = d.get_edges()
        assert edges['src'].dtype == np.int
        assert edges['dest'].dtype == np.int
        assert edges['weight'].dtype == np.float32        

    def testFromEdgelist_dataframe(self):
        name = "testFromEdgelist_dataframe"
        
        lst = pd.DataFrame([[1, 2], [2, 2], [2, 3]], columns=['src', 'dest'])
        d = convert.from_edgelist(name, lst, overide=True)

        lst = pd.DataFrame(np.array([[1, 2, 0.4], [2, 2, 2], [2, 3, 12]]), columns=['src', 'dest', 'weight'])
        d = convert.from_edgelist(name, lst, overide=True)
        edges = d.get_edges()
        assert edges['src'].dtype == np.int
        assert edges['dest'].dtype == np.int
        assert edges['weight'].dtype == np.float32  
                        
    def testToNextworkx(self):
        for data in self.graphs: 
            g = convert.to_networkx(data)

    def testFromNextworkx(self):
        name = "testFromNextworkx"

        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = nx.complete_graph(5)
        d = convert.from_networkx(name, G, weighted=False, overide=True)
        print (d) 

        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = nx.complete_graph(5).to_directed()
        d = convert.from_networkx(name, G, weighted=False, overide=True)
        print (d)
       
        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = nx.complete_graph(5) 
        G.add_weighted_edges_from((u, v, 1) for u, v in nx.complete_graph(5).edges())
        d = convert.from_networkx(name, G, weighted=True, overide=True)
        print (d)
                
        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = nx.complete_graph(5).to_directed()
        G.add_weighted_edges_from((u, v, 1) for u, v in nx.complete_graph(5).edges())
        d = convert.from_networkx(name, G, weighted=True, overide=True)
        print (d)

    def testToIGraph(self):
        for data in self.graphs:
            g = convert.to_igraph(data)
            print (data.is_weighted(), g.is_weighted(), data.is_directed(), g.is_directed())
            
    def testFromIGraph(self):
        name = "testFromIGraph"

        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = igraph.Graph.Full(5, directed=False)
        d = convert.from_igraph(name, G)
        print (d)

        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = igraph.Graph.Full(5, directed=True)
        d = convert.from_igraph(name, G)
        print (d)
        
        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = igraph.Graph.Full(5, directed=False)
        G.es['weight'] = [1] * G.ecount()
        d = convert.from_igraph(name, G)
        print (d) 

        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = igraph.Graph.Full(5, directed=True)
        G.es['weight'] = [1] * G.ecount()        
        d = convert.from_igraph(name, G)
        print (d) 

    def testToSnap(self):
        for data in self.graphs:
            if not data.is_weighted():
                g = convert.to_snap(data)
                print ("testToSnap", g, data)  

    def testFromSnap(self):
        name = "testFromSnap"

        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = snap.GenRndGnm(snap.PNGraph, 100, 1000) 
        d = convert.from_snap(name, G, overide=True)
        print ("testFromSnap", d)

        utils.remove_if_file_exit(config.get_data_file_path(name), is_dir=True)
        G = snap.GenRndGnm(snap.PUNGraph, 100, 1000) 
        d = convert.from_snap(name, G, overide=True)
        print ("testFromSnap", d) 

    def testToNetworkit(self):
        for data in self.graphs:
            g = convert.to_networkit(data)
            print ("testToNetworkit", g, data)  

                            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
