class Ballot(object):
    def __init__(self, seq_num=0, proc_id=0, depth=0):
        self.seq_num = seq_num
        self.proc_id = proc_id
        self.depth = depth

    def __lt__(self, other):
        if self.depth == other.depth:
            if self.seq_num == other.seq_num:
                return self.proc_id < other.proc_id
            else:
                return self.seq_num < other.seq_num
        else:
            return self.depth < other.depth

    def __eq__(self, other):
        return self.seq_num == other.seq_num and self.proc_id == other.proc_id and self.depth == other.depth

    def next(self):
        """ next ballot number (seq_num + 1) """
        return Ballot(self.seq_num + 1, self.proc_id)

    def update(self, other):
        """ update so that >= other's seq_num """
        if self.seq_num < other.seq_num:
            self.seq_num = other.seq_num
        return self

    def __str__(self):
        return '< ' + str(self.seq_num) + ' ' + str(self.proc_id) + ' ' + str(self.depth) + ' >'
