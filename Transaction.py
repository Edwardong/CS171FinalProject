import datetime


class Transaction(object):
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return str(self.sender) + " pays " + str(self.receiver) + " " + str(self.amount) + " in " + str(self.timestamp)


def apply_transactions(balance, transactions):
    """ apply transactions: Transaction[] on balance: int[] """
    for t in transactions:
        balance[t.sender] -= t.amount
        balance[t.receiver] += t.amount
        if balance[t.sender] < 0:
            return False
    return balance
