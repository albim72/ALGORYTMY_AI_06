import random

import numpy
import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax",base.Fitness,weights=(1.0,))
creator.create("Individual",np.ndarray,fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool",random.randint,0,1)
toolbox.register("individual",tools.initRepeat,creator.Individual,toolbox.attr_bool,n=100)
toolbox.register("population",tools.initRepeat,list,toolbox.individual)

def evalOneMax(individual):
    return sum(individual)

def cxTwoPointCopy(ind1,ind2):
    size = len(ind1)
    cxpoint1 = random.randint(1,size)
    cxpoint2 = random.randint(1,size-1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:
        cxpoint1,cxpoint2 = cxpoint2,cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind1[cxpoint1:cxpoint2].copy(), ind2[cxpoint1:cxpoint2].copy()

    return ind1,ind2

toolbox.register("evaluate",evalOneMax)
toolbox.register("mate",cxTwoPointCopy)
toolbox.register("mutate",tools.mutFlipBit,indpb = 0.05)
toolbox.register("select",tools.selTournament, tournsize=3)

def main():
    random.seed(64)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1,similar=np.array_equal)
    stats = tools.Statistics(lambda ind:ind.fitness.values)

    stats.register("avg",np.mean)
    stats.register("std",np.std)
    stats.register("min",np.min)
    stats.register("max",np.max)

    algorithms.eaSimple(pop,toolbox,cxpb=0.5,mutpb=0.2,ngen=40,stats=stats,halloffame=hof)

    return pop,stats,hof

if __name__ == '__main__':
    main()
