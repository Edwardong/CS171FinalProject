from network import PORTS, N, send_msg, listener, set_delay
from paxos import Paxos
from BlockChain import BlockChain
from BlockNode import BlockNode, createBlockNode
from Transaction import Transaction, apply_transactions
import queue
import argparse
import threading
import pickle
import time
import random
from copy import copy


task_queue = queue.Queue() # task queue
my_pid = -1
paxos = None
chain =  BlockChain(n=N)
transaction_queue = [] # transactions that have not been proposed
proposed_block = None # block of transactions that is in proposal but not yet accepted


def save():
    """ Save paxos, chain, transaction_queue, (and proposed_block?) """
    try:
        with open("stored_state_" + str(my_pid) + ".state", "wb") as f:
            pickle.dump((paxos, chain, transaction_queue), f)
    except:
        pass

def load():
    global paxos, chain, transaction_queue
    try:
        with open("stored_state_" + str(my_pid) + ".state", "rb") as f:
            paxos, chain, transaction_queue = pickle.load(f)
    except Exception as e:
        pass


def propose():
    global paxos, chain, transaction_queue
    if len(transaction_queue) > 0:
        # create block from transaction_queue and clear the queue
        proposed_block = createBlockNode(transaction_queue, chain.head)
        transaction_queue = []
        paxos.new_proposal(proposed_block)
        paxos.print()
    # else:
    #     print('Empty transaction queue.')


schedule_interrupt = False # set to True to stop the timer
def schedule_proposer():
    def proposer():
        global propose, schedule_interrupt
        schedule_interrupt = False
        time.sleep(15 * (1 + random.random() * 0.5))
        if not schedule_interrupt:
            propose()
        # else:
        #     print('Scheduled proposal is interrupted by blockchain update.')
    threading.Thread(target=proposer).start()


def processer(stop_signal):
    """ Processer thread """
    global chain, transaction_queue, proposed_block, send_msg, set_delay, schedule_proposer, schedule_interrupt
    print("processing")
    while True:
        while task_queue.empty():
            if stop_signal():
                break
        if not task_queue.empty():
            task = task_queue.get()
            print('task:', str(task)[:60])

        if task['type'] == 'console':
            if len(task['args']) == 0:
                pass

            elif task['args'][0] == 'propose' or task['args'][0] == 'p':
                propose()

            elif task['args'][0] == 'moneyTransfer' or task['args'][0] == 't':
                sender = int(task['args'][1])
                receiver = int(task['args'][2])
                amount = float(task['args'][3])
                trans = Transaction(sender, receiver, amount)
                if sender == receiver:
                    print('Sender and receiver cannot be the same')
                    continue
                # compute current balance after transactions in queue
                current_balance = apply_transactions(copy(chain.balance), transaction_queue)
                if apply_transactions(current_balance, [trans]):
                    print("Valid transaction.")
                    transaction_queue.append(trans)
                    schedule_proposer()
                else:
                    print('Insufficient balance.')

            elif task['args'][0] == 'printBlockchain' or task['args'][0] == 'pc':
                print(chain)
            elif task['args'][0] == 'printBalance' or task['args'][0] == 'pb':
                print(chain.balance)
            elif task['args'][0] == 'printQueue' or task['args'][0] == 'pq':
                print(transaction_queue)
            elif task['args'][0] == 'printPaxos' or task['args'][0] == 'pp':
                paxos.print()
            
            elif task['args'][0] == 'update': # debug
                send_msg(int(task['args'][1]), {'type':'chain-reply', 'chain': chain})

            elif task['args'][0] == 'failProcess':
                return
            elif task['args'][0] == 'delay':
                set_delay(float(task['args'][1]))
            elif task['args'][0] == 'save':
                save()
            elif task['args'][0] == 'load':
                load()
                print(paxos)
                print(transaction_queue)
            
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

        elif task['type'] == 'chain-request':
            print('chain-request')
            send_msg(task['from'], {'type':'chain-reply', 'chain': chain})

        elif task['type'] == 'chain-reply':
            print('chain-reply')
            received_chain = task['chain']
            print(received_chain)
            if received_chain.depth > chain.depth:
                # reset chain, paxos, queue
                chain = received_chain
                schedule_interrupt = True
                paxos.update_depth(chain.depth)
                transaction_queue = []
                proposed_block = None
                print('Chain updated. All transactions in queue are discarded.')

        save() #save after every task


def on_inconsistent_depth(self, pid):
    print('on_inconsistent_depth')
    send_msg(pid, {'type': 'chain-request', 'from': my_pid})

def on_decision(self, msg):
    # global proposed_block
    global chain, transaction_queue, proposed_block, schedule_interrupt
    if msg['bal'].depth != chain.depth:
        on_inconsistent_depth(msg['bal'].proc_id)
        return
    # add to chain
    print('on_decision')
    schedule_interrupt = True
    chain.insert(msg['val'])
    # remove everything in proposed block and transaction queue
    transaction_queue = []
    proposed_block = None
    print(chain)
    print('Chain updated. All transactions in queue are discarded.')
    # if msg['val'] != proposed_block:
    #     print('Other node appended to the block chain. Local transaction queue deleted.')        
    #     transaction_queue = []

def on_accept(self, msg):
    # verify blockchain
    block = msg['val']
    return block.previous_hash == chain.head.hash \
        and apply_transactions(chain.balance, block.transactions) \
        and int(block.hash[-1],16) < 4

def on_offer(self, pid):
    global chain
    send_msg(pid, {'type':'chain-reply', 'chain': chain})



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
    load()
    paxos.on_decision = on_decision
    paxos.on_inconsistent_depth = on_inconsistent_depth
    paxos.on_accept = on_accept
    paxos.on_offer = on_offer

    # Console thread
    while(True):
        cmd_arg = input().split()
        task = {
            'type': 'console',
            'args': cmd_arg
        }
        task_queue.put(task)
        if len(cmd_arg) > 0 and cmd_arg[0] == 'failProcess':
            break

    print("stop tracking keyboard input, trying to join processer_thread")
    processer_thread_stop_signal = True
    processer_thread.join()
    print("trying to join listen_thread")
    listener_thread_stop_signal = True
    listener_thread.join()
    exit()