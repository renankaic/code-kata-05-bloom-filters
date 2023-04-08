import math

class BloomFilter():
    def __init__(self, num_of_itens: int, false_pos_prob: float):
        """
        Instantiates a Bloom Filter by using Mumur 3 (mmh3) library to calculate hashes

        Parameters:
        num_of_itens (int): Number of itens that may be stored in the filter
        false_pos_prob (float): A decimal representating the false positive probability
            The lower the number, the bigger the filter will be

        Attributes:
        num_of_itens (int): Number of itens that may be stored in the filter
        false_pos_prob (float): A decimal representing the false positive probability.
        size (int): The size of the bloom filter based on the number of items and false positive probability.
        hash_count (int): The number of hash functions to be used.
        """
        
        self.num_of_itens = num_of_itens
        self.false_pos_prob = false_pos_prob
        self.size = self._calculate_size(num_of_itens, false_pos_prob)
        self.hash_count = self._calculate_hash_functions_count(
            self.size, num_of_itens)

    @classmethod
    def _calculate_size(cls, num_of_itens: int, false_pos_prob: float):
        m = -((num_of_itens * math.log(false_pos_prob)) / (math.log(2) ** 2))
        return int(m)
    
    @classmethod
    def _calculate_hash_functions_count(cls, m: int, n: int) -> int:
        """
        Calculates the optimal Hash Function count to be used in bloom filter.

        Parameters:
        m (int): Size of bloom filter
        n (int): Number of itens that may be inserted

        Returns:
        int: Number of optimal count of hash functions
        """
        k = ( m / n ) * math.log(2)
        return int(k)