from network import PORTS, N, send_msg, listener, delay
from paxos import Paxos
from BlockChain import BlockChain
from BlockNode import BlockNode, createBlockNode
from Transaction import Transaction
import queue
import argparse
import threading

task_queue = queue.Queue() # task queue
my_pid = -1
paxos = None
chain =  BlockChain(n=N)
transaction_queue = [] # transactions that have not been proposed
proposed_block = None # block of transactions that is in proposal but not yet accepted


def processer(stop_signal):
    """ Processer thread """
    global transaction_queue
    print("processing")
    while True:
        while task_queue.empty():
            if stop_signal():
                break
        if not task_queue.empty():
            task = task_queue.get()
            print('task:', task)

        if task['type'] == 'console':
            if len(task['args']) == 0:
                pass

            elif task['args'][0] == 'propose':
                if len(transaction_queue) > 0:
                    # create block from transaction_queue and clear the queue
                    proposed_block = createBlockNode(transaction_queue, (chain.head.hash() if chain.head is not None else '0'*64))
                    transaction_queue = []
                    paxos.new_proposal(proposed_block)
                    paxos.print()
                else:
                    print('Empty transaction queue.')

            elif task['args'][0] == 'moneyTransfer':
                sender = int(task['args'][1])
                receiver = int(task['args'][2])
                amount = float(task['args'][3])
                trans = Transaction(sender, receiver, amount)
                if chain.verify_transaction(trans):
                    transaction_queue.append(trans)
                    print("Valid transaction.")
                else:
                    print('Insufficient balance.')

            elif task['args'][0] == 'failProcess':
                exit(0)

            elif task['args'][0] == 'delay':
                delay = float(task['args'][1])
            
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



def on_decision(self, msg):
    global proposed_block
    global chain
    # TODO: check depth here
    # add to chain
    print('on_decision')
    print(chain)
    chain.insert(msg['val'])
    print(chain)
    # remove everything in proposed block and transaction queue
    proposed_block = None
    transaction_queue = []
    # if msg['val'] != proposed_block:
    #     print('Other node appended to the block chain. Local transaction queue deleted.')        
    #     transaction_queue = []



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
    # processer_thread = threading.Thread(target=processer, args=(lambda: processer_thread_stop_signal, lambda: transaction_queue))
    processer_thread.start()
    
    print('paxos init')
    paxos = Paxos(my_pid)
    paxos.on_decision = on_decision

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