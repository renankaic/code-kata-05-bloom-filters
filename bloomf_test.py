from bloom_filter import BloomFilter
from random import shuffle

n = 20 #no of items to add
p = 0.5 # false positive probability

bloomf = BloomFilter(items_count=n, fp_prob=p)
print(f"Size of bit array: {bloomf.size}")
print(f"False positive probability: {bloomf.fp_prob}")
print(f"Number of hash functions: {bloomf.hash_count}")

# Words to be added
word_present = ['abound','abounds','abundance','abundant','accessible',
                'bloom','blossom','bolster','bonny','bonus','bonuses',
                'coherent','cohesive','colorful','comely','comfort',
                'gems','generosity','generous','generously','genial']

# word not added
word_absent = ['bluff','cheater','hate','war','humanity',
               'racism','hurt','nuke','gloomy','facebook',
               'geeksforgeeks','twitter']

print(f"No of words present: {len(word_present)}")

for item in word_present:
    bloomf.add(item)

shuffle(word_present)
shuffle(word_absent)

test_words = word_present[:10] + word_absent
shuffle(test_words)
for word in test_words:
    if bloomf.check(word):
        if word in word_absent:
            print(f"'{word}' is a false positive")
        else:
            print(f"'{word}' is probably present")
    else:
        print(f"'{word}' is definitely not present")
