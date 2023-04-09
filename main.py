import argparse
from spell_checker import SpellChecker

parser = argparse.ArgumentParser()
parser.add_argument("-wl", "--wordlist", dest="wordlist_file", 
                    help="Name or absolute Path to wordlist file", required=False)
parser.add_argument("-fp","--false_pos_prob", type=float, dest="false_pos_prob",
                    help="False positive probability", required=False)

args = parser.parse_args()

wordlist_file = args.wordlist_file
false_pos_prob = args.false_pos_prob

spell_chk = SpellChecker(wordlist_file=wordlist_file, fp_prob=false_pos_prob)
spell_chk.start_sc()