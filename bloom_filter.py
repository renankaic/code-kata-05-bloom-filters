import math
import mmh3
from bitarray import bitarray

class BloomFilter(object):
    """
    Class for Bloom filter, using mumur3 hash function
    """

    def __init__(self, items_count: int, fp_prob: float) -> None:

        #False positive probability
        self.fp_prob = fp_prob

        # Size of bit array to use
        self.size = self.get_size(items_count, fp_prob)

        # Number of hash functions to use
        self.hash_count = self.get_hash_count(self.size, items_count)
        
        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # Initialize bit array with all bits as 0
        self.bit_array.setall(0)
    
    def add(self, item):
        """
        Add an item in the filter
        """
        digests = []
        for i in range(self.hash_count):
            # create digest for given item
            # i work as seed to mmh3.hash() function
            # with different seed, digest created is different
            digest = mmh3.hash(item, i) % self.size
            #digests.append(digest)

            # set the bit True in bit_array
            self.bit_array[digest] = True
    
    def check(self, item):
        """
        Checks for existence of an item in the filter
        """
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:
                # if any of the bit is False, then its not present in the filter
                # else there is probability that it exist
                return False
        return True

    @classmethod
    def get_size(cls, items_count: int, fp_prob: float):
        m = -(items_count * math.log(fp_prob)) 
        m = m / (math.log(2) ** 2)
        return int(m)
    
    @classmethod
    def get_hash_count(cls, size_of_bitarray: int, items_no: int):
        k = (size_of_bitarray/items_no) * math.log(2)
        return int(k)

    