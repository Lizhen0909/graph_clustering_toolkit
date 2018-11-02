'''
Created on Oct 27, 2018
include a few algorithms mentioned at https://github.com/eXascaleInfolab/PyCABeM
@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os
import json


class HiReCS(Clustering):

    def __init__(self, name="HiReCS"):
        
        super(HiReCS, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"HiReCS", "name": 'HiReCS' }

    '''
    Usage: ./hirecs [-o{t,c,j}] [-f] [-r] [-m<float>] <adjacency_matrix.hig>
      -o  - output data format. Default: t
        t  - text like representation for logs
        c  - CSV like representation for parcing
        j  - JSON represenation
        je  - extended JSON represenation (j + unwrap root clusters to nodes)
        jd  - detaile JSON represenation (je + show inter-cluster links)
      -c  - clean links, skip links validation
      -f  - fast quazy-mutual clustering (faster). Default: strictly-mutual (better)
      -r  - rand reorder (shuffle) nodes and links on nodes construction
      -m<float>  - modularity profit margin for early exit, float E [-1, 1]. Default: -0.999, but on practice >~= 0
        -1  - skip stderr tracing after each iteration. Recommended: 1E-6 or 0
    '''

    def run(self, data, f=False, m=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params = {}
        params['f'] = f
        params['m'] = m 
        
        if not utils.file_exists(data.file_hig):
            data.to_higformat()
        cmd = ["./hirecs"]
        cmd.append("-oje")
        if f: cmd.append('-f')
        if m is not None: cmd.append("-m{}".format(m))
        cmd.append(data.file_hig)
        cmd.append("> output")
        cmd = " ".join(cmd)
        with utils.TempDir() as tmp_dir:
            with open(os.path.join(tmp_dir, "tmpcmd"), 'wt') as f: f.write(cmd)
            self.logger.info("Running " + cmd)
            cmd = "bash tmpcmd" 
            
            utils.link_file(os.path.join(config.HIRECS_PATH, 'hirecs'), tmp_dir)
            utils.link_file(os.path.join(config.HIRECS_PATH, 'libhirecs.so'), tmp_dir)
            utils.link_file(data.file_hig, tmp_dir)
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as f:
                output = json.load(f)
                
            mod = output['mod']
            communities = output['communities']
            
            clusters = {}
            for c in communities:
                clusters[int(c)] = [int(u) for u in communities[c].keys()]
        
        self.logger.info("Made %d clusters in %f seconds with modularity %f" % (len(clusters), timecost, mod))

        result = {}
        result['algname'] = self.name
        result['params'] = params
        result['overlap'] = True
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
