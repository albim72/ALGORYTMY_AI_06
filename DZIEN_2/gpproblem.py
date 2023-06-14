import operator
import math
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


def protectedDiv(left,right):
    try:
        return left/right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN",1)
pset.addPrimitive(operator.add,2)
pset.addPrimitive(operator.sub,2)
pset.addPrimitive(operator.mul,2)
pset.addPrimitive(protectedDiv,2)
pset.addPrimitive(operator.neg,1)
pset.addPrimitive(math.cos,1)
pset.addPrimitive(math.sin,1)
pset.addEphemeralConstant("rand101",lambda:random.randint(-1,1))
pset.renameArguments(ARG0='x')

creator.create("FitnessMin",base.Fitness, weights=(-1.0,))
creator.create("Individual",gp.PrimitiveTree,fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr",gp.genHalfAndHalf,pset=pset,min_=-1,max_=2)
toolbox.register("individual",tools.initIterate, creator.Individual,toolbox.expr)
toolbox.register("population",tools.initRepeat,list,toolbox.individual)
toolbox.register("compile",gp.compile, pset=pset)
