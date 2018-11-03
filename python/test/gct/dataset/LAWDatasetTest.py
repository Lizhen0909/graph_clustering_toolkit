'''
Created on Oct 23, 2018

@author: lizhen
'''
import unittest
from gct.dataset import law_dataset as dataset 


class Test(unittest.TestCase):

    def testLoadDataset(self):
        return #TBD
        for name in dataset.list_datasets():
            if name in ['cnr-2000']:
                ds = dataset.get_dataset(name)
                print (ds)  
                ds.load()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoadSNAPDataset']
    unittest.main()
