'''
Created on Oct 31, 2018

@author:  Lizhen Shi
'''

import numpy as np
import pandas as pd   
from gct.alg.clustering import Result
import sys
from gct.dataset import convert
from gct.dataset.dataset import Cluster
from gct import utils, config
import os


class GraphMetrics(object):
    '''
    metrics for a graph. e.g. density, diameter etc.
    '''

    def __init__(self, data):
        if data.is_directed() or data.is_weighted():
            print ("Warning! Graph will be taken as undirected.")
        self.data = data 

    def set_if_not_exists(self, name, fun):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            # print ("call fun for " + name)
            value = fun()
            setattr(self, name, value)
            return value 
        
    @property    
    def directed(self):
        return self.data.directed
    
    @property
    def edges(self):

        def f():
            df = self.data.get_edges()
            if not self.data.is_weighted():
                df['weight'] = float(1)
            return df 

        return self.set_if_not_exists("_edges", f)
    
    @property
    def weighted(self):
        return self.data.weighted    
    
    @property 
    def num_edges(self):
        return self.edges.shape[0]
    
    @property 
    def num_vectices(self):
        return self.set_if_not_exists("_num_vetices", lambda: len(set(np.unique(self.edges[['src', 'dest']].values))))

    @property
    def density1(self):
        m, n = self.num_edges, self.num_vectices
        assert n > 1
        return float(m) / n
        
    @property
    def density(self):
        m, n = self.num_edges, self.num_vectices
        assert n > 1
        return float(m) * 2 / n / (n - 1)
    
    @property
    def degrees(self):
        return self.weighted_degrees()
    
    @property
    def unweighted_degrees(self):

        def f():
            arr = self.edges[['src', 'dest']].values.ravel() 
            unique, counts = np.unique(arr, return_counts=True)
            return dict(zip(unique, counts))

        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, f)

    @property
    def weighted_degrees(self):

        def f():
            df1 = self.edges[['src', 'weight']]
            df2 = self.edges[['dest', 'weight']]
            df2.columns = df1.columns
            df = pd.concat([df1, df2])
            return df.groupby('src')['weight'].sum().to_dict()

        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, f)


