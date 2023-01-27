from zlib import decompress
from msgpack import unpackb
from sys import exit, argv
from re import sub, match, compile
from pathlib import Path

mac_db = None
compiled_mac = compile('[^a-fA-F0-9]')


class NotValidMAC(Exception):
    pass


def load_mac_db():
     try:
         with open(Path(__file__).parent.joinpath('mac_db.dump'), 'rb') as mac_db_file:
             zipped_mac_db = mac_db_file.read()
             packed_mac_db = decompress(zipped_mac_db)
             globals()['mac_db'] = unpackb(packed_mac_db, strict_map_key=False) 
     except Exception as e:
         exit(f'error while loading mac_db {e}')
  

def sanitize_mac(mac_addr):
    stripped_mac = sub(compiled_mac, '', mac_addr)
    if len(stripped_mac) != 12:
        raise NotValidMAC()
    return stripped_mac.upper()


def mac_lookup(mac_addr: str) -> str:
   """
   Takes mac_addr, case-insensitive string in any format
   returns vendor string if found, "MAC Not Registered" otherwise)
   throws NotValidMAC exception if mac address is not valid 
   """
   sane_mac = sanitize_mac(mac_addr)
   sane_mac_prefix = sane_mac[0:6]
   if not globals()['mac_db']:
       load_mac_db()
   return mac_db.get(int(sane_mac_prefix, 16), b"MAC Not Registered").decode('utf-8')  


if __name__ == "__main__":
    if len(argv) < 2:
        exit("Usage: {} [mac-address1 mac-address2 mac-address3]".format(argv[0]))   
    else:
        for i in range(1, len(argv)):
            print(argv[i], mac_lookup(argv[i]))
