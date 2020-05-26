import hashlib, pickle
from prettytable import PrettyTable


def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

class BlockNode(object):
    def __init__(self, test_int = 0):
        self.__prev = None
        self.__nonce = None
        self.__previous_hash = None
        self.__transactions = []
        #self.__base_hash_val = None #hash value of transactions, used for updating Nonce
        #self.__prev_hash = ''
        self.test_int = test_int
        self.payload = {
            "Transactions": self.__transactions,
            "Nonce": self.__nonce
        }

    def add_trans(self, trans):
        self.__transactions.append(trans)

    # def set_base_hash(self):
    #     self.__base_hash_val = hashlib.sha256(self.payload).hexdigest()

    def find_nonce(self):
        self.__nonce = "0"
        attempt = hashlib.sha256(self.payload).hexdigest()
        while int(attempt[-1],16) > 4:
            self.__nonce = hex(int(self.__nonce,16) + 1)
            attempt = hashlib.sha256(self.payload).hexdigest()
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

    def __repr__(self):
        #print(self.test_int)
        table = PrettyTable()
        table.align = "c"
        table.add_column("Transactions",self.__transactions)
        nonce_list = [self.__nonce]
        while len(nonce_list) < len(self.__transactions):
            nonce_list.append("")
        table.add_column("Nonce", nonce_list)
        hash_list = list(chunkstring(self.__previous_hash, int(64/len(self.__transactions))+1))
        table.add_column("Hash", hash_list)
        #msg = "Transactions: {}, Nonce: {}, Hash: {}".format(self.__transactions, self.__nonce, self.__previous_hash)
        return table.get_string()
