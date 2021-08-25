from collections import deque

import sys
import numpy as np
import pylab as pl

def findpeaks_naive(f, W=100):
    """
    Iterator to find the peaks in a set of data points. 

    The algorithm is dumb. It checks to see if each element is greater
    than the W values to the left and W values to the right.

    Args: 
        f: the data 
        W: (optional) The half-width of the window. A
        peak must be greater than W elements to its left and W
        elements to its right.

    Returns: 
        the peaks of the data, one at a time (streaming)

    Raises: 
        StopIteration.
    """    

    N = len(f)

    for i in range(W, N-W):
        foundPeak = True
        current = f[i]

        for j in range(i-W, i+W+1):
            if current < f[j]:
                foundPeak = False
                break

        if foundPeak:
            yield i


def findpeaks(f, W=100):
    """
    Iterator to find the peaks in a set of data points. 

    The algorithm uses a double ended queue. The front of the queue
    contains the index of a running maximum. When this index is
    differs from the index at the back of the queue (the current
    position) by half a window width a peak is located.  The double
    ended queue method of computing a running maximum is described by
    Leet: http://articles.leetcode.com/sliding-window-maximum/

    Args: 
        f: the data 
        W: (optional) The half-width of the window. A
        peak must be greater than W elements to its left and W
        elements to its right.

    Returns: 
        the peaks of the data, one at a time (streaming)

    Raises: 
        StopIteration.
    """

    deq = deque()

    N = len(f)
    WW = 2*W+1

    if N < WW:
        raise StopIteration

    WW = 2*W+1
    for i in range(WW-1):

        while len(deq) > 0 and f[i] > f[deq[-1]]:
            deq.pop()   # bump smaller values off the back

        deq.append(i)

    for i in range(WW-1, N):

        while len(deq) > 0 and f[i] > f[deq[-1]]:
            deq.pop()   # bump smaller values off the back

        while len(deq) > 0 and deq[0] <= i-WW:
            deq.popleft()  # remove the front because the window is past

        deq.append(i)        

        if deq[0] == i - W:
            yield deq[0]   # it's a peak if it's in the middle of the window


if __name__ == '__main__':

    usage = """
Speed test:

naive find peaks

(sigproc) Joe ~/work $ time python {} 1

real	0m9.287s
user	0m9.224s
sys	0m0.042s

better find peaks

(sigproc) Joe ~/work $ time python {} 2

real	0m0.507s
user	0m0.456s
sys	0m0.037s

""".format(sys.argv[0], sys.argv[0])

    showPlots = False  # make true to see data and peaks
    
    N = 200000
    W = 1000
    t = np.arange(N)
    T = 2000.0
    f = np.sin(2*np.pi*t/T) + 3*np.sin(3*np.pi*t/T)

    if len(sys.argv) > 1:
        choice = int(sys.argv[1])
    else:
        print(usage)
        sys.exit(0)

    if choice == 1: # naive
        peaks = np.array(list(findpeaks_naive(f, W)))
    elif choice == 2: # fast
        peaks = np.array(list(findpeaks(f, W)))
    else:
        printf('Not a valid choice ', choice)
        choice = None

    if showPlots:
        pl.plot(t, f)
        pl.plot(peaks, f[peaks], 'y*')
        pl.show()

    print(peaks)
