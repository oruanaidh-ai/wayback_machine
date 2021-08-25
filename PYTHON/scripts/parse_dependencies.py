import json
import numpy as np

parent2child = dict()
satisfied = dict()

def traverse(parent):

    for child in parent2child[parent]:
        for val in traverse(child):
            yield val
        else:
            yield child
    else:
        yield parent

def expandList(parent):

    for n in traverse(parent):
        if n not in satisfied:
            satisfied[n] = 1
            yield n


def childrenBeforeParents(lst):
    
    for item in lst:
        parent = item['package']['package_name']

        if parent not in parent2child:
            parent2child[parent] = []

        for element in item['dependencies']:
            child = element['package_name']
            parent2child[parent].append(child)

            if child not in parent2child:
                parent2child[child] = []

    nodes = []
    for p in parent2child:
        for n in expandList(p):
             nodes.append(n)

    return nodes


with open('dependencies.json') as fp:

    jtree = json.load(fp)

    dependencies = childrenBeforeParents(jtree)

    map = dict( zip(dependencies, np.arange(len(dependencies) ) ) ) 
    for d in dependencies:
        if np.any( np.array( [map[c] for c in parent2child[d]] ) > map[d]):
            print ' * FAIL * : ', d
        else:
            print 'PASS', d
                              

