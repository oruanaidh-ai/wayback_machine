import random
import sys
N = 150

paths = dict()

for i in range(5000):
    x = int(random.random()*N)
    y = int(random.random()*N)
    d = 60+int(random.random()*N)
    
    if y > x and (x, y) not in paths: 
        paths[(x, y)] = d

inlinks = dict()
for x, y in paths.keys():
    if y not in inlinks:
        inlinks[y] = []
    inlinks[y].append(x)

memory = dict()

class NoPathFoundError(Exception):
    pass


def get_path(a, b):

    if (a, b) in memory: return memory[(a, b)]

    if a == b:
        return 0, (a, )

    dd = 1e6
    kk = -8;

    if b not in inlinks: raise NoPathFoundError

    for k in inlinks[b]:
        if k==b: continue
        if paths[(k, b)] < dd:
            dd =  paths[(k, b)]
            kk = k
    memory[ (kk, b) ] = dd, (kk, )

    dnew, p = get_path(a, kk)

    return dd + dnew, p + (kk,) 


src = min(x for x, y in paths.keys())
tgt = max(y for x, y in paths.keys())

print src, tgt

if len(inlinks[tgt]) > 1:
    try:
        f = get_path(src, tgt)

        print f

        if src in inlinks[tgt]:
            print 'Direct path found'
            m = (tgt,)
            print (src, tgt), paths[(src, tgt)]
        else:
            m = f[1] + (tgt,)
        
            print len(m)

            for c, x in enumerate(m[:-1]):
                ss, tt = m[c], m[c+1]
                if ss==tt: continue
                print (ss, tt), paths[(ss, tt)]
    
    except NoPathFoundError:
        print 'No path found'

else:
    print 'No path found'
