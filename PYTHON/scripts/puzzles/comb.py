# generate combinations
def comb(N, k):

    if k==0:
        yield []
    elif N==k:
        yield range(1, k+1)   # 1, 2, 3, 4 ... k
    else:
        for x in comb(N-1, k):
            yield x
        for x in comb(N-1, k-1):
            yield x + [N]


