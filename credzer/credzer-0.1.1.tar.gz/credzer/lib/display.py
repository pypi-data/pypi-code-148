import json
from tinydb import TinyDB, Query

def display(db,arg):
    db=TinyDB(db)
    if(arg=='cleartext'):
        Entry = Query()
        entries=db.search(Entry.clear_password!="")
        for entry in entries:
            prettyPrint(entry)

def prettyPrint(entry):
    print( "%s\%s:%s"%(entry['domain'],entry['username'],entry['clear_password']))

def displayStats(db):
    db=TinyDB(db)
    entries=db.all()
    clear_password=0
    total_entries=0
    for entry in entries:
        if(entry['clear_password'] and entry['clear_password']!=""):
            clear_password+=1
        total_entries+=1
    print("[Entries] %s\n[ClearText] %s\n[Percent Clear] %s"%(total_entries,clear_password,int((clear_password/total_entries)*100)))