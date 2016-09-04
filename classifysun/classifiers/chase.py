from .classifier import TransactionClassifier
import re

class Classifier(TransactionClassifier):
    def parse_amount(self, row):
        flag = row[8]
        amount = re.match('.*\$([0-9\.]+).*', row[2]).group(1)
        sign = '+'
        if flag == 'D':
            sign = '-'
        elif flag == 'C':
            pass
        else:
            raise Exception("Flag of type \"{}\" not recongnized".format(flag))
        return float(sign + amount)

    def parse_row(self, row):
        date = row[0]
        amount = self.parse_amount(row)
        merchant = row[3]
        return (date, amount, merchant)
