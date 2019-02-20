import random


class Chromosome(object):
    def __init__(self, genes):
        self._genes = genes

    def mutate(self, chromosome):
        gene_list = chromosome.split(' ')
        idx = random.choice(range(len(gene_list)))
        gene_list[idx] = self._genes[idx].mutate(gene_list[idx])
        return ' '.join(gene_list)

    def random_chromosome(self):
        return ' '.join([gene.random_gene() for gene in self._genes])

    def parameters(self, chromosome):
        gene_list = chromosome.split(' ')
        return [gene.transform(_gene) for gene, _gene in zip(self._genes, gene_list)]


class ErrorCatchChromosome(Chromosome):
    """
    Temporary Chromosome alternative to catch RunTimeWarning raised by calling the fitness function. Respective operator
    will be reiterated until the RunTimeWarning ceases. TODO (*): Raise this to the EvolutionaryStrategy level.
    """

    def __init__(self, genes, fitness_function):
        super().__init__(genes)
        self._fitness_function = fitness_function

    def random_chromosome(self):
        _random = Chromosome.random_chromosome(self)
        while True:
            try:
                self._fitness_function(*Chromosome.parameters(self, _random))
                break
            except RuntimeWarning:
                _random = Chromosome.random_chromosome(self)
        return _random

    def mutate(self, chromosome):
        _mutated = Chromosome.mutate(self, chromosome)
        while True:
            try:
                self._fitness_function(*Chromosome.parameters(self, _mutated))
                break
            except RuntimeWarning:
                _mutated = Chromosome.mutate(self, chromosome)
        return _mutated
