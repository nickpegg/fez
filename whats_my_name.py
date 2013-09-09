#!/usr/bin/env python3

# Attempts at solving the floating stone puzzle
# My notes at the end of this script outline the puzzle and my thought process

import multiprocessing
import string

from itertools import permutations
from functools import partial


# List of lists to hold the blocks
# I've numbered the blocks 0 - 8 left-to-right when viewing them 
# when you're also seeing the door. Each sublist are the letters
# on the four sides of the block.
# Some block have >4 letters since two symbols share letters (U/V, K/Q)
blocks = [
    'gmsa',
    'tnhb',
    'zkqex',
    'msag',
    'tnhb',
    'uvoic',
    'nhbt',
    'rlfy',
]


def main():
    pool = multiprocessing.Pool(8)

    # Get a list of words from the dictionary and massage it a bit
    dictfile = open('dict')
    dictwords = map(lambda s: s.strip(), dictfile)  # Get rid of newlines
    dictwords = map(lambda s: s.lower(), dictwords) # Make everything lowercase
    dictwords = set(dictwords)                      # Get rid of duplicates

    eight_letter_dictwords = [w for w in dictwords if len(w) == 8]
    four_letter_dictwords = [w for w in dictwords if len(w) == 4]

    block_permutations = permutations(blocks)

    motw = partial(made_of_two_words, four_letter_dictwords)
    words = pool_filter(pool, motw, eight_letter_dictwords)
    print("Found {0} words that are made of two 4-letter words".format(len(words)))

    wip = partial(word_in_permutation, list(block_permutations))
    words = pool_filter(pool, wip, words)
        
    print("Found {0} words that can be made with our blocks".format(len(words)))

    # Dump that shit to a file!
    outfile = open("whats_my_name.output.txt", 'w')
    for word in words:
        outfile.write(word + "\n")
    outfile.close()



def pool_filter(pool, func, stuff):
    return [c for c, keep in zip(stuff, pool.map(func, stuff)) if keep]


def made_of_two_words(dictwords, word):
    return word[:4] in dictwords and word[4:] in dictwords


def word_in_permutation(perms, word):
    for permutation in perms:
        good = True
        for char, block in zip(word, permutation):
            #print((char, block))
            if char not in block:
                good = False
                break
        if good:
            break

    return good


if __name__ == '__main__':
    main()


"""
# Nick's Notes

## Premise

There is a stone floating in the air with some writing on it. 

    PLEASE ANSWER 
    THIS SECURITY
    QUESTION
    WHATS MY NAME

    SECURITY
    QUESTION HINT
    MY FIRST HALF
    IS WHAT IT IS
    MY SECOND HALF
    IS HALF OF
    WHAT MADE IT

On the ground, there are eight blocks with letter symbols on them. 
Unfortunately, on the four sides of each block is a rotation of that letter 
symbol, which makes each block actually four different letters.

Based on the hint, we can assume the word is a name and is made of two
four-letter words. This should be fairly simple to brute-force with a 
dictionary; we just need to filter the dictionary down first.


## Though Process

I started this by getting all of the block permutations and then getting all 
words that you could make with those permutations (used a Cartesian product).
I then filtered those words, first by existance in the dictionary of 8-leter
words, and then by which words were made of two 4-letter words (assuming that
was a safe assumption by the 'security hint').

This was a bad idea. There are 40320 permutations, and taking the Cartesian
product of each permutation yielded roughly 2^16 words, which would be 
roughly 40320 * (2 ^ 16) words to sift through. Even with multiprocessing it 
took my computer about 5 minutes to get the wrong answer.

I did some thinking and figured it would be faster to start with a 
filtered-down dictionary, first by filtering down to only 8-letter words and 
then filtering down to words made of two 4-letter words. This yields only 3933
words which we need to check against the 40320 permutations. Even with that,
we don't have to check _every_ block in the permutation since if the first 
letter of the word can't be made with the first block, it's trash.

The function word_in_permutation() is the meat of this algorithm. Basically, 
if a word canbe made with one of the permutations, it's a candidate.

Filtering using this method yielded only 38 words! There's a lot of names, 
so a lot of thinking will have to be done to match them up with the hint.


## Post-Mortem

I used a lot of functional things here (especially partial function evaluation,
which is kind of ugly in Python). I should have written this in Haskell. 

You know, I just might do that. :)

"""