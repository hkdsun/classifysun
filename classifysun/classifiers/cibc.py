from .classifier import TransactionClassifier

class Classifier(TransactionClassifier):
    def parse_amount(self, row):
        if row[2]:
            return float('-' + row[2])
        else:
            return float('+' + row[3])

    def parse_row(self, row):
        date = row[0]
        merchant = row[1]
        amount = self.parse_amount(row)
        return (date, amount, merchant)

