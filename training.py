import pyaudio
import Queue
import threading
import numpy as np
from gcc_phat import gcc_phat
import math
from mic_array import MicArray
import numpy as np
import pandas as pd
from multiprocessing import Process, Queue
from bluetooth import *
import time
import os
import pygame


SAMPLE_RATE = 48000
CHANNELS = 8
DATA_RATE = 200
AUDIO_NAME = 'raw_data/sig1822k_210duo_pi.wav'
PLAY_TIME = 20 # seconds

# MicArray part
def mic_main(client_sock):
    record_queue = Queue()
    record_p = Process(target=record, args=(record_queue, PLAY_TIME))
    play_p = Process(target=play, args=(AUDIO_NAME, PLAY_TIME))
    save_p = Process(target=save, args=(record_queue))
    play_p.start()
    record_p.start()
    save_p.start()
    save_p.join()
    record_p.join()
    play_p.join()

def play(audio, end_time=20.0):
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    start = time.time()
    while pygame.mixer.music.get_busy() == True:
        if time.time() - start > end_time:
            print('record break')
            break
        continue

def record(queue, end_time=20.0):
    import signal
    # from pixel_ring import pixel_ring

    is_quit = threading.Event()

    def signal_handler(sig, num):
        is_quit.set()
        print('Quit')

    signal.signal(signal.SIGINT, signal_handler)
    start = time.time()
    print('------')
    with MicArray(SAMPLE_RATE, CHANNELS,  CHANNELS * SAMPLE_RATE / DATA_RATE)  as mic:
        for chunk in mic.read_chunks():
            chans = [list(), list(), list(), list()]
            for i in range(len(chunk)):
                index = i % CHANNELS
                if index < 4:
                    chans[index].append(chunk[i])
            queue.put(chans)
            if time.time() - start > end_time:
                print('record break')
                break

            if is_quit.is_set():
                print('start break')
                break
    queue.put('DONE')

def save(queue):
    record_data = pd.DataFrame(columns=['MIC1','MIC2','MIC3','MIC4'])
    while True:
        chans = queue.get()
        if chans == 'DONE':
            break
        pd.concat(record_data, [pd.DataFrame([chans[0][i], chans[1][i], chans[2][i], chans[3][i]], columns=['MIC1','MIC2','MIC3','MIC4']) for i in len(chans[0])], ignore_index=True)
    time_stamp = get_time_stamp()
    output_file = 'record_'+time_stamp
    record_data.to_csv(output_file, index=False)

def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    return "%s-%03d" % (data_head, data_secs)


# Bluetooth part

def main():
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "SampleServer",
                       service_id = uuid,
                       service_classes = [ uuid, SERIAL_PORT_CLASS ],
                       profiles = [ SERIAL_PORT_PROFILE ],
    #                   protocols = [ OBEX_UUID ]
                        )

    print "Waiting for connection on RFCOMM channel %d" % port

    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info

    mic_main(client_sock)

    try:
        data = client_sock.recv(1024)
        print "received [%s]" % data
        while data:
            client_sock.send('Received => ' + str(data))
            data = client_sock.recv(1024)
            if len(data) == 0: break
            print "received [%s]" % data

            if data == 'record':
                client_sock.send('Start recording')
                mic_main(client_sock)
                pass

            # send data back
    except IOError:
        pass

    print "disconnected"

    client_sock.close()
    server_sock.close()
    print "all done"

if __name__ == '__main__':
    # main()
    mic_main(None)
