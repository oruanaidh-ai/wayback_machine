

def permutation(w):
    if len(w) == 1: yield w[0]

    for c, a in enumerate(w):
        for x in permutation(w[:c] + w[c+1:]):
            yield a + x


for k in permutation('abcde'):
    print k
        


