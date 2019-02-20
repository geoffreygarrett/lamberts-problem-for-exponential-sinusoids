import numpy as np
import pandas as pd


class EvolutionaryStrategy(object):
    def __init__(self, population, fitness_function, crossover_function, selection_function,
                 termination_criteria, mutation_rate, colonize=False):
        """

        :param population:  asd asd asd
        :param fitness_function:
        :param crossover_function:
        :param selection_function:
        :param termination_criteria:
        :param mutation_rate:
        :param colonize:
        """
        self.population = population
        self.fitness_function = fitness_function
        self.crossover_function = crossover_function
        self.selection_function = selection_function
        self.termination_criteria = termination_criteria
        self.mutation_rate = mutation_rate
        self.generation_number = 0
        self.children = None

    def perform_crossover(self, population):
        """

        :param population:
        :return:
        """
        return population.crossover(self.crossover_function)

    def perform_mutation(self, population):
        population.mutate(self.mutation_rate)

    def perform_selection(self, population):
        population.contestants = population.selection(self.selection_function, self.fitness_function)

    def get_population_fitness(self):
        return self.population.fitness(self.fitness_function)

    def get_average_fitness(self):
        return float(np.mean(self.get_population_fitness()))

    def get_maximum_fitness(self):
        return np.max(self.get_population_fitness())

    def get_minimum_fitness(self):
        return np.min(self.get_population_fitness())

    def get_fittest_chromosome(self):
        return list(set(np.array(self.population.contestants)[
                            np.array(self.get_population_fitness()) == self.get_maximum_fitness()]))

    def get_fittest_solution(self):
        return list(set([tuple(self.population._chromosome.parameters(c)) for c in self.get_fittest_chromosome()]))

    def evolve(self, verbose=False, return_log=False):
        if return_log:
            log = []

        while self.termination_criteria(self.get_population_fitness(), self.generation_number) is False:
            self.children = self.perform_crossover(self.population)
            self.perform_mutation(self.children)
            self.population.contestants += self.children.contestants
            self.perform_selection(self.population)
            self.generation_number += 1
            if verbose:
                print("GEN: ",
                      str(self.generation_number).ljust(5),
                      "   ||   ",
                      "MAX_FIT: ",
                      str(np.round(self.get_maximum_fitness(), 4)).ljust(10),
                      "   ||   ",
                      "MIN_FIT: ",
                      str(np.round(self.get_minimum_fitness(), 4)).ljust(10),
                      "   ||   ",
                      "AVG_FIT: ",
                      str(np.round(self.get_average_fitness(), 4)).ljust(10),
                      "   ||   ",
                      "CHROMOSOME: ",
                      str(self.get_fittest_chromosome()).ljust(15),
                      "   ||   ",
                      "BEST_SOLN: ",
                      str(self.get_fittest_solution()),
                      ),
            if return_log:
                log.append([self.generation_number,
                            np.round(self.get_maximum_fitness(), 3),
                            np.round(self.get_minimum_fitness(), 3),
                            np.round(self.get_average_fitness(), 3),
                            self.get_fittest_chromosome()[0],
                            np.round(self.get_fittest_solution()[0], 3)])

        if verbose:
            print("\n" + "--" * 100 + "\n")

        if return_log:
            df = pd.DataFrame(log,
                              columns=
                              """Generation,Maximum Fitness,Minimum Fitness,Average Fitness,Chromosome,Best Solution""".split(
                                  ","))

            df = df.set_index("Generation")
            return df
