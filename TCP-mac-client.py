from threading import Thread
import socket, time
from python_visual_animation import scatter_plot
import numpy as np

VERBOSE = False
IP_ADDRESS = "10.20.43.94"
IP_PORT = 22000

def debug(text):
    if VERBOSE:
        print("Debug:---", text)

# ------------------------- class Receiver ---------------------------
class Receiver(Thread):
    def run(self):
        debug("Receiver thread started")
        while True:
            try:
                rxData = self.readServerData()
            except:
                debug("Exception in Receiver.run()")
                isReceiverRunning = False
                closeConnection()
                break
        debug("Receiver thread terminated")

    def readServerData(self):
        debug("Calling readResponse")
        bufSize = 4096
        data = ""
        while data[-1:] != "\0": # reply with end-of-message indicator
            try:
                blk = sock.recv(bufSize)
                if blk != None:
                    debug("Received data block from server, len: " + \
                        str(len(blk)))
                else:
                    debug("sock.recv() returned with None")
            except:
                raise Exception("Exception from blocking sock.recv()")
            data += blk
        print("Data received:", data)
# ------------------------ End of Receiver ---------------------

def startReceiver():
    debug("Starting Receiver thread")
    receiver = Receiver()
    receiver.start()

def sendCommand(cmd):
    debug("sendCommand() with cmd = " + cmd)
    try:
        # append \0 as end-of-message indicator
        sock.sendall(cmd + "\0")
    except:
        debug("Exception in sendCommand()")
        closeConnection()

def closeConnection():
    global isConnected
    debug("Closing socket")
    sock.close()
    isConnected = False

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    debug("Connecting...")
    try:
        sock.connect((IP_ADDRESS, IP_PORT))
    except:
        debug("Connection failed.")
        return False
    startReceiver()
    return True

# ------------------------ End of TCP functions ---------------------

def training_main():
    ready_one = 6*np.ones(100)
    ready_zero= 6*np.ones(100)
    x_ready = np.concatenate((ready_one, ready_zero, ready_one, ready_zero,
                        ready_one, ready_zero, ready_one, ready_zero,
                        ready_one, ready_zero))
    y_ready = np.concatenate((ready_one, ready_zero, ready_one, ready_zero,
                        ready_one, ready_zero, ready_one, ready_zero,
                        ready_one, ready_zero))

    x_hori = np.linspace(2, 10, 800)
    x_hore = np.linspace(10, 2, 800)
    x_2 = 2*np.ones(100)
    x_10= 10*np.ones(100)

    y_down = list()
    y_hori = list()
    for i in [10, 8, 6, 4]:
        y_down.append(np.linspace(i, i-2, 100))
        y_hori.append(i*np.ones(800))
    y_hori.append(2*np.ones(800))
    x = np.concatenate((x_ready, x_hori, x_10, x_hore, x_2,
                        x_hori, x_10, x_hore, x_2,
                        x_hori))
    y = np.concatenate((y_ready, y_hori[0], y_down[0], y_hori[1], y_down[1],
                        y_hori[2], y_down[2], y_hori[3], y_down[3],
                        y_hori[4]))
    scatter_plot(x,y)

if __name__ == '__main__':
    sock = None
    isConnected = False

    if connect():
        isConnected = True
        print("Connection established")
        time.sleep(1)
        while isConnected:
            # print "Sending command: go..."
            # sendCommand("go")
            command = input("Please enter a command:")
            if command == "training":
                training_main()
                pass
            else:
                sendCommand(command)
            time.sleep(2)
    else:
        print("Connection to %s:%d failed" % (IP_ADDRESS, IP_PORT))
    print("done")
