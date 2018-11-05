'''
Created on Nov 4, 2018

@author: bo
'''
import unittest

from gct import alg 

class Test(unittest.TestCase):


    def testAlg(self):
        lst = alg.list_algorithms()
        print ("{} has {} algorithms: {}".format(alg.__name__, len(lst), str(lst)))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAlg']
    unittest.main()