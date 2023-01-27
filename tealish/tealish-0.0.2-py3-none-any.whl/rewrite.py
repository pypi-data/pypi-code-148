from collections import defaultdict
import json
from operator import index
import re
import sys
from tealish import TealishCompiler

filename = sys.argv[1]
lines = open(filename).readlines()

compiler = TealishCompiler(lines)
compiler.parse()
compiler.process()

new_tealish = compiler.nodes[0].tealish(formatter)


if len(sys.argv) == 2:
    output_filename = filename
else:
    output_filename = sys.argv[2]

if output_filename == "-":
    sys.stdout.write(new_tealish)
else:
    with open(output_filename, "w") as f:
        f.write(new_tealish)
