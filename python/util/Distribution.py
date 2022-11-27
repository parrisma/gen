import numpy as np


class Distribution:

    @classmethod
    def random_distribution(cls,
                            n: int) -> np.ndarray:
        """
        Create a random probability distribution
        :param n: the number of elements in teh distribution
        :return: A probability distribution of length n
        """
        rd = np.random.random_sample((n,))
        return rd / np.sum(rd)
