import numpy as np
import operator


# TODO: Make Mutation Operator.

class TerminationCriteria:

    @staticmethod
    def _convergence_check(convergence_ratio, population_fitness):
        if abs((np.max(population_fitness) - np.mean(population_fitness)) / np.mean(
                population_fitness)) <= convergence_ratio / 2:
            return True
        else:
            return False

    @staticmethod
    def _fitness_level_check(fitness_level, population_fitness, _operator):
        ops = {'>': operator.gt,
               '<': operator.lt,
               '>=': operator.ge,
               '<=': operator.le,
               '=': operator.eq}
        inp = abs(np.max(population_fitness))
        relate = _operator
        cut = fitness_level
        return ops[relate](inp, cut)

    @staticmethod
    def _generations_check(generations, generation_limit):
        if generations >= generation_limit:
            return True
        else:
            return False

    def __init__(self):
        self._checks = []
        self._convergence_limit = None
        self._fitness_limit = None
        self._generation_limit = None
        self._operator = None

    def _checker_of_convergence(self):
        def _checker(population_fitness, generation_number):
            return self._convergence_check(self._convergence_limit, population_fitness)

        return _checker

    def _checker_of_fitness(self):
        def _checker(population_fitness, generation_number):
            return self._fitness_level_check(self._convergence_limit, population_fitness, self._operator)

        return _checker

    def _checker_of_generations(self):
        def _checker(population_fitness, generation_number):
            return self._generations_check(generation_number, self._generation_limit)

        return _checker

    def add_convergence_limit(self, convergence_ratio):
        self._checks.append(self._checker_of_convergence())
        self._convergence_limit = convergence_ratio

    def add_fitness_limit(self, operator, fitness_level):
        self._checks.append(self._checker_of_fitness())
        self._generation_limit = fitness_level
        self._operator = operator

    def add_generation_limit(self, generation_limit):
        self._checks.append(self._checker_of_generations())
        self._generation_limit = generation_limit

    def check(self, population_fitness, generation_number):
        if np.any([check(population_fitness, generation_number) for check in self._checks]) == True:
            return True
        else:
            return False


# def convergence_or_100(population_fitness, convergence_ratio):
#     if abs((np.max(population_fitness) - np.mean(population_fitness)) / np.mean(
#             population_fitness)) <= convergence_ratio / 2:
#         return True
#     elif abs(np.max(population_fitness)) == 100:
#         return True
#     else:
#         return False


class SelectionOperator:

    @staticmethod
    def supremacy(m, contestants, fitness):
        return list(np.array(contestants)[np.argpartition(np.array(fitness), -m)[-m:]])

    @staticmethod
    def random(m, contestants, fitness):
        # used = None
        # assert fitness is not used
        return list(np.random.choice(contestants, m))


class CrossoverOperator:

    @staticmethod
    def random_polygamous(parents, n_children):
        gene_lst = []
        child_ls = []
        for gene_idx in range(len(parents[0].split(' '))):
            gene_col = np.random.choice(np.array([parent.split(' ') for parent in parents])[:, gene_idx], n_children)
            gene_lst.append(gene_col)
        gene_arr = np.array(gene_lst).T
        for child_idx in range(len(gene_arr[:, 0])):
            child_new = ' '.join(list(gene_arr[child_idx, :]))
            child_ls.append(child_new)
        return child_ls

    @staticmethod
    def supremecy_polygamous(parents, n_children, fitness):
        raise NotImplemented("Supremacy not implemented yet")


def fitness_function_himmelblau(x, y):  # execute himmelblau function
    f = (x ** 2. + y - 11.) ** 2. + (x + y ** 2. - 7.) ** 2.
    return 100 - f
