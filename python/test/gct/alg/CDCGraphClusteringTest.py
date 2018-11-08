'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg import clustering
import sys
from gct.alg.cdc_clustering import CliquePercolation, Connected_Iterative_Scan,\
    EAGLE


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

    def test_CliquePercolation(self):
        for data in  self.graphs: 
            alg = CliquePercolation()
            print(sys._getframe().f_code.co_name)
            if data.is_directed():
                with self.assertRaises(Exception) as context:
                    print (alg.run(data, k=3).get_result())
            else:
                print (alg.run(data, k=3).get_result())
                print (clustering.load_result(data.name, alg.name))

    def test_Connected_Iterative_ScanPercolation(self):
        for data in  self.graphs: 
            alg = Connected_Iterative_Scan()
            print(sys._getframe().f_code.co_name)
            print (alg.run(data, l=0.).get_result())
            print (clustering.load_result(data.name, alg.name))
            
    def test_EAGLE(self):
        for data in  self.graphs: 
            alg = EAGLE()
            print(sys._getframe().f_code.co_name)
            print (alg.run(data, nThread=2).get_result())
            print (clustering.load_result(data.name, alg.name))            


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
