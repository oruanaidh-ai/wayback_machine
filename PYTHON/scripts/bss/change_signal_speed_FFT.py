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


# Scale time in the frequency domain
def changer(x, fac):

    N = len(x)

    Nout = int(fac*N)

    Fout = np.zeros(Nout, dtype=complex)

    F = np.fft.fft(x, N)

    if fac > 1:
        indx = np.arange(1, N/2)
    else:
        indx = np.arange(1, Nout/2)

    Fout[0] = F[0]
    Fout[indx] = F[indx]
    Fout[-indx] = F[-indx]
    Fout[Nout/2] = F[N/2];

    out = np.fft.ifft(Fout, Nout)
    print out
    
    return np.real(out)


if __name__ == '__main__':

    # Read in data
    src1, fs = sf.read('onam66_p0db_am000m12_am150f21_y1static.wav')
    #sf.write('src1.wav', src1, fs1)

    N = len(src1)
 
    mix1 = changer(src1, 3)

    sf.write('mix1.wav', mix1, fs)

