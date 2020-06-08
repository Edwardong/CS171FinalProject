import datetime


class Transaction(object):
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return str(self.sender) + " pays " + str(self.receiver) + " " + str(self.amount) + " in " + str(self.timestamp)
