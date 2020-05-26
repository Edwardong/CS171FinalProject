import hashlib, pickle

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

class BlockNode:
    def __init__(self, val, prev=None):
        self.val = val
        self.prev = prev
        self.Nonce = None
        self.previous_hash = None
        self.transaction = []
        self.base_hash_val = '' #hash value of transactions, used for updating Nonce
        self.prev_hash = ''

    def add_trans(self, trans):
        self.transaction.append(trans)

    def set_base_hash(self):
        self.base_hash_val = hashlib.sha256(pickle.dumps(self.transaction)).hexdigest()

    def find_Nonce(self):
        return