'''
Zone file management.

Copyright: Copyright 2021-2023 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

def main():

    zone_file = sys.argv[1]
    action = sys.argv[2]

    if action == 'add-acme-challenge':
        domain = sys.argv[3]
        key_digest = sys.argv[4]
        return action_add_acme_challenge(zone_file, domain, key_digest)
    elif action == 'del-acme-challenge':
        domain = sys.argv[3]
        key_digest = sys.argv[4]
        return action_delete_acme_challenge(zone_file, domain, key_digest)
    elif action == 'update-serial':
        return action_update_zone_serial(zone_file)
    else:
        print(f'Wrong action: {action}', file=sys.stderr)
        return 1

def action_add_acme_challenge(zone_file, domain, key_digest):
    content = load_zone_file(zone_file)
    if not content:
        return 1
    content = update_zone_serial(content)
    if not content:
        return 1
    resource_record = make_acme_challenge_rr(domain, key_digest)
    save_zone_file(zone_file, f'{content}\n{resource_record}\n')
    return 0

def action_delete_acme_challenge(zone_file, domain, key_digest):
    content = load_zone_file(zone_file)
    if not content:
        return 1
    content = update_zone_serial(content)
    if not content:
        return 1
    resource_record = make_acme_challenge_rr(domain, key_digest)
    content = content.replace(resource_record, '').rstrip()
    save_zone_file(zone_file, content)
    return 0

def action_update_zone_serial(zone_file):
    '''
    Update zone serial number using current timestamp.
    '''
    content = load_zone_file(zone_file)
    if not content:
        return 1
    content = update_zone_serial(content)
    if not content:
        return 1
    save_zone_file(zone_file, content)
    return 0

def load_zone_file(zone_file):
    if os.path.exists(zone_file):
        with open(zone_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f'File does not exist: {zone_file}', file=sys.stderr)
        return None

def save_zone_file(zone_file, content):
    statinfo = os.stat(zone_file)
    with atomic_write(zone_file, mode='w', encoding='utf-8', overwrite=True) as f:
        f.write(content)
    os.chmod(zone_file, stat.S_IMODE(statinfo.st_mode))

def make_acme_challenge_rr(domain, key_digest):
    idna_domain = idna.encode(domain).decode('ascii')
    return f'_acme-challenge.{idna_domain}. 300 IN TXT "{key_digest}"'

def update_zone_serial(content):
    matchobj = re.search(r'\n\s+(\d+)(\s+; SERIAL\n)', content)
    if matchobj:
        return content[:matchobj.start(1)] + str(int(time.time())) + content[matchobj.start(2):]
    else:
        print('Cannot update serial number', file=sys.stderr)
        return None

#-----------------------------------------------------------------------------------
# Dependencies

import os
import re
import stat
import sys
import time

from atomicwrites import atomic_write
import idna

#-----------------------------------------------------------------------------------
# Run main

if __name__ == '__main__':
    main()
