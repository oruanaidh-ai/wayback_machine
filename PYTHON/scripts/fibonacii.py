class Fibonacci:
    def __init__(self):
        self.memo = dict()
        self.memo[1] = 1
        self.memo[2] = 1

    def __call__(self, N):

        if N <= 0 or type(N) != int:
            raise ValueError('Invalid argument: %s'   % str(N) )

        if N in self.memo:
            return self.memo[N]
        else:
            ret = self(N-1) + self(N-2)
            self.memo[N] = ret
            return ret

fibonacci = Fibonacci()
print (fibonacci(15))


