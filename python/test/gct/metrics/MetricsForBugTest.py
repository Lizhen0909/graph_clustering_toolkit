'''

@author: Bo Chen
'''
import unittest
from gct.metrics.metrics import GraphMetrics, GraphClusterMetrics, \
    ClusterComparator
import numpy as np 
from gct.alg import clustering
from gct.dataset import dataset
import json
import gct


def calc_clu_metrics(data, clu):
    o = GraphClusterMetrics(data, clu)
    l = ['num_clusters', 'intra_cluster_density', 'inter_cluster_density', 'modularity', 'conductance',
        'normalized_cut', 'cluster_max_out_degree_fraction', 'cluster_avg_out_degree_fraction',
        'cluster_flake_out_degree_fraction', 'separability', 'cluster_clustering_coefficient'
        ]

    def f(o, u):
        try:
            return getattr(o, u)
        except:
            raise
            return np.nan

    d = {u:f(o, u) for u in l}
    ret = {}
    for k, v in d.items():
        if isinstance(v, dict):
            ret[k] = np.nanmean(list(v.values()))
        else:
            ret[k] = v
    return ret

def calc_clu_gt_attrib(gt,clu):
    compa = ClusterComparator(gt, clu)
    o = ClusterComparator(gt,clu)
    l = ['sklean_nmi', 'sklean_ami', 'sklean_ars','sklean_completeness' 
        ]
    d= {u:getattr(o,u)() for u in l}
    return d

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBug1(self):
        alg = 'karateclub_NNSED'
        dataname = 'EVAL2_LFR_ud_wu_N1024_mu0.3'
        clu = clustering.load_result(dataname, alg)
        data = dataset.load_local(dataname)
        calc_clu_metrics(data, clu)
        
    def testBug2(self):
        alg = 'cdc_MSCD_LFK2'
        dataname = 'EVAL2_LFR_ud_wu_N1024_mu0.3'
        clu = clustering.load_result(dataname, alg)
        data = dataset.load_local(dataname)
        calc_clu_metrics(data, clu)        

    def testBug3(self):
        alg = 'karateclub_SCD'
        dataname = 'EVAL2_LFR_ud_wu_N1024_mu0.3'
        clu = clustering.load_result(dataname, alg)
        data = dataset.load_local(dataname)
        calc_clu_metrics(data, clu)

    def testBug4(self):
        alg = 'scan_pScan'
        dataname = 'SIMPLE_ud_wu_nc128_cz8_in7_it4'
        clu = clustering.load_result(dataname, alg)
        data = dataset.load_local(dataname)
        gt=list(data.get_ground_truth().values())[0]
        a=calc_clu_metrics(data, gt)
        print(a)
        a=calc_clu_metrics(data, clu)
        print(a)
        a = calc_clu_gt_attrib(gt, clu)
        print(a)

    def testBug5(self):
        alg = 'cdc_MSCD_LFK2'
        dataname = 'EVAL2_LFR_ud_wu_N1024_mu0.3'
        clu = clustering.load_result(dataname, alg)
        data = dataset.load_local(dataname)
        calc_clu_metrics(data, clu)
        gt=list(data.get_ground_truth().values())[0]        
        a = calc_clu_gt_attrib(gt, clu)
        print(a)

    def testBug6(self):
        alg = 'oslom_Infohiermap'
        dataname = 'EVAL2_LFR_ud_wu_N1024_mu0.3'
        clu = clustering.load_result(dataname, alg)
        data = dataset.load_local(dataname)
        a=calc_clu_metrics(data, clu)
        print(a)
        self.assertTrue(not np.isnan(a['cluster_clustering_coefficient']))
                                                                              
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
