import pickle
import socket, threading, time, random


PORTS = [5000, 5001, 5002]
N = len(PORTS)
PIDS = range(N)
MAJORITY = N // 2 + 1

delay = 0.5


def send_msg(receiver, msg):
    """ General purpose sender """

    def delay_send(receiver, msg, delay):
        try:
            time.sleep(delay)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', PORTS[receiver])) # safe
            s.send(pickle.dumps(msg))
        except Exception as e:
            print("Failed to send to process " + str(receiver) + "... but it doesn't matter!")
        # print("msg sent", msg)
    
    t = threading.Thread(target=delay_send, args=(receiver, msg, delay))
    t.start()
    


def listener(port, stop_signal, task_queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(5)
    print("start listening")

    while True:
        if task_queue().empty():
            if stop_signal():
                print("listen thread exiting")
                break
        s.settimeout(2.0)
        try:
            c, addr = s.accept()
            data = c.recv(1024)
            msg = pickle.loads(data)
            # print("msg received", msg)
            task = msg
            task_queue().put(task)
            c.close()
        except Exception:
            pass
    return