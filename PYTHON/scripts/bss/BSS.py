import sys

import soundfile as sf
from math import pi
import numpy as np
from scipy import signal
from scipy import stats
from scipy import optimize
from numpy import linalg as LA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


# Time delay in the frequency domain
def delay(x, delay):

    N = len(x)

    FFT_LEN = 16
    while FFT_LEN < N + delay:
        FFT_LEN *= 2
    
    X = np.fft.fft(x, FFT_LEN)

    indx = np.arange(1, FFT_LEN/2)    
    mult = np.exp(-1j*2*pi*indx*delay/FFT_LEN)
    X[indx] = X[indx]*mult

    indx = FFT_LEN - indx
    X[indx] = X[indx]*np.conj(mult)
    
    return np.real(np.fft.ifft(X, FFT_LEN)[:N])
    

# Cross correlation in the frequency domain
def RXXsummed(delta, R11, R12, R21, R22, indx):

    shift1 = np.exp(-1j*2*pi*delta[0]*indx/FFT_LEN)
    shift2 = np.exp(-1j*2*pi*delta[1]*indx/FFT_LEN)

    # This is element 1,2 of the output covariance.
    val = -R11*shift2*np.conj(shift1) + R12*shift2 + R21*np.conj(shift1) - R22

    # we want off diagonal terms to be zero so we are minimizing the following
    # number.
    RXX = np.log(np.sum(abs(val)**2));

    return RXX


def make_plot(R11, R12, R21, R22, indx):

    print
    print 'Mesh plot'
    print
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.linspace(-3.5, 3.5, 21)
    Y = np.linspace(-3.5, 3.5, 21)

    Z = np.zeros((len(X), len(Y)))
    for i, d1 in enumerate(X):
        for j, d2 in enumerate(Y):
            val = RXXsummed((d1, d2), R11, R12, R21, R22, indx)
            print '.',
            Z[i, j] = val
        print
    print
            
    X, Y = np.meshgrid(X, Y)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

    # Customize the z axis.
    #ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


if __name__ == '__main__':

    # Read in data
    src1, fs1 = sf.read('left.wav')
    #sf.write('src1.wav', src1, fs1)

    src2, fs2 = sf.read('right.wav')
    #sf.write('src2.wav', src2, fs2)

    if fs1 != fs2:
        print >> sys.stderr, 'Sampling rates don''t match: %d != %d' % (fs1, fs2)
        sys.exit(1)
    else:
        fs = fs1

    if len(src1) > len(src2):
        N = len(src2)
        src1 = src1[:N]
    else:
        N = len(src1)
        src2 = src2[:N]


    # Two microphones spaced 10cm apart
    # Sources at 30 degrees and 90 degrees to line joining mics
    d = 0.06
    c = 343  # speed of sound
    #delta1 = fs*d/c*np.cos(pi/6)
    #delta2 = fs*d/c*np.cos(pi/2)
        
    mix1 = src1
    mix2 = src2    
    #mix1 = src1 + src2
    #mix2 = delay(src1, delta1) + delay(src2, delta2)

    sf.write('mix1.wav', mix1, fs)
    sf.write('mix2.wav', mix2, fs)


    # Precompute the FFT of each mixture and their cross correlations for speed
    N = len(mix1)

    FFT_LEN = 16
    #while FFT_LEN < N + delta1 + delta2:
    while FFT_LEN < N:## + delta1 + delta2:
        FFT_LEN *= 2;

    Y1 = np.fft.fft(mix1, FFT_LEN)
    Y2 =  np.fft.fft(mix2, FFT_LEN)
    indx = np.arange(1, FFT_LEN/2)
    Y1 = Y1[indx]
    Y2 = Y2[indx]

    R11 = Y1*np.conj(Y1)
    R12 = Y1*np.conj(Y2)
    R21 = Y2*np.conj(Y1)
    R22 = Y2*np.conj(Y2)


    # Make a mesh plot
    make_plot(R11, R12, R21, R22, indx)
 
    # Coarse search first: grid search
    print
    print 'Coarse search'
    print
    mx = d/c*fs # Maximum possible delay
    X = np.linspace(-mx, mx, 40)
    Y = X
    idx1, idx2 = 0, 0
    bestVal = np.inf
    for i, d1 in enumerate(X):
        for j, d2 in enumerate(Y):
            if d1 > d2: continue
            print '.',
            val = RXXsummed((d1, d2), R11, R12, R21, R22, indx)
            if val < bestVal:
                bestVal = val
                idx1 = i
                idx2 = j
        print
    print

    print 'Coarse search for delays: ', X[idx1], Y[idx2]
    #print 'True delays: ', delta1, delta2


    # Use the result of the coarse search as a starting point for optimizer
    deltas = optimize.fmin(RXXsummed, (X[idx1], Y[idx2]), (R11, R12, R21, R22, indx))

    delta1 = deltas[0]
    delta2 = deltas[1]
    
    print 'Optimizer delays: ', delta1, delta2

    # Compute the output
    out1 = delay(mix1, delta2)-mix2;
    out2 = delay(mix2, delta1)-mix1;
    
    sf.write('out1.wav', out1, fs)
    sf.write('out2.wav', out2, fs)




