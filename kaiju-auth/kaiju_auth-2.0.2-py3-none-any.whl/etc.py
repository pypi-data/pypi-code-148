"""
This module loads a list of weak passwords from the file and stores it in memory.
The list is used by an auth service when registering a new user.

`weak_passwords` - a set of weak passwords (see passwords.csv)

"""

import csv
import pathlib

__all__ = ['WEAK_PASSWORDS']

WEAK_PASSWORDS = pathlib.Path(__file__).resolve().parent.parent / 'passwords.csv'

with open(WEAK_PASSWORDS, 'r') as f:
    reader = csv.reader(f)
    weak_passwords = []
    for row in reader:
        password = row[0].strip()
        if password:
            weak_passwords.extend([
                password,
                password.capitalize(),
                password.upper(),
                password.lower()
            ])
    WEAK_PASSWORDS = frozenset(weak_passwords)
    del reader

del f
