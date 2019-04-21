# import pyaudio
from multiprocessing import Process, Queue
from mic_array import MicArray
import subprocess

SAMPLE_RATE = 48000
CHANNELS = 8
AUDIO_NAME = 'raw_data/sig1822k_5s.wav'
PLAY_TIME = 5 # seconds

def play(audio, end_time=20.0):
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    start = time.time()
    while pygame.mixer.music.get_busy() == True:
        if time.time() - start > end_time:
            print('play break')
            break
        continue

def record(file_name):
    subprocess.call(['arecord', '-Dac108', '-f', 'S32_LE', '-r', '48000', '-c', '4', file_name])

def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    return "%s-%03d" % (data_head, data_secs)

def main():
    file_name = get_time_stamp() + '-record.wav'
    play_p = Process(target=play, args=(AUDIO_NAME, PLAY_TIME,))
    record_p = Process(target=record, args=(file_name,))
    play_p.start()
    record_p.start()
    start = time.time()
    while time.time() - start < PLAY_TIME:
        # busy waiting.
        time.sleep(0.05)
    print('force end')
    play_p.terminate()
    record_p.terminate()
    record_p.join()
    play_p.join()


if __name__ == '__main__':
    main()
