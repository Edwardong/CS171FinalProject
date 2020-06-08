import hashlib, pickle


class BlockChain(object):
    def __init__(self, head=None, n=1):
        """ Init a blockchain with n nodes """
        self.__head = head
        self.N = n
        self.depth = 0
        self.balance = [100.0] * n


    def verify_transaction(self, transaction):
        return self.balance[transaction.sender] >= transaction.amount


    def insert(self, block):
        """ Insert a block. Update balance and depth """
        # attach block
        block.prev = self.head
        if block.prev is None:
            block.previous_hash = '0' * 64
        else:
            block.previous_hash = block.prev.hash()

        self.head = block
        # update balance
        for trans in block.transactions:
            self.balance[trans.sender] -= trans.amount
            self.balance[trans.receiver] += trans.amount
            if trans.sender < 0:
                print('ERROR in blockchain balance')
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
            for trans in iter_node.transactions:
                balance[trans.sender] -= trans.amount
                balance[trans.receiver] += trans.amount
                if trans.sender < 0:
                    print('ERROR in blockchain balance')
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

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node))
            node = node.prev
        nodes.append("NULL")
        nodes.reverse()
        return " \n ↑ \n".join(nodes)
