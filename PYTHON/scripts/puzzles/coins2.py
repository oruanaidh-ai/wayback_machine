coins = [1, 5, 10, 25]


def C(P):

    if P == 0: return 0
    if P in coins: return 1
 
    return min(C(P-v) for v in coins if P >= v) + 1

memory = dict()
memory[0] = 0, []
for k in coins: memory[k] = (1, [k,])

def C2(P, v):

    if P in memory: return memory[P]
 
    ff = 1e6
    cc = None
    for c in coins:  
        if c > P: continue
        f, ww = C2(P-c, v)
        if len(ww) < ff:
            ff = len(ww)
            cc = c
            vv = v + ww
    if cc: vv.append(cc)
    memory[P] = (len(vv), vv)
    
    return memory[P]

K = 40

for i in range(1001):
    print i, C2(i, [])

print 
print
"""
for i in range(K):
    print i, C(i)
"""
