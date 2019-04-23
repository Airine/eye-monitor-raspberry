from mic_array import MicArray
from multiprocessing import Process, Queue
import pygame


FILENAME = 'test.csv'
ENCODING = 'utf-8'
SAMPLE_RATE = 48000
CHANNELS = 8
DATA_RATE = 1
AUDIO_NAME = 'raw_data/sig1822k_210duo_pi.wav'
PLAY_TIME = 5 # seconds

def play(audio, end_time):
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    start = time.time()
    while pygame.mixer.music.get_busy() == True:
        if time.time() - start > end_time:
            print('play break')
            break
        continue

def aplay(audio, end_time):
    proc = subprocess.Popen(['aplay', '-d', str(end_time), audio])

def 

def main():
    pass

if __name__ == '__main__':
    main()
