'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
import traceback
from gct.alg import clustering
from gct.alg.karateclub_clustering import EdMot, SCD, EgoNetSplitter, DANMF, NNSED, BigClam, SymmNMF
import sys
from gct.alg.AlgTestBase import AlgTestBase


class Test(AlgTestBase):

    def tearDown(self):
        pass
    
    def testSymmNMFClam(self):
        for data in  self.graphs:
            if data.is_directed():
                continue
            try: 
                alg = SymmNMF()
                print(sys._getframe().f_code.co_name, data.name) 
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
            except:
                traceback.print_exc() 
    
    def testBigClam(self):
        for data in  self.graphs:
            if data.is_directed():
                continue
            try: 
                alg = BigClam()
                print(sys._getframe().f_code.co_name, data.name) 
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
            except:
                traceback.print_exc() 
                
    def testNNSED(self):
        for data in  self.graphs:
            if data.is_directed():
                continue
            try: 
                alg = NNSED()
                print(sys._getframe().f_code.co_name, data.name) 
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
            except:
                traceback.print_exc() 

    def testDANMF(self):
        for data in  self.graphs:
            if data.is_directed():
                continue
            try: 
                alg = DANMF()
                print(sys._getframe().f_code.co_name, data.name) 
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
            except:
                traceback.print_exc() 

    def testEgoNetSplitterMot(self):
        for data in  self.graphs:
            if data.is_directed():
                continue
            try: 
                alg = EgoNetSplitter()
                print(sys._getframe().f_code.co_name, data.name) 
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
            except:
                traceback.print_exc() 

    def testEdMot(self):
        for data in  self.graphs:
            if data.is_directed():
                continue
            try: 
                alg = EdMot()
                print(sys._getframe().f_code.co_name, data.name) 
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
            except:
                traceback.print_exc() 

    def testSCD(self):
        for data in  self.graphs:
            if data.is_directed():
                continue
            try: 
                alg = SCD()
                print(sys._getframe().f_code.co_name, data.name) 
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))
            except:
                traceback.print_exc() 

                            
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
