import random
import numpy as np
import math
from operators import *


class _BaseGene(object):
    """

    """

    @staticmethod
    def mutate(_gene):
        """
        :param _gene:
        :return:
        """
        binary_list = list(_gene)
        idx = random.choice(range(len(_gene)))
        binary_list[idx] = '0' if binary_list[idx] is '1' else '1'
        return ''.join(binary_list)

    @staticmethod
    def random_gene():
        """

        :return:
        """
        raise NotImplemented("random() Not implemented in _BaseGene")

    def __repr__(self):
        return type(self).__name__ + "(" + "val=" + str(self.value) + ", " + "gene=" + str(self) + ")"

    def __str__(self):
        return str()

    def transform(self, _gene):
        return _gene

    @property
    def value(self):
        return self.transform(_gene=self._gene)


class BinaryGene(_BaseGene):
    """
    Single boolean
    """

    @staticmethod
    def random_gene():
        return str(random.randint(0, 1))


class BitarrayGene(_BaseGene):
    """
    Sequence of booleans
    """

    def __init__(self, n_bits):
        self._n_bits = n_bits

    def random_gene(self):
        return ''.join([random.choice(['0', '1']) for _ in range(self._n_bits)])


class DenaryGeneFloat(_BaseGene):

    def __init__(self, limits=(None, None), n_bits_exponent=4, n_bits_fraction=4, signed=False):
        self.limits = limits
        self._n_bits_exponent = n_bits_exponent
        self._n_bits_fraction = n_bits_fraction
        self._n_bits = n_bits_exponent + n_bits_fraction if n_bits_fraction else n_bits_exponent
        self._n_bits += 1 if signed else 0
        self._signed = signed

    def random_gene(self):
        _random = ''.join([random.choice(['0', '1']) for _ in range(self._n_bits)])
        if self.limits[0] is not None and self.limits[1] is not None:
            while not (self.limits[0] <= self.transform(_random) <= self.limits[1]):
                _random = ''.join([random.choice(['0', '1']) for _ in range(self._n_bits)])

        elif self.limits[1] is not None and self.limits[0] is None:
            while not self.transform(_random) <= self.limits[1]:
                _random = ''.join([random.choice(['0', '1']) for _ in range(self._n_bits)])

        elif self.limits[0] is not None and self.limits[1] is None:
            while not self.transform(_random) >= self.limits[0]:
                _random = ''.join([random.choice(['0', '1']) for _ in range(self._n_bits)])
        else:
            _random = ''.join([random.choice(['0', '1']) for _ in range(self._n_bits)])
        return _random

    def transform(self, _gene):
        exp_idx = 0
        sign = 1
        if self._signed:
            if _gene[0] is "0":
                pass
            else:
                sign = -1
            exp_idx = 1
        exp = 0
        for idx, bit in enumerate(_gene[exp_idx:exp_idx + self._n_bits_exponent]):
            if bit is "0":
                pass
            else:
                exp += 2 ** idx
        frac = 0
        if self._n_bits_fraction is None:
            pass
        else:
            for idx, bit in enumerate(
                    _gene[-self._n_bits_fraction:]):
                if bit is "0":
                    pass
                else:
                    frac += 2 ** -(idx + 1)
        return sign * (exp + frac)

    # Inherited mutate member function must be over-written for linear boundaries.
    def mutate(self, _gene):
        """
        :param _gene:
        :return:
        """
        mutated = _BaseGene.mutate(_gene)
        if self.limits[1] and self.limits[0]:
            while not (self.limits[0] <= self.transform(mutated) <= self.limits[1]):
                mutated = _BaseGene.mutate(_gene)

        elif self.limits[1] and not self.limits[0]:
            while not self.transform(mutated) <= self.limits[1]:
                mutated = _BaseGene.mutate(_gene)

        elif self.limits[0] and not self.limits[1]:
            while not self.transform(mutated) >= self.limits[0]:
                mutated = _BaseGene.mutate(_gene)
        else:
            return _BaseGene.mutate(_gene)
        return mutated


class LinearRangeGene(_BaseGene):
    """
    -32,767 to 32,767
    """

    def __init__(self, start, stop, num, endpoint=True, retstep=False, dtype=None):
        """
        :param start: Lower bound for search
        :param stop: Upper bound for search
        :param a_res: Minimum absolute resolution required
        :param endpoint:
        :param retstep:
        :param dtype:
        """
        self._num = num
        self._linear_space = np.linspace(start, stop, num=self._num, endpoint=endpoint, retstep=retstep,
                                         dtype=dtype)
        self._lower_bound = start
        self._upper_bound = stop

    # Inherited mutate member function must be over-written for linear boundaries.
    def mutate(self, _gene):
        """
        :param _gene:
        :return:
        """
        mutated = _BaseGene.mutate(_gene)
        while True:
            try:
                self.transform(mutated)
            except IndexError:
                mutated = _BaseGene.mutate(_gene)
            else:
                break
        return mutated

    def random_gene(self):
        _format = '{' + '0:0{}b'.format(len(bin(self._num)[2:])) + '}'
        return _format.format(random.randint(0, self._num))

    def transform(self, _gene):
        return self._linear_space[int(_gene, 2) - 1]
