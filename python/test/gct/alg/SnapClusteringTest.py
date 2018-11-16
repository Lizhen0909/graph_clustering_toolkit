'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg.snap_clustering import Clauset_Newman_Moore, Girvan_Newman
from gct.alg import clustering
from gct.exception import UnsupportedException
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

    def testClauset_Newman_Moore(self):
        for data in  self.graphs: 
            alg = Clauset_Newman_Moore()
            print(sys._getframe().f_code.co_name, data.name)
            if data.is_directed():
                with self.assertRaises(UnsupportedException) as context:
                    print (alg.run(data).get_result())
            else:
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
 
    def testGirvan_Newman(self):
        for data in  self.graphs: 
            alg = Girvan_Newman()
            print(sys._getframe().f_code.co_name, data.name)
            if data.is_directed():
                with self.assertRaises(UnsupportedException) as context:
                    print (alg.run(data).get_result())
            else:
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
