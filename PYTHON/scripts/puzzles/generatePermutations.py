# find all words that are permuted substrings

"""
I am addicted to a game called Wordscapes. It involves solving for all
the words in a crossword that are permutations of a six letters.

Every so often I get stuck. So I wrote a Python script to cheat.

See attached

try: python generate2.py mousetrap 4
"""

import sys

allEnglishWords = dict( (w.strip(), 1) for w in open('wordsEn.txt'))
minLength = 3

S = sorted(sys.argv[1])

if len(sys.argv) > 2:
    minLength = int(sys.argv[2])

found = {}

def permute(S, stringSoFar, indx, n):

    if n == 0:
        if stringSoFar in allEnglishWords and stringSoFar not in found:
            found[stringSoFar] = 1
            yield stringSoFar
        return

    elif indx + n > len(S):
        return
    
    #choose S[indx]: add letter to stringSoFar in different positions, reduce n
    for i in range(len(stringSoFar)+1):
        for word in permute(S, stringSoFar[:i] + S[indx] + stringSoFar[i:], indx+1, n-1):
            yield word

    #skip this letter: leave stringSoFar alone, leave n alone
    for word in permute(S, stringSoFar, indx+1, n):
        yield word


for i in range(minLength, len(S)+1):
    for word in permute(S, '', 0, i):
        print(word)
