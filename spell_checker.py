import math
from mmh3 import mmh3
from bitarray import bitarray

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
        
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add(self, item: str):
        """
        'Adds' an item to the Bloom Filter by generating `self.hash_counts` hashed numbers
        from the `item` content and setting the respective index of the `bit_array` as 1
        This process uses multiple independent hash functions to increase the accuracy of the Bloom filter 
        and reduce the chance of false positives.

        Parameters:
        item (str): String to be hashed and "added" to the Bloom filter
        """
        for i in range(self.hash_count):
            hsh = mmh3.hash(item, i) % self.size
            self.bit_array[hsh] = True

    @classmethod
    def _calculate_size(cls, n: int, p: float):
        """
        Calculates the size of bloom filter based on number of items and the desired false positive probability

        Parameters:
        - n (int): The number of items that may be stored in the filter.
        - p (float): A decimal representing the desired false positive probability

        Returns:
        - int: The size of the Bloom filter, calculated based on the number of items and false positive probability

        Note:
        A Bloom filter is a probabilistic data structure that uses multiple hash functions
        to represent a set of items. It can return false positives, meaning that it may indicate
        that an item is in the set when it is not, but it will NEVER return false negatives 
        (meaning that it will never indicate that an item is not in the set when it is)

        The false positive probability `p` is the probability that a Bloom filter will indicate
        a false positive for an item that is not in the set. The size of the Bloom filter `m` is
        determined by the number of itens `n` and the false positive probability `p`, and
        it affects the probability of false positives and the memory usage of the Bloom filter.
        """
        m = -((n * math.log(p)) / (math.log(2) ** 2))
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