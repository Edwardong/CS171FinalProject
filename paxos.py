from network import PORTS, N, PIDS, MAJORITY, send_msg, listener
from Ballot import Ballot


class Paxos:

    depth = 0
    my_pid = None
    my_proposal_phase = 'PREPARE'
    my_proposal_bal = None
    my_proposal_val = None
    my_proposal_promises = []
    my_proposal_accept = 0
    latest_bal = None
    accepted_bal = None
    accepted_val = None

    def __init__(self, pid):
        self.my_pid = pid
        self.latest_bal = Ballot(0, 0, 0)
        self.accepted_bal = Ballot(0, 0, 0)
        self.accepted_val = None

    def set_proposel(self, value):
        self.my_proposal_phase = 'PREPARE'
        self.my_proposal_bal = Ballot(self.latest_bal.seq_num + 1, self.my_pid, self.depth) 
        # latest_bal should update immediately afterwards
        self.my_proposal_val = value
        self.my_proposal_promises = []
        self.my_proposal_accept = 0
        
        
    def send_prepare(self):
        prepare_msg = {
            'type': 'msg-prepare',
            'bal': self.my_proposal_bal
        }
        for p in range(N):
            if p != self.my_pid:
                send_msg(p, prepare_msg)
            else:
                self.recv_prepare(prepare_msg)
                

    def recv_prepare(self, msg):
        print("recv-prepare")
        # only promise a prepare msg if latest
        if msg['bal'] > self.latest_bal:
            sender = msg['bal'].proc_id
            promise_msg = {
                'type': 'msg-promise',
                'accepted_bal': self.accepted_bal,
                'accepted_val': self.accepted_val
            }
            if sender != self.my_pid:
                send_msg(sender, promise_msg)
            else:
                self.recv_promise(promise_msg)
            self.latest_bal = msg['bal']


    def recv_promise(self, msg):
        bal = msg['accepted_bal']
        val = msg['accepted_val']
        self.my_proposal_promises.append((bal, val))
        # if majority, move to ACCEPT phase
        print(self.my_proposal_promises)
        if self.my_proposal_phase == 'PREPARE' and len(self.my_proposal_promises) >= MAJORITY:
            self.my_proposal_phase = 'ACCEPT'
            # decide value
            max_bal = Ballot(0,0,0)
            for bal, val in self.my_proposal_promises:
                if val is not None and bal > max_bal:
                    self.my_proposal_val = val
            # send 'accept' messages
            for p in PIDS:
                accept_msg = {
                    'type': 'msg-accept',
                    'bal': self.my_proposal_bal,
                    'val': self.my_proposal_val
                }
                if p != self.my_pid:
                    send_msg(p, accept_msg)
                else:
                    self.recv_accept(accept_msg)
    
    
    def recv_accept(self, msg):
        if not msg['bal'] < self.latest_bal:
            self.accepted_bal = msg['bal']
            self.accepted_val = msg['val']
            self.latest_bal = msg['bal']
            # reply "accepted"
            sender = msg['bal'].proc_id
            accepted_msg = {
                'type': 'msg-accepted',
            }
            if sender != self.my_pid:
                send_msg(sender, accepted_msg)
            else:
                self.recv_accepted(accepted_msg)


    def recv_accepted(self, msg):
        self.my_proposal_accept += 1
        # majority
        if self.my_proposal_phase == 'ACCEPT' and self.my_proposal_accept >= MAJORITY:
            self.my_proposal_phase = 'DECISION'
            for p in PIDS:
                decision_msg = {
                    'type': 'msg-decision',
                    'bal': self.my_proposal_bal,
                    'val': self.my_proposal_val
                }
                if p != self.my_pid:
                    send_msg(p, decision_msg)
                else:
                    self.recv_decision(decision_msg)
     

    def recv_decision(self, msg):
        print('recv_decision')
        print(msg['bal'])
        print(msg['val'])
        self.update_depth()


    def update_depth(self):
        """ start paxos for new depth: reset vars and """
        self.depth += 1
        latest_bal = None
        accepted_bal = None
        accepted_val = None


    def inconsistent_depth(self, depth):
        if depth < self.depth:
            # ignore this
            return True
        elif depth > self.depth:
            # TODO: triggers a force update
            return True
        else:
            return False
        
        
    def print(self):
        print('my_pid:', self.my_pid)
        print('my_proposal_bal: ', self.my_proposal_bal)
        print('my_proposal_val: ', self.my_proposal_val)
        print('my_proposal_promises: ', self.my_proposal_promises)
        print('my_proposal_accept: ', self.my_proposal_accept)
        print('latest_bal:', self.latest_bal)
