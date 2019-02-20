from chromosome import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import figure
import numpy as np


class Population(object):

    def __init__(self, m: int, n: int, chromosome_class: Chromosome):
        self._m = m
        self._n = n
        self._chromosome = chromosome_class
        self._population = [self._chromosome.random_chromosome() for _ in range(m)]

    def fitness(self, fitness_function, *args):
        return [fitness_function(*self._chromosome.parameters(member), *args) for member in self._population]

    def crossover(self, crossover_function, *args):
        children_population = Population(self.m, self.n, self._chromosome)
        children_population.contestants = crossover_function(self._population, self.n, *args)
        return children_population

    def mutate(self, rate=0.001):
        for idx, individual in enumerate(self._population):
            self._population[idx] = self._chromosome.mutate(individual) if random.uniform(0, 1) <= rate else \
                self._population[idx]

    # def selection_function(m, contestants, fitness, *args):

    def selection(self, selection_function, fitness_function, *args):
        return selection_function(self.m, self.contestants, self.fitness(fitness_function), *args)

    @property
    def m(self):
        return self._m

    @property
    def n(self):
        return self._n

    @property
    def contestants(self):
        return self._population

    @contestants.setter
    def contestants(self, x):
        self._population = x

