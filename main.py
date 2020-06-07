from network import PORTS, send_msg, listener
from paxos import Paxos
import queue
import argparse
import threading

task_queue = queue.Queue() # event queue
my_pid = -1
paxos = None


def processer(stop_signal):
    """ Processer thread """
    print("processing")
    while True:
        while task_queue.empty():
            if stop_signal():
                break
        if not task_queue.empty():
            task = task_queue.get()
            print('task:', task)

        if task['type'] == 'console':
            if task['args'][0] == 'propose':
                paxos.set_proposel('value' + str(my_pid))
                paxos.print()
                paxos.send_prepare()
            
        elif task['type'] == 'msg-prepare':
            print('msg-prepare')
            paxos.recv_prepare(task)
        
        elif task['type'] == 'msg-promise':
            print('msg-promise')
            paxos.recv_promise(task)

        elif task['type'] == 'msg-accept':
            print('msg-accept')
            paxos.recv_accept(task)

        elif task['type'] == 'msg-accepted':
            print('msg-accepted')
            paxos.recv_accepted(task)

        elif task['type'] == 'msg-decision':
            print('msg-decision')
            paxos.recv_decision(task)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', type=int)
    arg = parser.parse_args()
    my_pid = arg.pid

    listener_thread_stop_signal = False
    listener_thread = threading.Thread(target=listener, args=(PORTS[my_pid], lambda: listener_thread_stop_signal, lambda: task_queue))
    listener_thread.start()
    processer_thread_stop_signal = False
    processer_thread = threading.Thread(target=processer, args=(lambda: processer_thread_stop_signal,))
    processer_thread.start()
    
    print('paxos init')
    paxos = Paxos(my_pid)

    # Console thread
    while(True):
        cmd_arg = input().split()
        task = {
            'type': 'console',
            'args': cmd_arg
        }
        task_queue.put(task)

    print("stop tracking keyboard input, trying to join processer_thread")
    processer_thread_stop_signal = True
    processer_thread.join()
    print("trying to join listen_thread")
    listener_thread_stop_signal = True
    listener_thread.join()
    exit()