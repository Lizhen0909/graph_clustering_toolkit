import pandas as pd 
from gct.dataset.dataset import local_exists, load_local 
from gct.dataset import convert
from gct import config
import os

_DATASET_ = {
"cities":"cities_edges.csv.gz",
"CSphd":"CSphd_edges.csv.gz",
"cora":"paican_cora_edges.csv.gz",
"hvr":"paican_hvr_edges.csv.gz",
"parliament":"paican_parliament_edges.csv.gz",
"social_papers":"paican_social_papers_edges.csv.gz",
"PairsFSG":"PairsFSG_edges.csv.gz",
"PairsP":"PairsP_edges.csv.gz",
"revije":"revije_edges.csv.gz",
"TAP":"TAP_edges.csv.gz",
"wordnet3":"wordnet3_edges.csv.gz",
"Yeast":"Yeast_edges.csv.gz",

    }


def load_sample_dataset(name, overide=False):
    if not overide and local_exists(name):
        return load_local(name)
    
    else:
        path = os.path.join(config.GCT_HOME, 'data',_DATASET_[name ])
        edges = pd.read_csv(path)
        gt = pd.read_csv(path.replace("_edges", '_gt'))
        description = ""
        directed = False
        return convert.from_edgelist(name, edges, groundtruth=gt, directed=directed, description=description, overide=overide)    


def list_datasets():
    return _DATASET_.keys()

