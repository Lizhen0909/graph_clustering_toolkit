'''
Created on Oct 23, 2018

@author: lizhen
'''
import unittest
from gct.dataset.sample_dataset import list_datasets, load_sample_dataset, \
    _DATASET_
from gct import config
import os
import pandas as pd 


class Test(unittest.TestCase):

    def testCheckData(self):
        for name in list_datasets():
            path = os.path.join(config.GCT_HOME, 'data', _DATASET_[name ])
            edges = pd.read_csv(path)
            self.assertTrue('src' in edges.columns)
            self.assertTrue('dest' in edges.columns)
            gt = pd.read_csv(path.replace("_edges", '_gt'))
            self.assertTrue('node' in gt.columns)
            self.assertTrue('cluster' in gt.columns)

    def testLoadDataset(self):
        for name in list_datasets():
            ds = load_sample_dataset(name, overide=True)
            print (ds)  
            ds = load_sample_dataset(name, overide=False)
            print (ds)  


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoadSNAPDataset']
    unittest.main()
