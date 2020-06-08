import hashlib, pickle
from Transaction import Transaction, apply_transactions

class BlockChain(object):
    def __init__(self, head=None, n=1):
        """ Init a blockchain with n nodes """
        self.__head = head
        self.N = n
        self.depth = 0 # it's okay not to encapsulate depth here cuz we have to maintain 'balance' anyhow so maintaining depth is just by-the-way
        self.balance = [100.0] * n


    def verify_transaction(self, transaction):
        return self.balance[transaction.sender] >= transaction.amount


    def verify_insert_hash(self, block):
        # TODO:
        pass


    def insert(self, block):
        """ Insert a block. Update balance and depth """
        # update balance
        if apply_transactions(self.balance, block.transactions) == False:
            print('ERROR Cannot insert block: negative balance.')
            return
        # attach block
        block.prev = self.head
        self.head = block
        # update depth
        self.depth += 1


    def rewrite(self, chain):
        """ Rewrite the whole chain and update balance and depth """
        self.__head = chain.head
        # TODO: put chain to self.head
        self.depth = 0
        self.balance = [100.0] * self.N
        iter_node = self.head
        while iter_node is not None:
            if apply_transactions(self.balance, [iter_node.transactions]) == False:
                print('ERROR Cannot insert block: negative balance.')
            self.depth += 1
            iter_node = iter_node.prev


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

    # @property
    # def depth(self):
    #     return self.find_depth()

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node))
            node = node.prev
        nodes.append("NULL")
        nodes.reverse()
        return " \n ↑ \n".join(nodes)
