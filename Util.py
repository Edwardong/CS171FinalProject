import hashlib, pickle

P1PORT = 5001
P2PORT = 5002
P3PORT = 5003
P4PORT = 5004
P5PORT = 5005
PORTS = [P1PORT, P2PORT, P3PORT, P4PORT, P5PORT]
N = 5 # number of processes

NETWORK_PORT = 5006


class Transaction(object):
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount


class BlockChain(object):
    def __init__(self, head=None):
        self.__head = head

    def insert(self, block):
        block.prev = self.head
        self.head = block

    def discard_last(self):
        if self.head is not None:
            self.head = self.head.prev

    def discard_last_and_insert_new(self,block):
        self.discard_last()
        self.insert(block)

    @property
    def head(self):
        return self.__head

    @head.setter
    def head(self, new_head):
        self.__head = new_head

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.test_int))
            node = node.prev
        nodes.append("NULL")
        nodes.reverse()
        return " <- ".join(nodes)


class BlockNode(object):
    def __init__(self, test_int = 0):
        self.__prev = None
        self.Nonce = None
        self.previous_hash = None
        self.__transaction = []
        self.__base_hash_val = '' #hash value of transactions, used for updating Nonce
        self.__prev_hash = ''
        self.test_int = test_int

    def add_trans(self, trans):
        self.transaction.append(trans)

    def set_base_hash(self):
        self.__base_hash_val = hashlib.sha256(pickle.dumps(self.transaction)).hexdigest()

    def find_Nonce(self):
        return

    @property
    def base_hash_val(self):
        return self.__base_hash_val

    @property
    def prev(self):
        return self.__prev
    @prev.setter
    def prev(self, new_prev):
        self.__prev = new_prev


class Ballot(object):
    def __init__(self, seq_num=0, proc_id=0,depth=0):
        self.__seq_num = seq_num
        self.__proc_id = proc_id
        self.__depth = depth

    def __lt__(self, other):
        if self.__seq_num == other.seq_num:
            return self.__proc_id < other.proc_id
        else:
            return self.__seq_num < other.seq_num

    @property
    def seq_num(self):
        return self.__seq_num

    @seq_num.setter
    def seq_num(self, new_seq_num):
        self.__seq_num = new_seq_num

    @property
    def depth(self):
        return self.depth

    @depth.setter
    def depth(self, depth):
        self.depth = depth