import argparse
from spell_checker import SpellChecker

"""
This program is a spell checker that uses a Bloom filter. It takes as input a wordlist file and 
an optional false positive probability. It outputs a list of misspelled words.
"""

parser = argparse.ArgumentParser()
parser.add_argument("-wl", "--wordlist", dest="wordlist_file", 
                    help="Name or absolute Path to wordlist file", required=False)
parser.add_argument("-fp","--false_pos_prob", type=float, dest="false_pos_prob",
                    help="False positive probability", required=False)

args = parser.parse_args()

wordlist_file = args.wordlist_file
false_pos_prob = args.false_pos_prob
try:
    spell_chk = SpellChecker(wordlist_file=wordlist_file, fp_prob=false_pos_prob)
    spell_chk.start_sc()
except FileNotFoundError:
    print(f"Error: could not find file '{wordlist_file}'. Please check the filename or path and try again")
except ValueError:
    print(f"Error: The false positive probability should be a decimal number between 0 and 1.")
    print(f"Example usage: python main.py -wl wordlist.txt -fp 0.05")