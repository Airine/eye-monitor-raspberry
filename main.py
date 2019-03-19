import pyaudio
import Queue
import threading
import numpy as np
from gcc_phat import gcc_phat
import math
from mic_array import MicArray
import numpy as np
from multiprocessing import Process, Queue
from bluetooth import *
import time

SAMPLE_RATE = 48000
CHANNELS = 4
DATA_RATE = 200

# MicArray part
def mic_main(client_sock):
    record_queue = Queue()
    # process_p = Process(target=other_test, args=(record_queue,))
    record_p = Process(target=record, args=(record_queue,))
    process_p = Process(target=process_record, args=(record_queue,))
    process_p.start()
    record_p.start()
    # process_p.start()
    record_p.join()
    process_p.join()

def record(queue, end_time=10.0):
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
            # direction = mic.get_direction(chunk)
            # pixel_ring.set_direction(direction)
            # print(int(direction))
            # print("Chunk length: %d" % (len(chunk)))
            chans = [list(), list(), list(), list()]
            for i in range(len(chunk)):
                chans[i%4].append(chunk[i])
            # print(chunk)
            # print(type(chunk))
            queue.put(chans)
            # print('------appended------')
            if time.time() - start > end_time:
                print('record break')
                break

            if is_quit.is_set():
                print('start break')
                break

def other_test(queue):
    while True:
        print('testing')
        time.sleep(0.005)

def process_record(queue, end_time=10.0):
    print('entering process')
    while True:
        time.sleep(0.005)
        # print('testing')
        print('try get data')
        data = queue.get_nowait()
        print('success get')
        if not data :
            time.sleep(0.005)

    # start_time = time.time()
    # dir = 'data/' + str(time.strftime("%Y-%m-%d", time.localtime(time.time()))) + '/'
    # while True:
    #     if time.time() - start_time > end_time:
    #         print('process break')
    #         break
    #     print('try get data')
    #     data = queue.get_nowait()
    #     print('success get')
    #     if not data :
    #         time.sleep(0.005)
    #     chans = [np.asarray(chan) for chan in data]
    #     ct = time.time()
    #     local_time = time.localtime(ct)
    #     data_head = time.strftime("%H:%M:%S", local_time)
    #     data_secs = (ct - int(ct)) * 1000
    #     time_stamp = "%s-%03d" % (data_head, data_secs)
    #     for i in len(chans):
    #         target_file = dir + '-channel{}-'.format(i) + time_stamp + '.npy'
    #         print(target_file)
    #         np.save(target_file, chans[i])
    #
    #     time.sleep(0.005)


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
    main()
