'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
import gct
from gct import config, utils
import os
from gct.dataset import random_dataset


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Prepare data")
        prefix = Test.__module__
        gct.remove_data(prefix + '_*', dry_run=False)
        graph_unweighted_direct = random_dataset.generate_directed_unweighted_random_graph_LFR(name=prefix + "_tmp", \
                                       N=128, k=16, maxk=16, mu=0.1, minc=32)
        data1 = graph_unweighted_direct.as_undirected(newname=prefix + "_w1")
        data2 = data1.as_mirror_edges(newname=prefix + "_uw1", overide=True)
            
    def setUp(self):
        self.prefix = Test.__module__
        pass 

    def tearDown(self):
        pass

    def has_run(self, runame, dsname):
        fpath = os.path.join(config.get_result_file_path(dsname=dsname, runname=runame), 'result.txt')
        return utils.file_exists(fpath)

    def test_1(self):
        bad_algs = ['igraph_community_optimal_modularity', 'igraph_community_fastgreedy', 'scan_pScan']  # these alg failed for this test
        runned_algs = []
        algs = gct.list_algorithms()
        algs = [u for u in algs if u not in bad_algs and u not in runned_algs]
        datasets = [self.prefix + "_w1", self.prefix + "_uw1"]
        for dsname in datasets:
            for alg in algs:
                runname = alg 
                if not self.has_run(runname, dsname):
                    print ("runing ", alg, dsname)
                    gct.run_alg(runname=runname, data=gct.load_local_graph(dsname), algname=alg)        
                    runned_algs.append(alg)
                    print ("AAAA", runned_algs)
        results = {}
        d = gct.list_all_clustering_results(print_format=False)
        for u in d:
            if self.prefix + "_" in u:
                for run in d[u]:
                    a = gct.load_clustering_result(u, run)
                    print (u, run)
                    results[u + run] = a

        import pandas as pd
        lst = [];
        for alg in algs:
            for dsname in datasets:
                if dsname.startswith(self.prefix + '_uw'):
                    a = [];columns = []
                    dsname2 = dsname.replace(self.prefix + "_uw", self.prefix + "_w")
                    a += [alg, dsname, dsname2]
                    columns += ['alg', 'data1', 'data2']
                    cluster1 = gct.to_cluster(results[dsname + alg])
                    cluster2 = gct.to_cluster(results[dsname2 + alg])
                    compa = gct.ClusterComparator(cluster1, cluster2)
                    gt = list(gct.load_local_graph(dsname).get_ground_truth().values())[0]                    
                    a += [compa.sklean_nmi, cluster1.is_overlap, cluster2.is_overlap,
                          cluster1.num_cluster, cluster2.num_cluster, gt.num_cluster,
                         compa.OvpNMI()['NMImax']]
                    columns += ['nmi_12', 'ovp1', 'ovp2', "#c1", "#c2", '#c_gt', 'ovpnmi_12']
            
                    compa = gct.ClusterComparator(gt, cluster1)            
                    a += [compa.sklean_nmi, compa.OvpNMI()['NMImax']]
                    columns += ['nmi_t1', 'ovpnmi_t1']
                    
                    compa = gct.ClusterComparator(gt, cluster2)            
                    a += [compa.sklean_nmi, compa.OvpNMI()['NMImax']]
                    columns += ['nmi_t2', 'ovpnmi_t2']
                    
                    lst.append(a)
        for alg in bad_algs:
            lst.append([alg] + [None] * (len(columns) - 1))
        rdf = pd.DataFrame(lst, columns=columns)
        with pd.option_context('display.max_rows', 2000, 'display.max_columns', 200):
            print (rdf)
        rdf.to_csv(self.prefix + ".csv", index=None)

        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
