import csv
import yaml
import sys
from shutil import copyfile
from importlib import import_module

classifiers = {
    'cibc': None,
    'chase': None
}

for c in classifiers.keys():
    m = import_module('classifysun.classifiers.{}'.format(c))
    classifiers[c] = m

def csv_rows(filename, *r_opts):
    res = []
    with open(filename, 'r') as f:
        r = csv.reader(f, *r_opts)
        for row in r:
            res.append(row)
    return res

def parse_yaml(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

def write_csv(rows, o_file, *w_opts):
    with open(o_file, 'w') as f:
        w = csv.writer(f, *w_opts)
        for row in rows:
            print(row)
            w.writerow(row)

def write_yaml(yml, filename):
    copyfile(filename, ".{}.backup".format(filename))
    with open(filename, 'w') as f:
        f.write(yaml.dump(yml, default_flow_style=False))

def run_classifier(input_file, output_file, rules_file, classifier):
    #TODO catch interrupt

    c = classifier.lower()
    if c in classifiers:
        classifier = classifiers[c].Classifier
    else:
        print("{} is not a recognized classifier".format(classifier))
        sys.exit(1)

    rules = parse_yaml(rules_file)
    classifier = classifier(rules)
    rows = csv_rows(input_file)
    #TODO fix this garbage
    if "Transaction Date" in rows[0][0]:
        rows = rows[1:]
    transactions = classifier.transactions(rows)
    res = []
    for r in transactions:
        res.append([r.date, r.merchant, r.category, r.amount])
    write_csv(res, output_file)
    write_yaml(rules, rules_file)
    return
