'''
Created on Oct 23, 2018

@author: lizhen
'''
import unittest
from gcb import dataset, random_dataset


class Test(unittest.TestCase):

    def testRandomDataset2(self):
        ds = random_dataset.generate_LFR("test_LFR_unw_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1)
        print ds 
        ds.load()
        
        ds = random_dataset.generate_LFR("test_LFR_w_und", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True)
        print ds 
        ds.load()
        
        ds = random_dataset.generate_LFR("test_LFR_w_dir", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=True, a=1)
        print ds 
        ds.load()
        
        ds = random_dataset.generate_LFR("test_LFR_unw_dir", N=128, k=16, maxk=16, muw=0.1, minc=32, beta=1, weighted=False, a=1)
        print ds 
        ds.load()
        
    def testRandomDataset1(self):
        ds = random_dataset.generate_Erdos_Renyi("test1", 100, 1000, False)
        print ds 
        ds.load()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoadSNAPDataset']
    unittest.main()
