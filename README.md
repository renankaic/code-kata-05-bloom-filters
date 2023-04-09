# Bloom Filter Spell Checker

This is a simple spell checker that uses a Bloom filter to check if words are spelled correctly.

## Usage

To use the spell checker, you need to have a wordlist file containing a list of correctly spelled words, one word per line. You can use the wordlist.txt file included in this repository as an example.

To run the spell checker, use the following command:
```
python main.py -wl <wordlist_file> -fp <false_pos_prob>
```

where `<wordlist_file>` is the name or absolute path to your wordlist file, and `<false_pos_prob>` is the desired false positive probability (a decimal number between 0 and 1). 

For example:

```
python main.py -wl wordlist.txt -fp 0.05
```

The program will start a CLI where you can type a word and it will return the probably of its existence in the dictionary.

## Installation
To install the required packages, run inside a virtual environment:

```
pip install -r requirements.txt
```

## Implementation
The spell checker is implemented in Python and uses a Bloom filter to efficiently check if words are spelled correctly. 

A Bloom filter is a probabilistic data structure that allows efficient membership tests, but may give false positives (i.e., report that a word is spelled correctly when it's not) with a certain probability.

The program reads in the wordlist file and creates a Bloom filter with the desired false positive probability. It then reads in a list of words to check and uses the Bloom filter to check if each word is likely to be spelled correctly.

## Acknowledgments
This project was inspired by the [CodeKata 5](http://codekata.com/kata/kata05-bloom-filters/) from Dave Thomas' CodeKata series.

## License
This project is licensed under the MIT License, which is a permissive free software license that allows you to use, copy, modify, and distribute the software with few restrictions. This means that you are free to use the code in your own projects, modify it to suit your needs, and distribute it to others. 