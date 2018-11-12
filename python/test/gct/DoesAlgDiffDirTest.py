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
        data1 = random_dataset.generate_directed_unweighted_random_graph_LFR(name=prefix + "_1", \
                                       N=128, k=16, maxk=32, mu=0.2, minc=32)
        data2 = data1.as_undirected(newname=prefix + "_2")
            
    def setUp(self):
        self.prefix = Test.__module__
        pass 

    def tearDown(self):
        pass

    def has_run(self, runame, dsname):
        fpath = os.path.join(config.get_result_file_path(dsname=dsname, runname=runame), 'result.txt')
        return utils.file_exists(fpath)

    def test_1(self):
        bad_algs = ['igraph_community_multilevel', 'igraph_community_fastgreedy', 'igraph_community_optimal_modularity', 'scan_pScan', 'snap_Clauset_Newman_Moore', 'snap_Girvan_Newman', 'alg_Paris']  # these alg failed for this test
        runned_algs = ['oslom_Infohiermap', 'oslom_Infomap', 'oslom_OSLOM', 'oslom_copra', 'oslom_louvain_method', 'oslom_lpm', 'oslom_modopt', 'pycabem_GANXiSw', 'pycabem_HiReCS', 'pycabem_LabelRank', 'cgcc_CGGC', 'dct_dlplm', 'dct_dlslm', 'dct_dlslm_map_eq', 'dct_dlslm_no_contraction', 'dct_dlslm_with_seq', 'dct_infomap', 'dct_seq_louvain', 'igraph_community_edge_betweenness', 'igraph_community_infomap', 'igraph_community_label_propagation', 'igraph_community_leading_eigenvector', 'igraph_community_spinglass', 'igraph_community_walktrap', 'mcl_MCL', 'networkit_CutClustering', 'networkit_LPDegreeOrdered', 'networkit_PLM', 'networkit_PLP', 'alg_GossipMap', 'alg_RelaxMap', 'alg_label_propagation', 'scan_AnyScan', 'scan_Scanpp', 'sklearn_AffinityPropagation', 'sklearn_DBSCAN', 'sklearn_SpectralClustering']
        runned_algs = []
        algs = gct.list_algorithms()
        algs = [u for u in algs if u not in bad_algs and u not in runned_algs]
        datasets = [self.prefix + "_1", self.prefix + "_2"]
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
                if dsname.startswith(self.prefix + '_1'):
                    a = [];columns = []
                    dsname2 = self.prefix + "_2"
                    a += [alg, dsname, dsname2]
                    columns += ['alg', 'data1', 'data2']
                    if dsname + alg in results and dsname2 + alg in results:
                        cluster1 = gct.to_cluster(results[dsname + alg])
                        cluster2 = gct.to_cluster(results[dsname2 + alg])
                        compa = gct.ClusterComparator(cluster1, cluster2)
                        gt = list(gct.load_local_graph(dsname).get_ground_truth().values())[0]                    
                        a += [compa.sklean_nmi, gt.is_overlap, cluster1.is_overlap, cluster2.is_overlap,
                              cluster1.num_cluster, cluster2.num_cluster, gt.num_cluster]
                        columns += ['nmi_12', 'ovp_gt', 'ovp1', 'ovp2', "#c1", "#c2", '#c_gt']
                
                        compa = gct.ClusterComparator(gt, cluster1)            
                        a += [compa.sklean_nmi]
                        columns += ['nmi_t1']
                        
                        compa = gct.ClusterComparator(gt, cluster2)            
                        a += [compa.sklean_nmi]
                        columns += ['nmi_t2']
                        
                        lst.append(a)
                    else:
                        bad_algs.append(alg)
        for alg in bad_algs:
            lst.append([alg] + [None] * (len(columns) - 1))
        rdf = pd.DataFrame(lst, columns=columns)
        with pd.option_context('display.max_rows', 2000, 'display.max_columns', 200):
            print (rdf)
        rdf.to_csv(self.prefix + ".csv", index=None)

        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
