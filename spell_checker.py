from spell_checker_bf import BloomFilter
from typing import List


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

                if self.check(word_to_check):
                    print(
                        f"The word '{word_to_check}' probably exist in the dictionary!\n")
                else:
                    print(
                        f"The word '{word_to_check}' probably DOES NOT exist in the dictionary!\n")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    def check(self, word: str) -> bool:
        """
        Checks whether `word` probably exists in the loaded word list.

        Parameters:
        word (str): String containing the word to be checked

        Return:
        bool: True if probably exists, or False when definitely doesn't exist
        """
        return self._bloom_filter.check(word)

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