class GraphClusterMetrics(object):
    '''
    metrics for a clustering of a graph. e.g. modularity.
    '''

    def __init__(self, data, clusterobj):
        if data.is_directed() or data.is_weighted():
            print ("Warning! Graph will be taken as undirected and unweighted.")
        if isinstance(clusterobj, Cluster):
            self.clusterobj = clusterobj
        elif isinstance(clusterobj, Result):
            self.clusterobj = Cluster(clusterobj.clusters(as_dataframe=True))
        elif isinstance(clusterobj, pd.DataFrame) or isinstance(clusterobj, list) \
            or isinstance(clusterobj, np.ndarray) or isinstance(clusterobj, str) or isinstance(clusterobj, dict):
            self.clusterobj = Cluster(clusterobj)
        else:
            raise Exception("Unsupported " + str(type(clusterobj)))
        self.data = data 
        self.clusters = self.clusterobj.value()

    def set_if_not_exists(self, name, fun):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            # print ("call fun for " + name)
            value = fun()
            setattr(self, name, value)
            return value 
    
    @property
    def edges(self):

        def f():
            df = self.data.get_edges()
            if not self.data.is_weighted():
                df['weight'] = float(1)
            return df         

        prop_name = "_" + sys._getframe().f_code.co_name 
        return self.set_if_not_exists(prop_name, f)
    
    @property 
    def num_edges(self):
        return self.edges.shape[0]
    
    @property 
    def num_vectices(self):
        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, lambda: len(set(np.unique(self.edges[['src', 'dest']].values))))

    '''
    degree for each node
    '''    

    @property
    def node_degrees(self):
        return self.unweighted_degrees

    '''
    sum weight for each node
    '''

    @property
    def node_weights(self):
        return self.weighted_degrees

    @property
    def sum_weight(self):
        return np.sum(list(self.node_weights.values()))
        
    @property
    def unweighted_degrees(self):

        def f():
            arr = self.edges[['src', 'dest']].values.ravel() 
            unique, counts = np.unique(arr, return_counts=True)
            return dict(zip(unique, counts))

        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, f)

    @property
    def weighted_degrees(self):

        def f():
            df1 = self.edges[['src', 'weight']]
            df2 = self.edges[['dest', 'weight']]
            df2.columns = df1.columns
            df = pd.concat([df1, df2])
            return df.groupby('src')['weight'].sum().to_dict()

        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, f)

    @property 
    def num_clusters(self):
        return len(self.cluster_indexes)
    
    @property 
    def cluster_indexes(self):
        return self.cluster_sizes.keys()    
    
    @property 
    def cluster_sizes(self):
        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, lambda: self.clusters[['node', 'cluster']].groupby('cluster')['node'].count().to_dict())
    
    @property 
    def cluster_sum_intra_weights(self):

        def f():
            df = self.edges[['src', 'dest', 'weight']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df = df [(df['src_c'] == df['dest_c'])]

            a = df[['src_c', 'weight']].groupby('src_c')['weight'].sum() * 2
            return a.to_dict()
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        

    @property 
    def cluster_sum_weighted_degrees(self):

        def f():
            df = self.clusters[['node', 'cluster']]
            d = self.weighted_degrees
            df['wd'] = df['node'].map(d)
            return df.groupby("cluster")['wd'].sum().to_dict()
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        
        
    @property
    def cluster_edge_sizes(self):

        def f():
            df = self.edges[['src', 'dest']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df['is_intra'] = (df['src_c'] == df['dest_c']).astype(np.float)

            a = df[['src_c', 'is_intra']].groupby('src_c')['is_intra'].sum().to_dict()
            return a 
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        
    
    @property
    def cluster_out_sum_weights(self):

        def f():
            df = self.edges[['src', 'dest', 'weight']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df = df[(df['src_c'] != df['dest_c'])]
            
            a = df.groupby('src_c')[['weight']].sum().reset_index()
            b = df.groupby('dest_c')[['weight']].sum().reset_index() 
            b.columns = a.columns
            a = pd.concat([a, b]).groupby('src_c').sum()
            return a['weight'].to_dict()
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)
        
    @property
    def cluster_expansions(self):
        if self.data.is_weighted():
            raise Exception("only support unweighted graph")

        def f():
            ow = self.cluster_out_sum_weights
            cs = self.cluster_sizes
            return {u:v / cs[u] for u, v in ow.items()}
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        

    @property
    def cluster_cut_ratios(self):
        d = self.cluster_sizes
        n = self.num_vectices
        return {u:v / float(n - d[u]) for u, v in self.cluster_expansions.items()}
    
    @property
    def intra_cluster_densities(self):
        if self.data.is_weighted():
            raise Exception("only support unweighted graph")
        return self.unweighted_intra_cluster_densities
    
    @property
    def unweighted_intra_cluster_densities(self):

        def f():
            r = {}
            d = self.cluster_edge_sizes
            for cluster, n_node in self.cluster_sizes.items():
                n_edge = d[cluster]
                a = float(n_edge) * 2 / n_node / (n_node - 1) if n_node > 1 else 0.0
                r[cluster] = a
            return r 

        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        
    
    @property
    def intra_cluster_density(self):
        return np.mean(list(self.intra_cluster_densities.values()))    

    @property
    def inter_cluster_density(self):
        if self.data.is_weighted():
            raise Exception("only support unweighted graph")        
        return self.inter_unweighted_cluster_density
    
    @property
    def inter_unweighted_cluster_density(self):
        n_intra_edges = np.sum(list(self.cluster_edge_sizes.values()))
        n_edge = self.num_edges
        n = self.num_vectices
        d = n * (n - 1) - np.sum([u * (u - 1) for u in self.cluster_sizes.values()])
        return float(n_edge - n_intra_edges) * 2 / d

    @property
    def relative_cluster_densities(self):

        def f():
            df = self.edges[['src', 'dest', 'weight']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df['is_intra'] = (df['src_c'] == df['dest_c'])
            df['is_inter'] = (df['src_c'] != df['dest_c'])

            a = df[df['is_intra']].groupby('src_c')['weight'].sum()
            b = df[df['is_inter']].groupby('src_c')['weight'].sum()
            c = df[df['is_inter']].groupby('dest_c')['weight'].sum()

            newdf = pd.concat([a, b, c], axis=1).fillna(0)
            newdf.columns = ['intra', 'inter1', 'inter2']
            newdf['density'] = newdf['intra'] / (newdf['inter1'] + newdf['inter2'] + newdf['intra'])
            
            return newdf['density'].to_dict()
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)       

    @property
    def snap_modularities(self):
        import snap

        def f():
            G = convert.to_snap(self.data)
            m = self.num_edges
            ret = {}
            for k, v in self.clusters.groupby('cluster')['node'].apply(lambda u: list(u)).to_dict().items():
                Nodes = snap.TIntV()
                for nodeId in v:
                    Nodes.Add(nodeId)
                mod = snap.GetModularity(G, Nodes, 1024)
                ret[k] = mod 
            return ret 

        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)       

    @property
    def modularity(self):
        return self.modularity2

    @property
    def modularity2(self):  # another formula

        def f():
            c = self.sum_weight
            d = 1.0 / (c * c)
            a = np.sum(list(self.cluster_sum_intra_weights.values())) / c
            b = np.sum([u * u * d for u in self.cluster_sum_weighted_degrees.values()])
            return a - b
            
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)
           
    @property
    def conductance(self):  # another formula

        def f():
            a = self.cluster_out_sum_weights
            d = self.cluster_sum_intra_weights
            return {u:v / (v + d[u]) for u, v in a.items() }
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)       
        
    @property
    def normalized_cut(self):  # another formula

        def f():
            m = self.sum_weight
            a = self.cluster_out_sum_weights
            d = self.cluster_sum_intra_weights
            return {u:v / (v + d[u]) + v / (v + m - d[u]) for u, v in a.items() }
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)       
    
    @property
    def cluster_max_out_degree_fraction(self):
        return self.cluster_out_degree_fraction[0]

    @property
    def cluster_avg_out_degree_fraction(self):
        return self.cluster_out_degree_fraction[1]

    @property
    def cluster_flake_out_degree_fraction(self):
        return self.cluster_out_degree_fraction[2]    
        
    @property
    def cluster_out_degree_fraction(self):

        def f1():
            df = self.edges[['src', 'dest', 'weight']]
            df2 = self.edges[['dest', 'src', 'weight']]
            df2.columns = df.columns 
            df = pd.concat([df, df2]);del df2 
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df1 = df[(df['src_c'] != df['dest_c'])].drop(['dest_c', 'dest'], axis=1)
            df1 = df1.groupby(['src_c', 'src'])["weight"].sum().reset_index()
            df1.columns = ['cluster', 'node', 'inter_weight']
            df2 = df[(df['src_c'] == df['dest_c'])].drop(['dest_c', 'dest'], axis=1)
            df2 = df.groupby(['src_c', 'src'])["weight"].sum().reset_index()
            df2.columns = ['cluster', 'node', 'intra_weight']
            df = pd.merge(df1, df2, on=['cluster', 'node'], how='outer')
            return df

        def f2():
            df = f1()
            df['odf'] = df['inter_weight'] / (df['inter_weight'] + df['intra_weight'])
            df['flake'] = (df['inter_weight'] > df['intra_weight']).astype(np.float)
            max_odf = df.groupby('cluster')['odf'].max().to_dict()
            avg_odf = df.groupby('cluster')['odf'].mean().to_dict()
            flake_odf = df.groupby('cluster')[['flake']].sum()
            d = self.cluster_sizes
            flake_odf['cluster_size'] = flake_odf.index.map(d)
            flake_odf = (flake_odf['flake'] / flake_odf['cluster_size']).to_dict()
            return max_odf, avg_odf, flake_odf

        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f2)
        
    @property
    def separability(self):
        a = self.cluster_out_sum_weights
        b = self.cluster_sum_intra_weights
        return {u:b[u] / float(v) for u, v in a.items() }
        
    @property
    def cluster_clustering_coefficient(self):

        def f1(edges):
            import igraph 
            g = igraph.Graph(edges=edges[['src', 'dest']].values.tolist(), directed=False) 
            return g.transitivity_undirected()

        def f2():
            df = self.edges[['src', 'dest']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df = df[(df['src_c'] == df['dest_c'])]
            
            ret = {}
            for i in self.cluster_indexes:
                edges = df[df['src_c'] == i]
                ret[i] = f1(edges)
            return ret 
        
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f2)

    @property
    def cluster_local_clustering_coefficient(self):

        def f1(edges):
            import igraph 
            g = igraph.Graph(edges=edges[['src', 'dest']].values.tolist(), directed=False) 
            return g.transitivity_local_undirected()

        def f2():
            df = self.edges[['src', 'dest']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df = df[(df['src_c'] == df['dest_c'])]
            
            ret = {}
            for i in self.cluster_indexes:
                edges = df[df['src_c'] == i]
                ret[i] = f1(edges)
            return ret 
        
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f2)


