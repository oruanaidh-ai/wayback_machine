class Node:
    pass

import random

top = Node()

def buildTree(t, lev=5):
    """
    Build a random tree. It is not a binary tree.
    Subnodes (if they exist) are placed inside a vector.
    There can be as many as fifteen subnodes.
    """
    if lev == 0: return

    subnodes = []
    for i in range(15):
        node = Node()
        if random.random() < 1.0 - 1.0/(lev+1):
            subnodes.append(buildTree(node, lev-1))
    t.subnodes = subnodes

    return t

tree = buildTree(top, 5)

count = {}
def countNodes(t):
    if t in count: return count[t]
    if hasattr(t, 'subnodes'):
        count[t] = 1 + sum(countNodes(x) for x in t.subnodes)
    else:
        count[t] = 1
    return count[t]

print countNodes(tree)

tree_memory = {}
def depth(t):
    if t in tree_memory: return tree_memory[t]
    if hasattr(t, 'subnodes') and len(t.subnodes):
        tree_memory[t] = 1 + max(depth(s) for s in t.subnodes)
    else:
        tree_memory[t] = 1
    return tree_memory[t]

print depth(tree)

ddeep = {}
def doubleDeep(t):
    if t in ddeep: return ddeep[t]
    if hasattr(t, 'subnodes') and len(t.subnodes) >= 2:
        dd = [depth(n) for n in t.subnodes]
        dd.sort()
        v = 1 + dd[-2] + dd[-1]
    else:
        v = 1

    if hasattr(t, 'subnodes') and len(t.subnodes) >= 1:
        maxVsubnode = max(doubleDeep(n) for n in t.subnodes)
        if v < maxVsubnode: v = maxVsubnode

    ddeep[t] = v
    return ddeep[t]


print doubleDeep(tree)
    
    
