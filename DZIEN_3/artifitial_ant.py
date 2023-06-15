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