class ClusterComparator(object):
    '''
    metrics for two clustering. e.g. nmi, overlap nmi etc.
    In case that some metrics requires ground truth, take ground truth as the first parameter.
    '''

    def __init__(self, clusterobj1, clusterobj2):
        self.logger = utils.get_logger("{}".format(type(self).__name__))

        def to_obj(clusterobj):
            if isinstance(clusterobj, Cluster):
                return  clusterobj
            elif isinstance(clusterobj, Result):
                return  Cluster(clusterobj.clusters(as_dataframe=True))
            elif isinstance(clusterobj, pd.DataFrame) or isinstance(clusterobj, list) \
                or isinstance(clusterobj, np.ndarray) or isinstance(clusterobj, str) or isinstance(clusterobj, dict):
                return Cluster(clusterobj)
            else:
                raise Exception("Unsupported " + str(type(clusterobj)))
        
        self.clusterobj1 = to_obj(clusterobj1) 
        self.clusterobj2 = to_obj(clusterobj2)
        
        if self.clusterobj1.is_overlap or  self.clusterobj2.is_overlap: 
            self.overlap = True 
        else:
            self.overlap = False  
        
        def clean():
            df1 = self.clusterobj1.value()
            df2 = self.clusterobj2.value()
            nodes = set(df1['node']).intersection(set(df2['node']))
            self.logger.info ("resulting {} nodes out of {},{}".format(len(nodes), len(df1), len(df2)))
            df1 = df1[df1['node'].isin(nodes)].set_index('node')
            df2 = df2[df2['node'].isin(nodes)].set_index('node').loc[df1.index]
            df2.index.name = 'node'
            return df1, df2 

        if not self.overlap:
            self.clean_clusterobj1, self.clean_clusterobj2 = clean()
    
    @property 
    def ground_truth(self):  # assume the first one is ground truth
        return self.clusterobj1
    
    @property 
    def clean_ground_truth(self):  # assume the first one is ground truth
        return self.clean_clusterobj1

    @property 
    def predition(self): 
        return self.clusterobj2

    @property 
    def clean_prediction(self): 
        return self.clean_clusterobj2
    
    @property
    def sklean_nmi(self):
        if self.overlap:
            return None 
        else:
            prop_name = "_" + sys._getframe().f_code.co_name 

            def f():
                from sklearn.metrics.cluster import normalized_mutual_info_score            
                return normalized_mutual_info_score(self.clean_clusterobj1['cluster'].values, self.clean_clusterobj2['cluster'].values)

            return utils.set_if_not_exists(self, prop_name, f)
    
    @property
    def sklean_ami(self):
        if self.overlap:
            return None 
        else:
            prop_name = "_" + sys._getframe().f_code.co_name 

            def f():
                from sklearn.metrics.cluster import adjusted_mutual_info_score            
                return adjusted_mutual_info_score(self.clean_clusterobj1['cluster'].values, self.clean_clusterobj2['cluster'].values)

            return utils.set_if_not_exists(self, prop_name, f)

    @property
    def sklean_ars(self):
        if self.overlap:
            return None 
        else:
            prop_name = "_" + sys._getframe().f_code.co_name 

            def f():
                from sklearn.metrics.cluster import adjusted_rand_score            
                return adjusted_rand_score(self.clean_clusterobj1['cluster'].values, self.clean_clusterobj2['cluster'].values)

            return utils.set_if_not_exists(self, prop_name, f)

    @property
    def sklean_completeness(self):
        if self.overlap:
            return None 
        else:
            prop_name = "_" + sys._getframe().f_code.co_name 

            def f():
                from sklearn.metrics.cluster import completeness_score            
                return completeness_score(self.clean_ground_truth['cluster'].values, self.clean_prediction['cluster'].values)

            return utils.set_if_not_exists(self, prop_name, f)
    
    '''
    wrapper for https://github.com/eXascaleInfolab/GenConvNMI
    
    Usage:  ./gecmi [options] <clusters1> <clusters2>
    clusters  - clusters file in the CNL format (https://github.com/eXascaleInfolab/PyCABeM/blob/master/formats/format.cnl), where each line lists space separated ids of the cluster members
    
    Options:
      -h [ --help ]                produce help message
      --input arg                  name of the input files
      -s [ --sync ]                synchronize the node base omitting the 
                                   non-matching nodes for the fair evaluation. The 
                                   node base is selected automatically as a 
                                   clustering having the least number of nodes.
      -i [ --id-remap ]            remap ids allowing arbitrary input ids 
                                   (non-contiguous ranges), otherwise ids should 
                                   form a solid range and start from 0 or 1
      -n [ --nmis ]                output both NMI [max] and NMI_sqrt
      -f [ --fnmi ]                evaluate also FNMI, includes '-n'
      -r [ --risk ] arg (=0.01)    probability of value being outside
      -e [ --error ] arg (=0.01)   admissible error
      -a [ --fast ]                apply fast approximate evaluations that are less
                                   accurate, but much faster on large networks
      -m [ --membership ] arg (=1) average expected membership of nodes in the 
                                   clusters, > 0, typically >= 1
      -d [ --retain-dups ]         retain duplicated clusters if any instead of 
                                   filtering them out (not recommended)
    
    '''

    def GenConvNMI(self, sync=None, id_remap=None, nmis=None, fnmi=True, risk=None, error=None, fast=None, membership=None, retain_dups=None):
        params = locals(); del params['self'];del params['sync']
        params = {u.replace('_', '-'):v for u, v in params.items() if v}
        nonbools = ['risk', 'error', 'membership']
        cmd = [config.GECMI_PROG]
        for u, v in params.items():
            if u in nonbools:
                cmd.append("--{} {}".format(u, v))
            else:
                if v:
                    cmd.append ("--{}".format(u))

        if sync:
            cmd.append("--sync -")
        with utils.TempDir() as tmp_dir:
            cnl1 = self.clusterobj1.make_cnl_file(filepath=os.path.join(tmp_dir, 'cluster1.cnl'))
            cnl2 = self.clusterobj2.make_cnl_file(filepath=os.path.join(tmp_dir, 'cluster2.cnl'))
            cmd.append(cnl1)
            cmd.append(cnl2)
            cmd.append("> nmioutput")
            cmd = " ".join(cmd)            
            self.logger.info("Running " + cmd)
            with open(os.path.join(tmp_dir, "tmpcmd"), 'wt') as f: f.write(cmd)            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait("bash tmpcmd", tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "nmioutput"), "r") as output:
                line = [u.strip() for u in output.readlines() if not u.startswith('#')][0]
                line = line.split(";")[0]
                if not nmis and not fnmi: 
                    res = {'NMI_max':float(line)}
                else:
                    lst = [u.split(":") for u in line.split(",")]
                    res = dict([ (k.strip(), float(v.strip())) for k, v in lst])
            return res 

    '''
    Compare sets of clusters by their members (nodes) using various measures (NMI,
    Omega) and considering overlaps
    
    Usage: onmi [OPTIONS] clsfile1 clsfile2
    
      -h, --help              Print help and exit
      -V, --version           Print version and exit
      -s, --sync=filename     synchronize the node base omitting the non-matching
                                nodes.
                                NOTE: The node base is either the first input file
                                or '-' (automatic selection of the input file
                                having the least number of nodes).
      -a, --allnmis           output all NMIs (sqrt and sum-denominators, LFK
                                besides the max-denominator)  (default=off)
      -m, --membership=FLOAT  average expected membership of nodes in the clusters,
                                > 0, typically >= 1  (default=`1')
      -o, --omega             print the Omega measure (can be slow)  (default=off)
      -t, --textid            use text ids of nodes instead of .cnl format
                                (default=off)
      -v, --verbose           detailed debugging  (default=off)
    
    '''        

    def OvpNMI(self, sync=None, allnmi=None, omega=None, membership=None, verbose=None):
        if self.clusterobj1.num_cluster < 2 or self.clusterobj2.num_cluster < 2:
            return {"NMImax":None}
        params = locals(); del params['self'];del params['sync']
        params = {u.replace('_', '-'):v for u, v in params.items() if v}
        nonbools = [ 'membership']
        cmd = [config.ONMI_PROG]
        for u, v in params.items():
            if u in nonbools:
                cmd.append("--{} {}".format(u, v))
            else:
                if v:
                    cmd.append ("--{}".format(u))

        if sync:
            cmd.append("--sync")

        with utils.TempDir() as tmp_dir:
            # tmp_dir="/tmp/abc"
            cnl1 = self.clusterobj1.make_cnl_file(filepath=os.path.join(tmp_dir, 'cluster1.cnl'))
            cnl2 = self.clusterobj2.make_cnl_file(filepath=os.path.join(tmp_dir, 'cluster2.cnl'))
            cmd.append(cnl1)
            cmd.append(cnl2)
            cmd.append("> ovpnmioutput")
            cmd = " ".join(cmd)            
            self.logger.info("Running " + cmd)
            with open(os.path.join(tmp_dir, "tmpcmd"), 'wt') as f: f.write(cmd)            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait("bash tmpcmd", tmp_dir))
            if status != 0: 
                self.logger.error(Exception("Run command with error status code {}".format(status)))
                return {"NMImax":None} 
            
            with open (os.path.join(tmp_dir, "ovpnmioutput"), "r") as output:
                line = [u.strip() for u in output.readlines() if not u.startswith('#')][0]
                line = line.split(";")[0]
                if not allnmi and not omega: 
                    res = {'NMImax':float(line)}
                else:
                    lst = [u.split(":")[:2] for u in line.split(",")]
                    lst = [ (k.strip(), v.strip().split(" ")[0]) for k, v in lst]
                    res = dict([ (k.strip(), float(v.strip())) for k, v in lst])
            return res 
        
    '''
    Evaluating measures are:
      - OI  - Omega Index (a fuzzy version of the Adjusted Rand Index, identical to
    the Fuzzy Rand Index), which yields the same value as Adjusted Rand Index when
    applied to the non-overlapping clusterings.
      - [M]F1  - various [mean] F1 measures of the Greatest (Max) Match including
    the Average F1-Score (suggested by J. Leskovec) with optional weighting.
    NOTE: There are 3 matching policies available for each kind of F1. The most
    representative evaluation is performed by the F1p with combined matching
    policy (considers both micro and macro weighting).
      - NMI  - Normalized Mutual Information, normalized by either max or also
    sqrt, avg and min information content denominators.
    ATTENTION: This is a standard NMI, which should be used ONLY for the HARD
    partitioning evaluation (non-overlapping clustering on a single resolution).
    It penalizes overlapping and multi-resolution structures.
    
    
      -h, --help                    Print help and exit
      -V, --version                 Print version and exit
      -O, --ovp                     evaluate overlapping instead of the
                                      multi-resolution clusters, where max matching
                                      for any shared member between R overlapping
                                      clusters is 1/R (the member is shared)
                                      instead of 1 (the member fully belongs to
                                      each [hierarchical  sub]group) for the member
                                      belonging to R distinct clusters on R
                                      resolutions.
                                      NOTE: It has no effect for the Omega Index
                                      evaluation.  (default=off)
      -q, --unique                  ensure on loading that all cluster members are
                                      unique by removing all duplicates.
                                      (default=off)
      -s, --sync=filename           synchronize with the specified node base
                                      omitting the non-matching nodes.
                                      NOTE: The node base can be either a separate,
                                      or an evaluating CNL file, in the latter case
                                      this option should precede the evaluating
                                      filename not repeating it
      -m, --membership=FLOAT        average expected membership of the nodes in the
                                      clusters, > 0, typically >= 1. Used only to
                                      facilitate estimation of the nodes number on
                                      the containers preallocation if this number
                                      is not specified in the file header.
                                      (default=`1')
      -d, --detailed                detailed (verbose) results output
                                      (default=off)
    
    Omega Index:
      -o, --omega                   evaluate Omega Index (a fuzzy version of the
                                      Adjusted Rand Index, identical to the Fuzzy
                                      Rand Index and on the non-overlapping
                                      clusterings equals to ARI).  (default=off)
      -x, --extended                evaluate extended (Soft) Omega Index, which
                                      does not excessively penalize distinctly
                                      shared nodes.  (default=off)
    
    Mean F1:
      -f, --f1[=ENUM]               evaluate mean F1 of the [weighted] average of
                                      the greatest (maximal) match by F1 or partial
                                      probability.
                                      NOTE: F1p <= F1h <= F1a, where:
                                       - p (F1p or Ph)  - Harmonic mean (F1) of two
                                      [weighted] averages of the Partial
                                      Probabilities, the most indicative as
                                      satisfies the largest number of the Formal
                                      Constraints (homogeneity, completeness and
                                      size/quantity except the rag bag in some
                                      cases);
                                       - h (F1h)  - Harmonic mean (F1) of two
                                      [weighted] averages of all local F1 (harmonic
                                      means of the Precision and Recall of the best
                                      matches of the clusters);
                                       - a (F1a)  - Arithmetic mean (average) of
                                      two [weighted] averages of all local F1, the
                                      least discriminative and satisfies the lowest
                                      number of the Formal Constraints.
                                        (possible values="partprob",
                                      "harmonic", "average" default=`partprob')
      -k, --kind[=ENUM]             kind of the matching policy:
                                       - w  - Weighted by the number of nodes in
                                      each cluster
                                       - u  - Unweighed, where each cluster is
                                      treated equally
                                       - c  - Combined(w, u) using geometric mean
                                      (drops the value not so much as harmonic
                                      mean)
                                        (possible values="weighted",
                                      "unweighed", "combined"
                                      default=`weighted')
    
    Clusters Labeling & F1 evaluation with Precision and Recall:
      -l, --label=gt_filename       label evaluating clusters with the specified
                                      ground-truth (gt) cluster indices and
                                      evaluate F1 (including Precision and Recall)
                                      of the (best) MATCHED labeled clusters only
                                      (without the probable subclusters).
                                      NOTE: If 'sync' option is specified then the
                                      file name  of the clusters labels should be
                                      the same as the node base (if specified) and
                                      should be in the .cnl format. The file name
                                      can be either a separate or an evaluating CNL
                                      file, in the latter case this option should
                                      precede the evaluating filename not repeating
                                      it.
      -p, --policy[=ENUM]           Labels matching policy:
                                       - p  - Partial Probabilities (maximizes
                                      gain)
                                       - h  - Harmonic Mean (minimizes loss,
                                      maximizes F1)
                                        (possible values="partprob", "harmonic"
                                      default=`harmonic')
      -u, --unweighted              Labels weighting policy on F1 evaluation:
                                      weighted by the number of instances in each
                                      label or unweighed, where each label is
                                      treated equally  (default=off)
      -i, --identifiers=labels_filename
                                    output labels (identifiers) of the evaluating
                                      clusters as lines of space-separated indices
                                      of the ground-truth clusters (.cll - clusters
                                      labels list)
                                      NOTE: If 'sync' option is specified then the
                                      reduced collection is outputted to the
                                      <labels_filename>.cnl besides the
                                      <labels_filename>
    
    
    NMI:
      -n, --nmi                     evaluate NMI (Normalized Mutual Information),
                                      applicable only to the non-overlapping
                                      clusters  (default=off)
      -a, --all                     evaluate all NMIs using sqrt, avg and min
                                      denominators besides the max one
                                      (default=off)
      -e, --ln                      use ln (exp base) instead of log2 (Shannon
                                      entropy, bits) for the information measuring
                                      (default=off)
    '''        

    def xmeasure_nmi(self, sync=None, all=False, membership=None, detailed=None):
        params = locals(); del params['self'];del params['sync']
        params = {u.replace('_', '-'):v for u, v in params.items() if v}
        nonbools = [ 'membership']
        cmd = [config.XMEASURES_PROG]
        for u, v in params.items():
            if u in nonbools:
                cmd.append("--{} {}".format(u, v))
            else:
                if v:
                    cmd.append ("--{}".format(u))
        
        cmd.append("--nmi") 
        if sync:
            cmd.append("--sync")

        with utils.TempDir() as tmp_dir:
            cnl1 = Cluster(self.clean_ground_truth.reset_index()).make_cnl_file(filepath=os.path.join(tmp_dir, 'cluster1.cnl'))
            cnl2 = Cluster(self.clean_prediction.reset_index()).make_cnl_file(filepath=os.path.join(tmp_dir, 'cluster2.cnl'))
            cmd.append(cnl1)
            cmd.append(cnl2)
            cmd.append("> xmeasurenmioutput")
            cmd = " ".join(cmd)            
            self.logger.info("Running " + cmd)
            with open(os.path.join(tmp_dir, "tmpcmd"), 'wt') as f: f.write(cmd)            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait("bash tmpcmd", tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "xmeasurenmioutput"), "r") as output:
                line = [u.strip() for u in output.readlines() if not u.startswith('=')][-1]
                line = line.split(";")[0]
                if not all: 
                    res = {'NMI_max':float(line)}
                else:
                    lst = [u.split(":")[:2] for u in line.split(",")]
                    lst = [ (k.strip(), v.strip().split(" ")[0]) for k, v in lst]
                    res = dict([ (k.strip(), float(v.strip())) for k, v in lst])
            return res 

    def xmeasure(self, sync=None, ovp=None, unique=None, omega=None, extended=None, f1=None, kind=False, membership=None, detailed=None):
        assert not(omega is None and f1 is None)
        params = locals(); del params['self'];del params['sync']
        params = {u.replace('_', '-'):v for u, v in params.items() if v}
        if f1 is not None: assert f1 in ['p', 'h', 'a']
        nonbools = [ 'membership', 'f1', 'kind']
        cmd = [config.XMEASURES_PROG]
        for u, v in params.items():
            if u in nonbools:
                cmd.append("--{}={}".format(u, v))
            else:
                if v:
                    cmd.append ("--{}".format(u))
        
        if sync:
            cmd.append("--sync")

        with utils.TempDir() as tmp_dir:
            cnl1 = Cluster(self.clean_ground_truth.reset_index()).make_cnl_file(filepath=os.path.join(tmp_dir, 'cluster1.cnl'))
            cnl2 = Cluster(self.clean_prediction.reset_index()).make_cnl_file(filepath=os.path.join(tmp_dir, 'cluster2.cnl'))
            cmd.append(cnl1)
            cmd.append(cnl2)
            cmd.append("> xmeasureoutput")
            cmd = " ".join(cmd)            
            self.logger.info("Running " + cmd)
            with open(os.path.join(tmp_dir, "tmpcmd"), 'wt') as f: f.write(cmd)            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait("bash tmpcmd", tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "xmeasureoutput"), "r") as output:
                lines = [u.strip() for u in output.readlines() if not u.startswith('=') and not ";"  in u]
                ret = {}
                assert len(lines) in [2, 4]
                ret [lines[0].split(" ")[0].strip()] = float(lines[1])
                if len(lines) == 4:
                    ret [lines[2].split(" ")[0].strip()] = float(lines[3])
            return ret, params 
