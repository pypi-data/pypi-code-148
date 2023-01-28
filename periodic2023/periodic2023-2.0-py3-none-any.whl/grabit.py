#!/usr/bin/env python3
import argparse
import collections
import json
import logging
from periodic import _logger

class Grabber:

    def __enter__(self):
        self.read_json()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read_json(self):
        attrs = collections.defaultdict(int)
        with open ('PeriodicTableJSON.json') as f:
            data = json.load(f)
        for e in data['elements']:
            for d in e.keys():
                attrs[d] += 1
        for a in sorted(attrs):
            print(f"{a} {attrs[a]}")
        example = data['elements'][0]
        for k,v in example.items():
            print(f"{k} {type(v)}")





def main():
    logging.basicConfig()
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', default='WARN', help="Python logging level")

    args = parser.parse_args()
    _logger.setLevel(getattr(logging,args.loglevel))
    with Grabber() as grb:
        print('x')


if __name__ == "__main__":
    main()
