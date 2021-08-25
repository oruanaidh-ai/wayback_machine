T = 15

I = {12:15, 2:2.1, 1:1, 0.5:0.4, 4:4.15}

def V(x):
    if x == 0: return 0

    maxV = 0
    for i, v in I.iteritems():
        if x >= i:
            f = v + V(x - i)
            if f > maxV:
                maxV = f
            
    return maxV

memory = dict()
memory[0] = 0
def V2(x):
    if x in memory: return memory[x]

    maxV = 0
    for i, v in I.iteritems():
        if x >= i:
            f = v + V2(x - i)
            if f > maxV:
                maxV = f

    memory[x] = maxV
    return maxV

K = 15;
print V2(K)  # very fast
print V(K)  # slow as treacle
