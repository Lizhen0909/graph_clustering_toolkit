'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset
from gct.alg.snap_clustering import Clauset_Newman_Moore, Girvan_Newman
from gct.alg import clustering
from gct.exception import UnsupportedException
import sys


from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):

    def tearDown(self):
        pass

    def testClauset_Newman_Moore(self):
        for data in  self.graphs: 
            alg = Clauset_Newman_Moore()
            print(sys._getframe().f_code.co_name, data.name)
            if data.is_directed():
                with self.assertRaises(UnsupportedException) as context:
                    print (alg.run(data).get_result())
            else:
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
 
    def testGirvan_Newman(self):
        for data in  self.graphs: 
            alg = Girvan_Newman()
            print(sys._getframe().f_code.co_name, data.name)
            if data.is_directed():
                with self.assertRaises(UnsupportedException) as context:
                    print (alg.run(data).get_result())
            else:
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
