import sys
memo = dict()

memo[0] = 1
memo[1] = 1

def fib(n):
    if n in memo: return memo[n]
    f = fib(n-1) + fib(n-2)
    memo[n] = f
    return f

def fib_bad(n):
    if n <= 1: return 1
    
    return fib_bad(n-1) + fib_bad(n-2)


K = 35

print fib(K)
sys.stdout.flush()
print fib_bad(K)
