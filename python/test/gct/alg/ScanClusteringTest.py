'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
from gct.alg.scan_clustering import Scanpp, pScan, _AnyScan
import sys


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

    def testScanpp(self):
        for data in  self.graphs: 
            alg = Scanpp()
            print(sys._getframe().f_code.co_name)
            if data.is_weighted():
                with self.assertRaises(Exception) as context:
                    print (alg.run(data).get_result())
            else:
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
                        

    def testPScan(self):
        for data in  self.graphs: 
            alg = pScan()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(self.graph_unweighted_undirect, mu=3, epsilon=0.5, prog='pScan').get_result())
            print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

    def testPScan2(self):
        name=sys._getframe().f_code.co_name
        data = random_dataset.generate_undirected_unweighted_random_graph_LFR(name=name, \
                                       N=128, k=16, maxk=32, mu=0.2, minc=32)
        alg = pScan()
        print("Testing", name, data.name)
        print (alg.run(self.graph_unweighted_undirect, mu=3, epsilon=0.5, prog='pScan').get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))
        
    def testPPScan(self):
        alg = pScan()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect, mu=3, epsilon=0.5, prog='ppScan').get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))

    def testPPScanSSE(self):
        alg = pScan()
        print(sys._getframe().f_code.co_name) 
        print (alg.run(self.graph_unweighted_undirect, mu=3, epsilon=0.5, prog='ppScanSSE').get_result())
        print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))
        
    def testAnyScan(self):
        alg = _AnyScan()
        for i in range(1, 5):
            print(sys._getframe().f_code.co_name,i) 
            print (alg.run(self.graph_unweighted_undirect, algorithm=i, minpts=3, epsilon=0.5).get_result())
            print (clustering.load_result(self.graph_unweighted_undirect.name, alg.name))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
