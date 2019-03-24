from scipy import signal
from scipy import fftpack
import numpy as np
import matplotlib.pyplot as plt
import math

T = 10
fs = 48000
f1 = 5000
f2 = 10000

N = T*fs
n = [i for i in range(N)]
t = np.linspace(0, T, N)

x = np.sin(2*math.pi*f1*t) + 0.5*np.sin(2*math.pi*f2*t)     # Signal composed of 5kHz and 10kHz components
X = fftpack.fft(x)                                          # FFT to the original sin

[b, a] = signal.butter(20, 2*7000/fs, 'high')               # Butterworth low/high-pass filter
y = signal.filtfilt(b, a, x)                                # Filtering
Y = fftpack.fft(y)                                          # FFT to the filtered signal

axis_f = fftpack.fftfreq(len(X)) * fs
plt.subplot(311)
plt.plot(t, x)
plt.title('5kHz')
plt.axis('tight')
plt.subplot(312)d
plt.plot(axis_f, abs(X))
plt.title('FFT')
plt.subplot(313)
plt.plot(axis_f, abs(Y))
plt.show()
