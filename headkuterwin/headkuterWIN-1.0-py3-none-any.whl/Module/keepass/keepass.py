"""
    Title: HeadKuarter
    Module Name: keepaass
    Language: Python
    Date Created: 15-05-2022
    Date Modified: 25-07-2022
    Description:
        ###############################################################
        ##  generate the database using pykeepass to store data      ## 
        ###############################################################
 """
from pykeepass import PyKeePass,create_database
import pyperclip

def createDb(locker_name,pwd):
    locker_name = locker_name.split(".")
    fname = locker_name[0]+'.kdbx'
    return create_database (fname, password=pwd, keyfile=None, transformed_key=None)
class locker:
    kdb=''
    def __init__(self,locker_name,pwd):
        self.db = locker_name+'.kdbx'
        self.pwd = pwd
        locker.kdb = PyKeePass(self.db,self.pwd)

    def createEntryinGrp(self):
        length = len(self)
        if length==3:
            grp = self[2]
            gname = input("Enter the domain name:- ")
            uname= input("Enter the username of the desired entry:- ")
            pwd = input("Enter the password:-  ")
        elif length==4:
            grp = self[2]
            gname = self[3]
            uname= input("Enter the username of the desired entry:- ")
            pwd = input("Enter the password:-  ")
        elif length==5:
            grp = self[2]
            gname = self[3]
            uname = self[4]
            pwd = input("Enter the password:-  ")
        elif length==6:
            grp = self[2]
            gname = self[3]
            uname = self[4]
            pwd = self[5]
        else:
            grp = input("Enter the group name:- ")
            gname = input("Enter the Domain name:- ")
            uname= input("Enter the username of the desired entry:- ")
            pwd = input("Enter the password:-  ")
        group =locker.kdb.find_groups(name=grp, first=True)
        if locker.kdb.find_entries(title=gname, first=True):
            return "domain alreay exist"
        if group:
            locker.kdb.add_entry(group, gname, uname, pwd)
        else:
            check = input("Group is not exist! you want to create a new group [y/n]:- ")
            if check=='y' or check=='Y':
                locker.kdb.add_group(locker.kdb.root_group, grp)
                group =locker.kdb.find_groups(name=grp, first=True)
                locker.kdb.add_entry(group, gname, uname, pwd)
            else:
                return "Entry is not added!!"
        locker.kdb.save()
        return "Entry is added successfully!!"

    def adEntry(self):
        length = len(self)
        if '@grp' in self:
            if '@grp' == self[1]:
                return locker.createEntryinGrp(self)
            else: return "@grp is must be at 2nd position"
        elif length>4:
            return "@grp is required at 2nd position if there is 5 argument"
        else:
            if length==2:
                gname = self[1]
                uname = input("Enter the username of the desired entry:- ")
                pwd = input("Enter the password:-  ")
            elif length==3:
                gname = self[1]
                uname = self[2]
                pwd = input("Enter the password:-  ")
            elif length==4:
                gname = self[1]
                uname = self[2]
                pwd = self[3]
            else:
                gname = input("Enter entry doamin name:- ")
                uname= input("Enter the username of the desired entry:- ")
                pwd = input("Enter the password:-  ")
            grp = locker.kdb.find_entries(title=gname, first=True)
            if grp:
                return "Domain already exist!!"
        locker.kdb.add_entry(locker.kdb.root_group, gname, uname, pwd)
        locker.kdb.save()
        return "Entry is added successfully!!"
        
    def retrivepass(self):
        if len(self)>1:
            grp_name = self[1]
        else:
            grp_name = input("Enter the name of Domain:- ")
        grp = locker.kdb.find_entries(title=grp_name, first=True)
        if grp:

            if len(self)>2:
                if self[2]:
                    pyperclip.copy(grp.password)
                    return "Password is copied to clipboard!"
                return "invalid command"
            return grp.password
        return "Domain not found"

    def delete(self):
        length = len(self)
        print(length,self)
        if '@grp' in self:
            if '@grp' == self[1]:
                return locker.deleteG(self)
            else: return "@grp is must be at 2nd position"
        elif length==2:
            ent = self[1]
        else:
            ent = input("Enter the entry you want to delete:- ")
        fnd = locker.kdb.find_entries(title=ent, first=True)
        if fnd:
            locker.kdb.delete_entry(fnd)
            locker.kdb.save()

            return "Entry deleted"
        return "Entry not found"


    def deleteG(self):
        print(len(self),self)

        if len(self)==3:
            group = self[2]
        else:
            group = input("Enter the entry you want to delete:- ")
        grp = locker.kdb.find_groups(name=group, first=True)
        if grp:
            locker.kdb.delete_group(grp)
            locker.kdb.save()

            return "Group deleted"
        return "Group not found"
    def findEntries(self):

        length = len(self)
        if length == 1:
            fnd = locker.kdb.entries
        elif '@grp' == self[1]:
            return locker.findEntryInGroup(self)
        elif length==2:
            name = self[1]
            fnd = locker.kdb.find_entries(title=name, first=True)
        elif length>2:
            return "@grp is required at 2nd position"
        else:
            name = input("Enter the name to find:- ")
            fnd = locker.kdb.find_entries(title=name, first=True)
        if fnd:
            return fnd
        return "Entry not found"

    def findEntryInGroup(self):

        if len(self)==3:
            group = self[2]
            grp = locker.kdb.find_groups(name=group, first=True)
            fnd = grp.entries
        elif len(self)==4:
            group = self[2]
            name = self[3]
            fnd = locker.kdb.find_entries(title=name, first=True)
        else:
            group = input("Enter the group name:")
        if fnd:
            return fnd
        return "Group entry is empty!!"
