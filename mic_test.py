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
plt.switch_backend("agg")

# import pylab as pl

SAMPLE_RATE = 48000
CHANNELS = 4

def main():
    import signal
    import time
    # from pixel_ring import pixel_ring

    is_quit = threading.Event()

    def signal_handler(sig, num):
        is_quit.set()
        print('Quit')

    signal.signal(signal.SIGINT, signal_handler)
    start = time.time()
    count = 1
    print('------')
    chunks = list()
    with MicArray(SAMPLE_RATE, CHANNELS, SAMPLE_RATE / CHANNELS)  as mic:
        for chunk in mic.read_chunks():
            direction = mic.get_direction(chunk)
            # pixel_ring.set_direction(direction)
            # print(int(direction))
            print("Channel:%d, lengtchunkh:%d" % (count, len(chunk)))
            chunks.append(chunk)
            print(chunk)
            print(type(chunk))
            print('------appended------')
            count = count + 1
            if time.time() - start > 1.0:
                break

            if is_quit.is_set():
                break

    chans = [list(), list(), list(), list()]
    start = 0
    for c in chunks:
        for i in range(len(c)):
            channel = i % 4
            chans[channel].append(c[i])

    pro_chans = [np.asarray(chan) for chan in chans]

    # file = open("./signal.txt", "w")
    N = 48000
    T = 1.0 / 48000
    x = np.linspace(0.0, N*T, N)
    i = 1
    for c in pro_chans:
        yf = fft(c)
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
        plt.grid()
        plt.show()
        plt.savefig('channel-{}.png'.format(i), format='png')
        i += 1
        # for i in c:
            # file.write(i)
            # file.write(',')
        # file.write('\n')
    # file.close()

if __name__ == '__main__':
    main()
