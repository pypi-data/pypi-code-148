

"""
This code snippet uses the argparse module to add a new command-line argument to the script. The --replace or -r flag can be passed in when running the script and this will replace multiple whitespaces with a single space in the contents of the file using the re module's sub function.

Note that this will replace all the spaces in the file, not only the trailing spaces.
"""

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--replace", help="Replace multiple whitespaces with a single space", action="store_true")
args = parser.parse_args()

#...
    with open(file, "r") as f:
        contents = f.read()
        if args.replace:
            contents = re.sub(r'\s+', ' ', contents)
    with open(file, "w") as f:
        f.write(contents)

"""

      This code snippet uses the lstrip() method to remove any whitespace characters at the beginning of each line, and the startswith() method to check if a line starts with a '#' character, if so it will not process the line. If the --replace or -r flag is passed in when running the script, this will replace multiple whitespaces with a single space in the contents of the file using the re module's sub function, but only if the line does not start with a '#' character.
"""

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--replace", help="Replace multiple whitespaces with a single space", action="store_true")
args = parser.parse_args()

#...
    with open(file, "r") as f:
        contents = f.readlines()
    with open(file, "w") as f:
        for line in contents:
            if args.replace and not line.lstrip().startswith('#'):
                line = re.sub(r'\s+', ' ', line.rstrip())
            f.write(line)




real	0m7,724s
user	0m6,005s
sys	0m1,205s
