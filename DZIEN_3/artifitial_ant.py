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

    def turn_left(self):
        if self.moves < self.max_moves:
            self.moves += 1
            self.dir = (self.dir-1)%4

    def turn_right(self):
        if self.moves < self.max_moves:
            self.moves += 1
            self.dir = (self.dir+1)%4

    def move_forward(self):
        if self.moves < self.max_moves:
            self.moves += 1
            self.row = (self.row+self.dir_row[self.dir])%self.matrix_row
            self.col = (self.col+self.dir_col[self.dir])%self.matrix_col
            if self.matrix_exc[self.row][self.col] == "food":
                self.eaten += 1
            self.matrix_exc[self.row][self.col]="passed"

    def sense_food(self):
        ahead_row = (self.row + self.dir_row[self.dir]) % self.matrix_row
        ahead_col = (self.col + self.dir_col[self.dir]) % self.matrix_col
        return self.matrix_exc[ahead_row][ahead_col] == "food"

    def if_food_ahead(self,out1,out2):
        return partial(if_then_else,self.sense_food,out1,out2)

    def run(self,routine):
        self._reset()
        while self.moves < self.max_moves:
            routine()

    def parse_matrix(self,matrix):
        self.matrix = list()
        for i, line in enumerate(matrix):
            self.matrix.append(list())
            for j, col in enumerate(line):
                if col == "#":
                    self.matrix[-1].append("food")
                elif col == ".":
                    self.matrix[-1].append("empty")
                elif col == "S":
                    self.matrix[-1].append("empty")
                    self.row_start = self.row = i
                    self.col_start = self.col = j
                    self.dir = 1
        self.matrix_row = len(self.matrix)
        self.matrix_col = len(self.matrix[0])
        self.matrix_exc = copy.deepcopy(self.matrix)

ant = AntSimulator(600)

pset = gp.PrimitiveSet("MAIN",0)
pset.addPrimitive(ant.if_food_ahead,2)
pset.addPrimitive(prog2,2)
pset.addPrimitive(prog3,3)
pset.addTerminal(ant.move_forward)
pset.addTerminal(ant.turn_left)
pset.addTerminal(ant.turn_right)


creator.create("FitnessMax",base.Fitness,weights=(1.0,))
creator.create("Individual",gp.PrimitiveTree,fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("expr_init",gp.genFull,pset=pset,min_=1,max_=2)

toolbox.register("individual",tools.initIterate,creator.Individual,toolbox.expr_init)
toolbox.register("population",tools.initRepeat,list,toolbox.individual)
def evalArtifitialAnt(individual):
    routine = gp.compile(individual,pset)
    ant.run(routine)
    return ant.eaten

toolbox.register("evaluate",evalArtifitialAnt)
toolbox.register("select",tools.selTournament,tournsize=7)
toolbox.register("mate",gp.cxOnePoint)
toolbox.register("expr_mut",gp.genFull,min_=0,max_=2)
toolbox.register("mutate",gp.mutUniform,expr=toolbox.expr_mut,pset=pset)

def main():
    random.seed(69)

    with open("santafe_trail.txt") as trail_file:
        ant.parse_matrix(trail_file)

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind:ind.fitness.values)
    stats.register("średnia arytmetyczna:",numpy.mean)
    stats.register("średnie odchylenie standardowe:",numpy.std)
    stats.register("minium:",numpy.min)
    stats.register("maximum:", numpy.max)

    algorithms.eaSimple(pop,toolbox,0.5,0.2,40,stats,halloffame=hof)
    return pop,hof,stats

if __name__ == '__main__':
    main()
