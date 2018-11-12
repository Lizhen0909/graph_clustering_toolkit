'''
Created on Nov 11, 2018

@author:  Lizhen Shi
'''

class UnsupportedException(Exception):
    def __init__(self,reason):
        super(UnsupportedException, self).__init__(reason)
