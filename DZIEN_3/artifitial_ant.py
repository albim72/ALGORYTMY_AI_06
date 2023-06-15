import copy
import random

import numpy

from functools import partial

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

def progn(*args):
    for arg in args():
        arg()

def prog2(out1,out2):
    return partial(progn,out1,out2)

def prog3(out1,out2,out3):
    return partial(progn,out1,out2,out3)

def if_then_else(condition,out1,out2):
    out1() if condition() else out2()

class AntSimulator(object):
    direction = ["north","east","south","west"]
    dir_row = [1,0,-1,0]
    dir_col = [0,1,0,-1]
    
    def __init__(self,max_moves):
        self.max_moves=max_moves
        self.moves=0
        self.eaten=0
        self.routine=None
        
    def _reset(self):
        self.row = self.row_start
        self.col = self.col_start
        self.dir=1
        self.moves=0
        self.eaten=0
        self.matrix_exc = copy.deepcopy(self.matrix)
        
    @property
    def position(self):
        return (self.row,self.col,self.direction[self.dir])
    
    
