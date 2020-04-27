import os, sys
import gct
from gct import config,utils
os.environ['OMP_NUM_THREADS']="1"


def has_run(runame, dsname):
    fpath = os.path.join("/{}/tmp/{}_{}.done".format('data', runame,dsname))
    return utils.file_exists(fpath)

def run_alg(alg,dsname, check_skip=True):
    try:
        runname = alg
        if not check_skip or (check_skip and not has_run(runname, dsname)):
            print ("runing ", alg, dsname)
            if alg =='cdc_SVINET':
                gct.run_alg(runname=runname, data=gct.load_local_graph(dsname), algname=alg, seed=123,  max_iterations=1000)        
            else:
                gct.run_alg(runname=runname, data=gct.load_local_graph(dsname), algname=alg, seed=123)
            
            print ("finished", alg,dsname)
        else:
            print("skip", runname,dsname)
    except:
        print("except", runname,dsname)
    fpath = os.path.join("/{}/tmp/{}_{}.done".format('data', runname,dsname))        
    open(fpath,'a').close()
    return True

if __name__ == "__main__":
    # execute only if run as a script
    run_alg(sys.argv[1],sys.argv[2],int(sys.argv[3])>0)