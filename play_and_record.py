from multiprocessing import Process, Queue
import subprocess
import time
import argparse
import wave
import contextlib

AUDIO_NAME = 'raw_data/sig1822k_5s.wav'
RECORD_NAME= ''
PLAY_TIME = 5 # seconds

# process_queue = Queue()
# TODO: adding force termination.
def play(audio, end_time=20.0):
    proc = subprocess.Popen(['aplay', '-d', str(end_time), audio])
    print(proc.pid)

def record(file_name, end_time=20.0):
    proc = subprocess.Popen(['arecord', '-Dac108', '-f', 'S16_LE', '-r', '48000', '-c', '4', '-d', str(end_time), file_name])
    print(proc.pid)

def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    return "%s-%03d" % (data_head, data_secs)

def get_wave_duration(file_name):
    with contextlib.closing(wave.open(file_name,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

def main():
    parser = argparse.ArgumentParser(description='play a audio and record in the same time')
    # parser.add_argument('-h', '--help', )
    # group = parser.add_mutually_exclusive_group()
    # parser.add_argument('-t', '--test', help='test with 5 seconds wav',
    #                     action='store_true')
    parser.add_argument('-d', '--duration', help='specify the play and record duration')
    parser.add_argument('play_audio', type=str, default='raw_data/sig1822k_5s.wav', help='the file name of the audio needed to play.')
    parser.add_argument('record_file', type=str, default='record/test.wav', help='the file path of your record')
    args = parser.parse_args()
    
    AUDIO_NAME = args.play_audio
    RECORD_NAME= args.record_file

    PLAY_TIME = int(get_wave_duration(AUDIO_NAME))
    # TODO
    # if args.d:
    #    print('set duration')
    #     if args.d < PLAY_TIME:
    #         PLAY_TIME = args.d
    #         print('set success')
    #     else:
    #         print('set failed')

    play_p = Process(target=play, args=(AUDIO_NAME, PLAY_TIME,))
    record_p = Process(target=record, args=(RECORD_NAME, PLAY_TIME,))
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
