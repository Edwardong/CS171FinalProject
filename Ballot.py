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