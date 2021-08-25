# find the longest words where the consonants are in alphabetical order

import re

words =  (x.strip() for x in open('wordsEn.txt'))

def stripVowels(w):

    return re.sub(r'[aeiou]', '', w)


def isValid(w):

    if len(w) <= 1:
        return False
    
    mark = ord(w[0])

    for ch in w[1:]:
        if ord(ch) != mark+1:
            return False
        else:
            mark += 1

    return True


maxLen=0
maxWord = []
for word in words:

    w = stripVowels(word)

    if isValid(w):
        print word

        if len(word) > maxLen:
            maxLen = len(word)
            maxWord = [word]
        elif len(word) == maxLen:
            maxWord.append(word)

print
for w in maxWord:
    print w
