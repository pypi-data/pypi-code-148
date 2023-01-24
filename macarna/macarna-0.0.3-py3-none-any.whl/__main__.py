from .mac_lookup import mac_lookup
from sys import argv

if __name__ == "__main__":
    if len(argv) < 2:
        exit("Usage: {} [mac-address1 mac-address2 mac-address3]".format(argv[0]))
    else:
        for i in range(1, len(argv)):
            print(argv[i], mac_lookup(argv[i]))
