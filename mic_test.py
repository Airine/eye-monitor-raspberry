import pyaudio
import Queue
import threading
import numpy as np
from gcc_phat import gcc_phat
import math
from mic_array import MicArray
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
import os
import time
import signal
plt.switch_backend("agg")

SAMPLE_RATE = 48000
CHANNELS = 8

# Get record chunks in `time_range` seconds.
def get_chunks(time_range=1.0):

    # from pixel_ring import pixel_ring

    is_quit = threading.Event()

    def signal_handler(sig, num):
        is_quit.set()
        print('Quit')

    signal.signal(signal.SIGINT, signal_handler)
    print('------')
    chunks = list()
    with MicArray(SAMPLE_RATE, CHANNELS, SAMPLE_RATE / CHANNELS)  as mic:
        start = time.time()
        for chunk in mic.read_chunks():
            if time.time()-start > time_range:
                break
            chunks.append(chunk)

            if is_quit.is_set():
                break
    print('------')
    print('record finished')
    return chunks

# Preprocess and return the processed chunk list.
def preprocess(chunks, channels=8):
    chans = [list() for i in range(channels)]
    start = 0
    for c in chunks:
        for i in range(len(c)):
            channel = i % channels
            chans[channel].append(c[i])
    print('------')
    print('preprocess finished')
    return [np.asarray(chan) for chan in chans]

# Plot the fft figure of the channels
def plot_fft(N, T, pro_chans):

    # N = 48000
    # T = 1.0 / 48000
    # x = np.linspace(0.0, N*T, N)
    i = 1
    for c in pro_chans:
        print('------')
        print('ploting fft')
        yf = fft(c)
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
        plt.grid()
        plt.show()
        plt.savefig('fft-channel-{}.png'.format(i), format='png')
        plt.close()
        i += 1

# plot the signal in time sequence.
def plot_signal(pro_chans, head=False):
    i = 1
    for c in pro_chans:
        print('------')
        print('ploting')
        x = np.linspace(1, len(c), len(c))
        if head:
            x = np.linspace(1, 200, 200)
            c = c[:200]
        plt.plot(x, c)
        plt.grid()
        plt.show()
        plt.savefig('time-channel-{}.png'.format(i), format='png')
        plt.close()
        i += 1

if __name__ == '__main__':
    chunks = get_chunks()
    pro_chans = preprocess(chunks, channels=8)
    N = 48000
    T = 1.0 / 48000
    # plot_signal(pro_chans, head=True)
    plot_fft(N, T, pro_chans)
