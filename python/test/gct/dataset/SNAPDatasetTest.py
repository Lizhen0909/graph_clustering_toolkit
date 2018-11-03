'''
Created on Oct 23, 2018

@author: lizhen
'''
import unittest
from gct.dataset.snap_dataset import list_datasets, load_snap_dataset


class Test(unittest.TestCase):

    def testLoadDataset(self):
        for name in list_datasets():
            if name in ['com-DBLP']:
                ds = load_snap_dataset(name, overide=True)
                print (ds)  
                ds = load_snap_dataset(name, overide=False)
                print (ds)  


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoadSNAPDataset']
    unittest.main()
