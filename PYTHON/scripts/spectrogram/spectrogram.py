import os
import sys
import time
from multiprocessing import Pool, cpu_count
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

FS = 128
N = FS*60*10
maxF = 3
STRIDE = FS
WIDTH = 32*FS

t = np.linspace(0, N, N*FS)
f_init = 1
f_final = 2
alpha = (f_final - f_init)/N

data = np.sin(2*np.pi*(f_init*t + 0.5*alpha*t*t)) + np.random.normal(len(t))


current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(*current_dir.split(os.path.sep)[:-2])
sys.path.append( str( Path('/') / Path(parent_dir) / 'utils' ) )

from tools.dsp.sliding_window import SlidingWindowIndexer


def get_interval_times(t, stride, width):
    nBlk = (len(t)-width)//stride + 1
    nSample = nBlk * stride

    return np.linspace(t[width//2]/FS, t[width//2 + nSample]/FS, nBlk)


def power_spectrum(indx, width, window, fs, maxF):
    d = data[indx:indx+width]
    fft = np.fft.rfft((d - np.mean(d)) * window)
    crop = int( maxF/fs * width )
    return np.abs(fft)[:crop]


def timer(func, *args, **kwargs):
    def count_ticks(*args, **kwargs):
        t1 = time.time()
        ret = func(*args, **kwargs)
        t2 = time.time()
        print(f'{func.__name__} took {t2-t1:1.3f} seconds')
        return ret
    return count_ticks


@timer
def spectrogram_multiprocess(fs, t, maxF):
    slider = SlidingWindowIndexer(data, stride=STRIDE, width=WIDTH)

    window = np.hamming(WIDTH)

    times = get_interval_times(t, STRIDE, WIDTH)

    psfunc = partial(power_spectrum, width=WIDTH, window=window, fs=fs, maxF=maxF)

    with Pool(cpu_count()-2) as pool:
        spec = np.array( pool.map(psfunc,  slider, chunksize=2**10))

    return spec, times


@timer
def spectrogram(fs, t, maxF):

    slider = SlidingWindowIndexer(data, stride=STRIDE, width=WIDTH)

    times = get_interval_times(t, STRIDE, WIDTH)

    window = np.hamming(WIDTH)

    spec = np.array([power_spectrum(indx, WIDTH, window, fs, maxF) for indx in slider])

    return spec, times


def draw_spectrogram(spec, fs, times, maxF, filename):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    _, N = spec.shape
    freqs = np.arange(N)/N*maxF

    times, freqs = np.meshgrid(times, freqs)

    ax.pcolormesh(times, freqs, spec.T, shading='auto')
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Time')

    plt.savefig(filename, dpi=150)
    #plt.show()


def main():

    print('Multiprocessing')
    spec, times = spectrogram_multiprocess(fs=FS, t=t, maxF=maxF)

    #draw_spectrogram( np.arcsinh(spec), fs=FS, times=times, filename='spectrum_mp.png')


    print('Single CPU')
    spec, times = spectrogram(fs=FS, t=t, maxF=maxF)

    draw_spectrogram( np.arcsinh(spec*100), fs=FS, times=times, maxF=maxF, filename='spectrum.png')
    
    
if __name__ == '__main__':

    main()


