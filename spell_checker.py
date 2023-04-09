import math
import mmh3
from bitarray import bitarray
from typing import List

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
        bit_array (bitarray): The array of bits
        """
        
        self.num_of_itens = num_of_itens
        self.false_pos_prob = false_pos_prob
        self.size = self._calculate_size(
            self.num_of_itens, self.false_pos_prob)
        self.hash_count = self._calculate_hash_functions_count(
            self.size, self.num_of_itens)
        
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

    def check(self, item: str) -> bool:
        """
        Check whether the provided `item` string possibly exists in the bloom filter.
        This is done by hashing the 'item' using Mumur 3, 
        and verifying that all generated hashes exists in the Bloom Filter 'bit_array'
        
        Parameters:
        item (str): The string to be checked for existence in Bloom Filter

        Returns:
        bool: 
            - 'True' when the `item` possibly exists in the Bloom Filter (see `Notes`)
            - 'False' when it does not exist in the Bloom Filter

        Notes:
        It may return false positives based on the `self.false_pos_prob` value.
        (that is, saying that the item has probability to exist even when, in fact, it does not exist) 
        However, it will NEVER return a false negative
        (which means that if it indicates that an item doesn't exist, it really doesn't exist)
        """
        for i in range(self.hash_count):
            hsh = (mmh3.hash(item, i)) % self.size
            if self.bit_array[hsh] == False:
                return False
        return True

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
    
class SpellChecker():
    def __init__(self, wordlist_file: str = "wordlist.txt", fp_prob: float = 0.05) -> None:
        """
        Initializes an instance of a SpellChecker which checks the probably existence of a word
        in a word list loaded from a file

        It uses the Bloom Filter algorithm to perform the check

        Note:
        It may return false positives based on the `fp_prob` value
        (that is, saying that the word has probability to exist even when, in fact, it does not exist).
        The lesser the fp_prob, the lesser false positives will return but the more memory it will use.

        Parameters:
        wordlist_file (str): Name or the absolute path of the file to be opened and loaded as word list
        fp_prob (float): False positive probability to be used - The lesser the number, the lesser false positives. 
            However, the program will use more memory        
        """
        self._bloom_filter = self._create_bloom_filter_with_wordlist(
            self._create_word_list(wordlist_file), fp_prob)

    def start_sc(self):
        """
        Starts this Spell Checker previously configured in the terminal console.
        It will ask for a word to check its probably existence in the loaded word list.
        """
        while True:
            try:
                word_to_check = input(
                    "Type the word to check its existence or press CTRL+C to exit: ")

                if not word_to_check:
                    print("Please, type a word to check!")
                    continue

                if self._bloom_filter.check(word_to_check):
                    print(
                        f"The word '{word_to_check}' probably exist in the dictionary!\n")
                else:
                    print(
                        f"The word '{word_to_check}' probably DOES NOT exist in the dictionary!\n")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    @classmethod
    def _create_word_list(cls, wordlist_file: str) -> List[str]:
        """
        This function return a list of raw strings obtained for each line in a file

        Parameters:
        wordlist_file (str): The name or absolute path of the file containing a words list

        Returns:
        List[str]: List of words obtained from the file
        """
        with open(wordlist_file, "r") as words_file:
            return [w.replace("\n", "") for w in words_file.readlines()]
    
    @classmethod
    def _create_bloom_filter_with_wordlist(cls, wordlist: List[str], fp_prob: float) -> BloomFilter:
        """
        Creates and return an instance of BloomFilter class containing a word list loaded into it.
        
        Parameters:
        wordlist (List[str]): List of words in string
        fp_prob (float): False positive probability

        Returns:
        BloomFilter: An instance of BloomFilter class loaded with the provided wordlist
        """
        bloomF = BloomFilter(num_of_itens=len(
            wordlist), false_pos_prob=fp_prob)
        
        for w in wordlist:
            bloomF.add(w)
        
        return bloomF
    
spell_chk = SpellChecker()
spell_chk.start_sc()