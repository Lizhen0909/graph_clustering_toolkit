'''
Created on Apr 6, 2018

@author: lizhen
'''
import os, time
from . import utils


class Task(object):

    def __init__(self, name, fun, task_path):
        self.name = name 
        self.fun = fun
        self.status_file = os.path.join(task_path, self.name + ".done")
        self.logger = utils.get_logger (self.name)
    
    def done(self):
        return os.path.exists(self.status_file)
    
    def __call__(self):
        if self.done():
            self.logger.info("Task %s is in done status. Skip.", self.name)
        else:
            t0 = time.time()
            self.logger.info("start %s", self.name)
            self.fun(self.logger)
            utils.touch(self.status_file)
            t1 = time.time()
            self.logger.info("finish %s, Total Time: %s", self.name, str(t1 - t0))
            
