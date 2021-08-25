coins = [1, 5, 10, 25]


def C(P):

    if P == 0: return 0
    if P in coins: return 1
 
    return min(C(P-v) for v in coins if P >= v) + 1

memory = dict()
memory[0] = 0
for k in coins: memory[k] = 1

def C2(P):

    if P in memory: return memory[P]
 
    f = min(C2(P-v) for v in coins if P >= v) + 1
    memory[P] = f
    return f

K = 100

for i in range(K):
    print i, C2(i)

print 
print
"""
for i in range(K):
    print i, C(i)
"""
