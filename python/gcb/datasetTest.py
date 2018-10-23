'''
Created on Oct 23, 2018

@author: lizhen
'''
import unittest
from gcb import dataset


class Test(unittest.TestCase):


    def testLoadDataset(self):
        for name in dataset.list_datasets():
            if name in ['com-DBLP']:
                dataset.load_dataset(name) 


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLoadSNAPDataset']
    unittest.main()