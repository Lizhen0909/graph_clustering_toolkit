'''
Created on Oct 27, 2018

@author: lizhen
'''
import unittest
from gct.dataset import random_dataset,dataset
from gct.alg import clustering
import sys
from gct.alg.cdc_clustering import CliquePercolation, Connected_Iterative_Scan, \
    EAGLE, clique_modularity, CONGA, LinkCommunities, TopGC, GCE, MOSES, ParCPM,\
    DEMON, HDEMON, FastCpm, MSCD_RB, MSCD_AFG, MSCD_HSLSW, MSCD_LFK, MSCD_LFK2,\
    MSCD_RN, MSCD_SO, MSCD_SOM, SVINET
from gct.dataset.dataset import create_dataset
from gct.exception import UnsupportedException

from gct.alg.AlgTestBase import AlgTestBase

class Test(AlgTestBase):

    def tearDown(self):
        pass

    def test_CliquePercolation(self):
        for data in  self.graphs: 
            alg = CliquePercolation()
            print(sys._getframe().f_code.co_name)
            if data.is_directed():
                with self.assertRaises(UnsupportedException) as context:
                    print (alg.run(data, k=3).get_result())
            else:
                print (alg.run(data, k=3).get_result())
                print (clustering.load_result(data.name, alg.name))

    def test_Connected_Iterative_ScanPercolation(self):
        for data in  self.graphs: 
            alg = Connected_Iterative_Scan()
            print(sys._getframe().f_code.co_name)
            print (alg.run(data, l=0.).get_result())
            print (clustering.load_result(data.name, alg.name))
            
    def test_EAGLE(self):
        for data in  self.graphs: 
            alg = EAGLE()
            print(sys._getframe().f_code.co_name)
            print (alg.run(data, nThread=2).get_result())
            print (clustering.load_result(data.name, alg.name))            

    def test_clique_modularity(self):
        for data in  self.graphs: 
            alg = clique_modularity()
            print(sys._getframe().f_code.co_name)
            print (alg.run(data, method="KJ").get_result())
            print (clustering.load_result(data.name, alg.name))

    def test_CONGA(self):
        for data in  self.graphs: 
            alg = CONGA()
            print(sys._getframe().f_code.co_name)
            print (alg.run(data, horizon=111111, nComm=[4, 8]).get_result())
            print (clustering.load_result(data.name, alg.name))

    def test_LinkCommunities(self):
        for data in  self.graphs: 
            alg = LinkCommunities()
            print(sys._getframe().f_code.co_name)
            print (alg.run(data, threshold=[0.01, 0.05]).get_result())
            print (clustering.load_result(data.name, alg.name))

    def test_TopGC(self):
        for data in  self.graphs: 
            alg = TopGC()
            print(sys._getframe().f_code.co_name)
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))            

    def test_GCEGC(self):
        for data in  self.graphs: 
            alg = GCE()
            print(sys._getframe().f_code.co_name, data.name)
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))

    def test_MOSES(self):
        for data in  self.graphs: 
            alg = MOSES()
            print(sys._getframe().f_code.co_name, data.name)
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))    
            
    def test_ParCPM(self):
        for data in  self.graphs: 
            alg = ParCPM()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))                             


    def test_DEMON(self):
        for data in  self.graphs: 
            alg = DEMON()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))                             

    def test_HDEMON(self):
        for data in  self.graphs: 
            alg = HDEMON()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            if data.is_directed():
                with self.assertRaises(Exception):                
                    print (alg.run(data).get_result())
            else:
                print (alg.run(data).get_result())
                print (clustering.load_result(data.name, alg.name))                             

    def test_FastCpm(self):
        for data in  self.graphs: 
            alg = FastCpm()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data).get_result())
            print (clustering.load_result(data.name, alg.name))                             

    def test_MSCD_RB(self):
        for data in  self.graphs: 
            alg = MSCD_RB()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data,scale_param="[1.2,2]").get_result())
            print (clustering.load_result(data.name, alg.name))                             

    def test_MSCD_AFG(self):
        for data in  self.graphs: 
            alg = MSCD_AFG()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data,scale_param="[1.2,2]").get_result())
            print (clustering.load_result(data.name, alg.name))    

    def test_MSCD_HSLSW(self):
        for data in  self.graphs: 
            alg = MSCD_HSLSW()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data,scale_param="[1.2,2]").get_result())
            print (clustering.load_result(data.name, alg.name))    

    def test_MSCD_LFK(self):
        for data in  self.graphs: 
            alg = MSCD_LFK()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data,scale_param="[1.2,2]").get_result())
            print (clustering.load_result(data.name, alg.name))   

    def test_MSCD_LFK2(self):
        for data in  self.graphs: 
            alg = MSCD_LFK2()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data,scale_param="[1.2,2]").get_result())
            print (clustering.load_result(data.name, alg.name))   

    def test_MSCD_RN(self):
        for data in  self.graphs: 
            alg = MSCD_RN()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data,scale_param="[1.2,2]").get_result())
            print (clustering.load_result(data.name, alg.name))   

    def test_MSCD_SO(self):
        for data in  self.graphs: 
            alg = MSCD_SO()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data,scale_param="[1.2,2]").get_result())
            print (clustering.load_result(data.name, alg.name))   

    def test_MSCD_SOM(self):
        for data in  self.graphs: 
            alg = MSCD_SOM()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data,scale_param="[1.2,2]").get_result())
            print (clustering.load_result(data.name, alg.name))   

    def test_SVINET(self):
        for data in  self.graphs: 
            alg = SVINET()
            print("Testing", sys._getframe().f_code.co_name, data.name)
            print (alg.run(data ).get_result())
            print (clustering.load_result(data.name, alg.name))   

    def test_AAA(self):

        a = [
            [0, 1, 1],
            [0, 2, 1],
            [1, 2, 1],
            
            [3, 4, 1],
            [3, 5, 1],
            [4, 5, 1],
            
            [6, 7, 1],
            [7, 8, 1],
            [6, 8, 1],
        ]
        
        for i in [0, 1, 2]:
            for j in [3, 4, 5]:
                a.append([i, j, 0.000001])        
        a.append([6, 4, 0.000001])        
        
        name=sys._getframe().f_code.co_name
        data = create_dataset(name=name, edgesObj=a,  directed=False, weighted=True, overide=True)
        alg = SVINET()
        print("Testing", sys._getframe().f_code.co_name, data.name)
        print (alg.run(data, max_iterations=1000).get_result())
        print (clustering.load_result(data.name, alg.name))
                                        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testClauset_Newman_Moore']
    unittest.main()
