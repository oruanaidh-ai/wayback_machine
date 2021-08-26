import os
import sys
import time
from multiprocessing import Pool, cpu_count
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(*current_dir.split(os.path.sep)[:-2])
sys.path.append( str( Path('/') / Path(parent_dir) / 'utils' ) )

from tools.dsp.sliding_window import SlidingWindow


def get_interval_times(t, stride, width):
    times = SlidingWindow(t, stride=stride, width=width)
    return np.mean([*times], axis=-1)


def power_spectrum(data, window, fs, maxF):
    fft = np.fft.rfft((data - np.mean(data)) * window)
    crop = int( maxF/fs * len(data) )
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
def spectrogram_multiprocess(data, fs, t, maxF):
    stride = fs
    width = fs*30
    slider = SlidingWindow(data, stride=stride, width=width)

    window = np.hamming(width)

    times = get_interval_times(t, stride, width)

    with Pool(cpu_count()) as pool:
        spec = pool.map(partial(power_spectrum, window=window, fs=fs, maxF=maxF),  slider, chunksize=5000)

    return np.array( spec ), times


@timer
def spectrogram(data, fs, t, maxF):

    stride = fs
    width = fs*30
    slider = SlidingWindow(data, stride=stride, width=width)

    times = get_interval_times(t, stride, width)

    window = np.hamming(width)

    spec = [power_spectrum(s, window, fs, maxF) for s in slider]
    return np.array(spec), times


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
    fs = 150
    N = fs*3600
    maxF = 3

    t = np.linspace(0, N, N*fs)
    f_init = 1
    f_final = 2
    alpha = (f_final - f_init)/N

    data = np.sin(2*np.pi*(f_init*t + 0.5*alpha*t*t)) + np.random.normal(len(t))

    print('Multiprocessing')
    spec, times = spectrogram_multiprocess(data, fs=fs, t=t, maxF=maxF)

    #draw_spectrogram( np.arcsinh(spec), fs=fs, times=times, filename='spectrum_mp.png')


    print('Single CPU')
    spec, times = spectrogram(data, fs=fs, t=t, maxF=maxF)

    draw_spectrogram( np.arcsinh(spec*100), fs=fs, times=times, maxF=maxF, filename='spectrum.png')
    
    
if __name__ == '__main__':

    main()


