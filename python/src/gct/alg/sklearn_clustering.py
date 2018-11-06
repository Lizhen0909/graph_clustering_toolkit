'''
Created on Oct 27, 2018
include a few algorithms mentioned at https://github.com/eXascaleInfolab/PyCABeM
@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os
import json
import glob
from gct.dataset import convert
import sklearn.cluster
import numpy as np 
from typing import DefaultDict

prefix = 'sklearn'


class AffinityPropagation(Clustering):
    '''
    A wrapper of *AffinityPropagation* algorithm from http://scikit-learn.org. 

    Parameters
    ----------
    damping : float, optional, default: 0.5
        Damping factor (between 0.5 and 1) is the extent to
        which the current value is maintained relative to
        incoming values (weighted 1 - damping). This in order
        to avoid numerical oscillations when updating these
        values (messages).
    max_iter : int, optional, default: 200
        Maximum number of iterations.
    convergence_iter : int, optional, default: 15
        Number of iterations with no change in the number
        of estimated clusters that stops the convergence.
    verbose : boolean, optional, default: False
        Whether to be verbose.
        
    Reference
    ------------------------
    Brendan J. Frey and Delbert Dueck, “Clustering by Passing Messages Between Data Points”, Science Feb. 2007
    
    '''

    def __init__(self, name="sklearn_AffinityPropagation"):
        
        super(AffinityPropagation, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"sklearn", "name": 'AffinityPropagation' }

    def run(self, data, damping=None, max_iter=None, convergence=None, verbose=None):
        
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params = locals();del params['self'];del params['data']
        params = {u:v for u, v in params.items() if v is not None}
        params['affinity'] = 'precomputed'
        params['copy'] = False

        A = convert.to_coo_adjacency_matrix(data, simalarity=True)

        def fun():
            obj = sklearn.cluster.AffinityPropagation(**params)
            return obj.fit_predict(A.toarray())

        timecost, res = utils.timeit(fun)
        
        clusters = DefaultDict(list)
        for i, c in enumerate(res):
            clusters[str(c)].append(i)
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))

        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 


class SpectralClustering(Clustering):
    '''
    A wrapper of *SpectralClustering* algorithm from http://scikit-learn.org. 

    Parameters
    -----------
    eigen_solver : {None, 'arpack', 'lobpcg', or 'amg'}
        The eigenvalue decomposition strategy to use. AMG requires pyamg
        to be installed. It can be faster on very large, sparse problems,
        but may also lead to instabilities
    random_state : int, RandomState instance or None (default)
        A pseudo random number generator used for the initialization of the
        lobpcg eigen vectors decomposition when eigen_solver == 'amg' and by
        the K-Means initialization. Use an int to make the randomness
        deterministic.
        See :term:`Glossary <random_state>`.
    n_init : int, optional, default: 10
        Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia.
    gamma : float, default=1.0
        Kernel coefficient for rbf, poly, sigmoid, laplacian and chi2 kernels.
        Ignored for ``affinity='nearest_neighbors'``.
    n_neighbors : integer
        Number of neighbors to use when constructing the affinity matrix using
        the nearest neighbors method. Ignored for ``affinity='rbf'``.
    eigen_tol : float, optional, default: 0.0
        Stopping criterion for eigendecomposition of the Laplacian matrix
        when using arpack eigen_solver.
    assign_labels : {'kmeans', 'discretize'}, default: 'kmeans'
        The strategy to use to assign labels in the embedding
        space. There are two ways to assign labels after the laplacian
        embedding. k-means can be applied and is a popular choice. But it can
        also be sensitive to initialization. Discretization is another approach
        which is less sensitive to random initialization.
    degree : float, default=3
        Degree of the polynomial kernel. Ignored by other kernels.
    coef0 : float, default=1
        Zero coefficient for polynomial and sigmoid kernels.
        Ignored by other kernels.
    kernel_params : dictionary of string to any, optional
        Parameters (keyword arguments) and values for kernel passed as
        callable object. Ignored by other kernels.
    n_jobs : int or None, optional (default=None)
        The number of parallel jobs to run.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.
        
    Reference
    ------------------------
    Normalized cuts and image segmentation, 2000 Jianbo Shi, Jitendra Malik http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.160.2324
    A Tutorial on Spectral Clustering, 2007 Ulrike von Luxburg http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.165.9323
    Multiclass spectral clustering, 2003 Stella X. Yu, Jianbo Shi http://www1.icsi.berkeley.edu/~stellayu/publication/doc/2003kwayICCV.pdf
    '''

    def __init__(self, name="sklearn_SpectralClustering"):
        
        super(SpectralClustering, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"sklearn", "name": 'SpectralClustering' }

    def run(self, data, **kargs):
        
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params = dict(kargs)
        params['affinity'] = 'precomputed'
        if  False and ('eigen_solver' not in params or params['eigen_solver'] is None):
            if utils.check_module_available('pyamg'):
                pass 
                params['eigen_solver'] = 'amg'
        A = convert.to_coo_adjacency_matrix(data, simalarity=True)

        def fun():
            obj = sklearn.cluster.SpectralClustering(**params)
            return obj.fit_predict(A)

        timecost, res = utils.timeit(fun)
        
        clusters = DefaultDict(list)
        for i, c in enumerate(res):
            clusters[str(c)].append(i)
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))

        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 


class DBSCAN(Clustering):
    '''
    A wrapper of *DBSCAN* algorithm from http://scikit-learn.org. 

   Parameters
    ----------
    eps : float, optional
        The maximum distance between two samples for them to be considered
        as in the same neighborhood.
    min_samples : int, optional
        The number of samples (or total weight) in a neighborhood for a point
        to be considered as a core point. This includes the point itself.
    algorithm : {'auto', 'ball_tree', 'kd_tree', 'brute'}, optional
        The algorithm to be used by the NearestNeighbors module
        to compute pointwise distances and find nearest neighbors.
        See NearestNeighbors module documentation for details.
    leaf_size : int, optional (default = 30)
        Leaf size passed to BallTree or cKDTree. This can affect the speed
        of the construction and query, as well as the memory required
        to store the tree. The optimal value depends
        on the nature of the problem.
    p : float, optional
        The power of the Minkowski metric to be used to calculate distance
        between points.
    n_jobs : int or None, optional (default=None)
        The number of parallel jobs to run.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.
    Reference
    ------------------------
    Ester, M., H. P. Kriegel, J. Sander, and X. Xu, “A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise”. In: Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining, Portland, OR, AAAI Press, pp. 226-231. 1996    
    '''

    def __init__(self, name="sklearn_DBSCAN"):
        
        super(DBSCAN, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"sklearn", "name": 'DBSCAN' }

    def run(self, data, **kargs):
        
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params = dict(kargs)
        
        params['metric'] = 'precomputed'
        A = convert.to_coo_adjacency_matrix(data, simalarity=False, distance_fun='exp_minus')
        params['eps'] = np.median(A.data)

        def fun():
            obj = sklearn.cluster.DBSCAN(**params)
            return obj.fit_predict(A)

        timecost, res = utils.timeit(fun)
        
        clusters = DefaultDict(list)
        for i, c in enumerate(res):
            clusters[str(c)].append(i)
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))

        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
