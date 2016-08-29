# Classifysun

Classifysun is a utility for classifying bank transactions based on their description. It currently requires initial user training to build a configuration file, `rules.yaml`. This configuration file contains regular expressions or substrings that will match against a CSV file.

### Support
Currently supported bank statements (export CSV from online account) are:

  * Canadian Imperial Bank of Commerce (CIBC)
  * Chase credit cards

Adding support for your own bank (PRs welcome) is also very easy:

```python
# cli.py
classifiers = {
    'other_bank': None,
    'new_bank': None
}

# classifiers/new_bank.py
from .classifier import TransactionClassifier

class Classifier(TransactionClassifier):
	def transform(self, amount):
    	return amount**2 # idk why you would do this
    
    def parse_row(self, row):
    	# row is a row of the CSV file
        date = row[0] # pick the column
        amount = self.transform(row[1]) # do any necessary transformations
        merchant = row[2]
        return (date, amount, merchant) # return this tuple
```

### Usage
Clone this repo
```
git clone https://repourl
```
Run `main.py` with appropriate arguments.
```
$ python main.py -h

usage: main.py [-h] -i INPUT [-o OUTPUT] [-c RULES] -t TARGET

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to the input file
  -o OUTPUT, --output OUTPUT
                        path to the ouput file (default result.csv)
  -c RULES, --rules RULES
                        path to the rules file (default rules.yaml)
  -t TARGET, --target TARGET
                        classifier type <CIBC|Chase>
```

### Status
Currently working on:

 * Category suggestion engine based on previously seen keywords
