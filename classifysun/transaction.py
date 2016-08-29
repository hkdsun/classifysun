class Transaction(object):
    def __init__(self, date, amount, merchant, category):
        #TODO add account
        self.date = date
        self.amount = amount
        self.merchant = merchant
        self.category = category

    def __str__(self):
        return "[{}: {:8.2f} $ on {} at {}]".format(
            self.category,
            self.amount,
            self.date,
            self.merchant
        )
