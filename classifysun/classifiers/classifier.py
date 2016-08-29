from classifysun.transaction import Transaction
import re

class TransactionClassifier(object):
    def __init__(self, rules):
        self.rules = rules

    def parse_row(self, row):
        # rtype: (date, amount, merchant)
        raise NotImplementedError

    def capitalize_word(self, w):
        return w[:1].upper() + w[1:].lower()

    def pretty_title(self, s):
        return " ".join(map(self.capitalize_word, s.strip().split()))

    def save_rules(self):
        #TODO eliminate this
        write_yaml(self.rules, "rules.yaml")

    def menu_option(self, menu):
        keys = sorted(menu.keys())
        for i, m in enumerate(keys):
            print("  [{}]. {}".format(i, m))

        resp = None
        while True:
            try:
                resp = int(input('--> '))
            except ValueError:
                print("Couldn't recognize that, try again..")
                continue
            if resp < 0 or resp >= len(keys):
                print("That's not an option, try again..")
            else:
                break
        return keys[resp]

    def transactions(self, rows):
        res = []
        for i, row in enumerate(rows):
            print("{}/{}".format(i + 1, len(rows)))
            res.append(self.classify_row(row))
        return res

    def classify_row(self, row):
        row = self.parse_row(row)
        date = row[0]
        amount = row[1]
        merchant = self.pretty_title(row[2])
        row = (date, amount, merchant)
        category = self.categorize_merchant(row)
        return Transaction(date, amount, merchant, category)

    def matches_rule(self, merchant, rule):
        if re.match('\w+', rule):
            if rule.lower() in merchant.lower():
                return True
            else:
                return False
        else:
            matched = False
            try:
                matched = re.match(rule.lower(), merchant.lower())
            except re.error:
                print("WARNING: Malformed rule found: {}".format(rule))
            return matched

    def new_rule(self, rep, merch):
        print("Pick category")
        categories = dict(self.rules)
        categories["_new_"] = None
        category = self.menu_option(categories)
        if category == "_new_":
            print("Enter category name:")
            category = input("{} --> ".format(merch))
        print("Enter new rule (regex/substr) for {}:".format(category))
        rule = input("(enter to skip) ---> ")
        if rule:
            if category in self.rules:
                if rule not in self.rules[category]:
                    self.rules[category].append(rule)
                    self.save_rules()
            else:
                self.rules[category] = [rule]
                self.save_rules()
        return category

    def ask_user(self, row, options):
        date, amount, merchant = row
        rep = "{}: {} on {}".format(merchant, amount, date)

        if not options:
            print("No rules matched: {}".format(rep))
            return self.new_rule(rep, merchant)
        else:
            print("Multiple rules matched: {}".format(rep))
            menu = {}
            menu["_other_"] = None
            for opt in options:
                menu[opt] = None
            option = self.menu_option(menu)
            if option == "_other_":
                return self.new_rule(rep)
            return option

    def categorize_merchant(self, row):
        res = []
        for category in self.rules:
            for rule in self.rules[category]:
                if self.matches_rule(row[2], rule):
                    res.append(category)
                    break
        if len(res) == 0:
            return self.ask_user(row, None)
        elif len(res) == 1:
            return res[0]
        else:
            return self.ask_user(row, res)
