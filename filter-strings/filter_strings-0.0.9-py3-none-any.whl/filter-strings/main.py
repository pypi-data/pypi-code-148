import argparse
import os
import re

def parse_args():
    parser = argparse.ArgumentParser(description='Filter strings from a file based on regex patterns.')
    parser.add_argument('--input_file', required=True, help='The input file to be filtered')
    parser.add_argument('--regex', required=True, nargs='+', help='The regex patterns to filter by')
    return parser.parse_args()

def filter_strings(input_file, regex):
    result_folder = 'result'
    filtered_file = os.path.join(result_folder, 'filtered.txt')

    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    with open(input_file, 'r') as input_f, open(filtered_file, 'w') as output_f:
        for line in input_f:
            match = any(re.search(r, line) for r in regex)
            if not match:
                output_f.write(line)

if __name__ == '__main__':
    args = parse_args()
    try:
        filter_strings(args.input_file, args.regex)
    except Exception as e:
        print(f'An error occurred: {e}')
