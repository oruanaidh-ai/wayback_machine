import sys
import time
from multiprocessing import Pool, cpu_count
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append('/Users/oruanaidh/projects/wayback_machine/PYTHON/utils')

from tools.dsp.sliding_window import SlidingWindow


def get_interval_times(t, stride, width):

    times = SlidingWindow(t, stride=stride, width=width)

    return np.mean([*times], axis=-1)


def power_spectrum(data, window):
    fft = np.fft.rfft(data * window)
    return np.abs(fft)


def timer(func, *args, **kwargs):
    def count_ticks(*args, **kwargs):
        t1 = time.time()
        ret = func(*args, **kwargs)
        t2 = time.time()
        print(f'{func.__name__} took {t2-t1:1.3f} seconds')
        return ret
    return count_ticks


@timer
def spectrogram_multiprocess(data, fs, t):
    stride = fs
    width = fs*30
    slider = SlidingWindow(data, stride=stride, width=width)

    window = np.hamming(width)
    kwargs = {'window': window}
    my_power_spectrum = partial(power_spectrum, **kwargs)

    pool = Pool(cpu_count())

    times = get_interval_times(t, stride, width)

    return np.array( pool.map(my_power_spectrum, slider) ), times


@timer
def spectrogram(data, fs, t):

    stride = fs
    width = fs*30
    slider = SlidingWindow(data, stride=stride, width=width)

    times = get_interval_times(t, stride, width)

    window = np.hamming(width)

    return np.array([power_spectrum(s, window) for s in slider]), times


def draw_spectrogram(spec, fs, times, filename):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    _, N = spec.shape
    freqs = np.arange(N)*fs/2/N

    times, freqs = np.meshgrid(times, freqs)

    ax.pcolormesh(times, freqs, spec.T, shading='auto')
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Time')


    plt.savefig(filename, dpi=150)
    #plt.show()


if __name__ == '__main__':

    fs = 128
    N = fs*900

    t = np.linspace(0, N, N*fs)
    f_init = 10
    f_final = 50
    alpha = (f_final - f_init)/N

    data = np.sin(2*np.pi*(f_init*t + 0.5*alpha*t*t)) + np.random.normal(len(t))

    print('Multiprocessing')
    spec, times = spectrogram_multiprocess(data, fs=fs, t=t)

    draw_spectrogram( 10*np.arcsinh(spec), fs=fs, times=times, filename='spectrum_mp.png')


    print('Single CPU')
    spec, times = spectrogram(data, fs=fs, t=t)

    draw_spectrogram( 10*np.arcsinh(spec), fs=fs, times=times, filename='spectrum.png')



