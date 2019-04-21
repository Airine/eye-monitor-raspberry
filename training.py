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
import codecs
import csv

record_queue = Queue()

FILENAME = 'test.csv'
ENCODING = 'utf-8'
SAMPLE_RATE = 48000
CHANNELS = 8
DATA_RATE = 1
AUDIO_NAME = 'raw_data/sig1822k_210duo_pi.wav'
PLAY_TIME = 5 # seconds

# MicArray part
def mic_main(client_sock):
    record_queue = Queue()
    #play_p = Process(target=play, args=(AUDIO_NAME, PLAY_TIME,))
    #save_p = Process(target=save, args=(record_queue, PLAY_TIME,))
    record_p = Process(target=record, args=(record_queue, PLAY_TIME,))
    record_p.start()
    while True:
        if record_queue.get() == 'start':
            break
    #play_p.start()
    #save_p.start()
    #save_p.join()
    record_p.join()
    #play_p.join()

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

def record(queue, end_time):
    import signal
    # from pixel_ring import pixel_ring

    is_quit = threading.Event()

    def signal_handler(sig, num):
        is_quit.set()
        print('Quit')

    signal.signal(signal.SIGINT, signal_handler)
    start = time.time()
    print('------')
    with MicArray(SAMPLE_RATE, CHANNELS,  CHANNELS * SAMPLE_RATE)  as mic:
        print('------')
        with codecs.open(FILENAME, "w", ENCODING) as f:
            writer = csv.writer(f)
            queue.put('start')
            for chunk in mic.read_chunks():
                # chans = pd.DataFrame(columns=['MIC1','MIC2','MIC3','MIC4'])
                for i in range(len(chunk)/4):
                    # index = i % CHANNELS
                    row = [chunk[4*i], chunk[4*i+1], chunk[4*i+2], chunk[4*i+3]]
                    writer.writerow(row)
                    #if index < 4:
                        #chans[index].append(chunk[i])
                queue.put(chans)
                print('recording')
                if time.time() - start > end_time:
                    print('record break')
                    break

                if is_quit.is_set():
                    print('start break')
                    break
            queue.put('DONE')
    print('record finished')

def save(queue, end_time):
    record_data = pd.DataFrame(columns=['MIC1','MIC2','MIC3','MIC4'])
    start = time.time()
    while True:
        chans = queue.get()
        if not chans:
            time.sleep(0.02)
            continue
        if chans == 'DONE':
            break
        print('saving')
        for i in range(len(chans[0])):
            tempt = pd.DataFrame([[chans[0][i], chans[1][i], chans[2][i], chans[3][i]],], columns=['MIC1','MIC2','MIC3','MIC4'])
            #print(tempt)
            record_data = pd.concat([record_data, tempt], ignore_index=True)
    time_stamp = get_time_stamp()
    output_file = 'record_'+time_stamp
    record_data.to_csv(output_file, index=False)
    print('save finished')

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
    # record(record_queue, PLAY_TIME)
