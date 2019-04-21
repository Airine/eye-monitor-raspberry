# import pyaudio
import pygame
from multiprocessing import Process, Queue
from mic_array import MicArray
import subprocess
import time

SAMPLE_RATE = 48000
CHANNELS = 8
AUDIO_NAME = 'raw_data/sig1822k_5s.wav'
PLAY_TIME = 5 # seconds

def play(audio, end_time=20.0):
    proc = subprocess.Popen(['aplay', '-d', str(end_time), audio])
    print(proc.pid)

def record(file_name, end_time=20.0):
    proc = subprocess.call(['arecord', '-Dac108', '-f', 'S16_LE', '-r', '48000', '-c', '4', '-d', str(end_time), file_name])
    print(proc.pid)

def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    return "%s-%03d" % (data_head, data_secs)

def main():
    file_name = get_time_stamp() + '-record.wav'
    play_p = Process(target=play, args=(AUDIO_NAME, PLAY_TIME,))
    record_p = Process(target=record, args=(file_name, PLAY_TIME,))
    record_p.start()
    play_p.start()
    # start = time.time()
    # while time.time() - start < PLAY_TIME:
    #     # busy waiting.
    #     time.sleep(0.05)
    # print('force end')
    # play_p.terminate()
    # record_p.terminate()
    record_p.join()
    play_p.join()


if __name__ == '__main__':
    main()
