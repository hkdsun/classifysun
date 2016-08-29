import argparse
from classifysun import cli

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
        help="path to the input file")
    ap.add_argument("-o", "--output", default='result.csv',
        help="path to the ouput file (default result.csv)")
    ap.add_argument("-c", "--rules", default='rules.yaml',
        help="path to the rules file (default rules.yaml)")
    ap.add_argument("-t", "--target", required=True,
        help="classifier type <CIBC|Chase>")

    args = vars(ap.parse_args())

    cli.run_classifier(args['input'], args['output'], args['rules'], args['target'])
