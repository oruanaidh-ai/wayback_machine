import sys

a = sys.argv[1]
b = sys.argv[2]

v = []
for ch in b:
    if ch in a:
        v.append(ch)

print ''.join(v)

mem=  dict()
for ch in a: mem[ch]=1
 
v=[]
for ch in b:
    if ch in mem:
        v.append(ch)

print ''.join(v)

v = [ch for ch in b if ch in a]
print ''.join(v)


v = [ch for ch in b if ch in mem]
print ''.join(v)
