import hashlib, pickle


class BlockChain(object):
    def __init__(self, head=None):
        self.__head = head
        #self.__depth = self.find_depth()

    def find_depth(self):
        if self.__head is None:
            return 0
        index = 1
        dummy = self.__head
        while dummy.prev is not None:
            dummy = dummy.prev
            index += 1
        return index

    def insert(self, block):
        block.prev = self.head
        if block.prev is None:
            block.previous_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        else:
            payload = {
                "Transaction": block.prev.transactions,
                "Nonce": block.prev.nonce,
                "Hash": block.prev.previous_hash
            }
            block.previous_hash = hashlib.sha256(pickle.dumps(payload)).hexdigest()
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

    @property
    def depth(self):
        return self.find_depth()

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node))
            node = node.prev
        nodes.append("NULL")
        nodes.reverse()
        return " \n ↑ \n".join(nodes)

    # def save(self, pid):
    #     # TODO:
    #     pass
    #
    # def load(self):
    #     # TODO:
    #     pass
