import hashlib, pickle
from prettytable import PrettyTable


def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

class BlockNode(object):
    def __init__(self):
        self.__nonce = None
        self.__transactions = []
        self.__previous_hash = None
        self.__prev = None
        #self.__base_hash_val = None #hash value of transactions, used for updating Nonce
        #self.__prev_hash = ''


    def add_trans(self, trans):
        self.__transactions.append(trans)


    @property
    def hash(self):
        payload = {
            "Transaction": self.transactions,
            "Nonce": self.nonce,
            "Previous Hash": self.previous_hash
        }
        return hashlib.sha256(pickle.dumps(payload)).hexdigest()

    # def set_base_hash(self):
    #     self.__base_hash_val = hashlib.sha256(self.payload).hexdigest()

        

    def find_nonce(self):
        self.__nonce = "0"
        while int(self.hash[-1],16) > 4:
            self.__nonce = hex(int(self.__nonce,16) + 1)
        return


    # @property
    # def base_hash_val(self):
    #     return self.__base_hash_val
    @property
    def nonce(self):
        return self.__nonce

    @property
    def previous_hash(self):
        return self.__previous_hash

    @previous_hash.setter
    def previous_hash(self, new_previous_hash):
        self.__previous_hash = new_previous_hash

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, new_prev):
        self.__prev = new_prev

    @property
    def transactions(self):
        return self.__transactions

    # @transactions.setter
    # def transactions(self, new_trans):
    #     self.__transactions = new_trans


    def __eq__(self, other):
        if len(self.transactions) != len(other.transactions):
            return False
        for i in len(self.transactions):
            if self.transactions[i] != other.transactions[i]:
                return False
        if self.nonce != other.nonce:
            return False
        if self.previous_hash != other.previous_hash:
            return False
        return True


    def __repr__(self):
        
        table = PrettyTable()
        table.align = "c"
        table.add_column("Transactions",self.__transactions)
        nonce_list = [self.__nonce]
        while len(nonce_list) < len(self.__transactions):
            nonce_list.append("")
        table.add_column("Nonce", nonce_list)
        hash_list = list(chunkstring(self.__previous_hash, int(64/len(self.__transactions))+1))
        table.add_column("HashPointer", hash_list)
        #msg = "Transactions: {}, Nonce: {}, Hash: {}".format(self.__transactions, self.__nonce, self.__previous_hash)
        return table.get_string()


def createBlockNode(transactions, previous_block):
    """ Create a blocknode based on $transactions$ and $previous_block$, auto compute nonce """
    b = BlockNode()
    # b.transactions = transactions
    for t in transactions:
        b.add_trans(t)
    b.previous_hash = previous_block.hash if previous_block is not None else '0'*64
    b.find_nonce()
    return b


