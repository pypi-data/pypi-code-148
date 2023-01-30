"""
    Title: HeadKuarter
    Title: app.py
    Language: Python
    Date Created: 06-05-2022
    Date Modified: 05-05-2022
    Description:
        ###############################################################
        ##                     Main file                             ## 
        ###############################################################
 """

from asyncio.windows_events import NULL
from ctypes.wintypes import CHAR
#from curses import echo
from socket import if_nameindex
from typing import Type
from unicodedata import name
import click
from Module.veracrypt import createContainer, mountDrive
from Module.formosa import passwordGenerator
from Module.formosa import passwordGeneratorLC
from Module.gui import rightclick
from autoVera import win
import getpass
import re
import json
from Module.keepass.keepass import locker,createDb
from os.path import exists as file_exists
if file_exists('C:\\Program Files\\VeraCrypt\\Veracrypt.exe')==False:
    win()



@click.group()
def headkurter():
    '''
    A tool to generate password encrypt drive  and Password manager 
    '''
    pass

@click.command()
@click.argument('filename')#, type=click.Path(exists=True)
@click.option('--size', required=True, type=int, help = "Create disk in Mega Byte")
@click.option('--autopass', type = bool, default = False, help = "True : Generate secure Password to encrypt disk")
@click.option('--encrypt','-encrypt_method',type = click.Choice(['AES', 'Serpent', 'Twofish', 'AES-Twofish', 'AES-Twofish-Serpent','Serpent-AES','Serpent-Twofish-AES','Twofish-Serpent']),default = 'AES')
@click.option('--hash','-hash_methond',type = click.Choice(['RIPEMD-160', 'SHA-512', 'Whirlpool']), default = 'SHA-512')
@click.option('--format','--format-types',type = click.Choice(['exFAT', 'ntfs']), default = 'ntfs')
@click.option('--pwd',type = str, help = "Password to encrypt drive can be Text or Environment Variable")
@click.option('--pim',default = 0)
@click.option('--theme',  type = click.Choice(['finances', 'harry_potter', 'medieval_fantasy', 'the_big_bang_theory','tourism']), default = 'finances', help = "String value from given option")
@click.option('--number', type = click.Choice(['2', '3', '4', '5', '6', '7','8']), default = '2', help = "an integer value between 2-8 ")
@click.option('--num','--insert-number', type = bool, default = False, help = "When Set insert number in password")
@click.option('--spchar','--insert-spchar', type = bool, default = False, help = "When Set Insert sepcial character in password")
@click.option('--sc','--swap-case', type = bool, default = False, help = "When Set change case of password")
@click.option('--cmplx','--complexity', type = bool, default = False, help = "passsword complexity when True: Generate complex password")
@click.option('--str-pwd','--store-password', type = click.Choice(['display','file','ram']), default = 'file', help = "Option To Store Password")
def create(filename,size,encrypt,hash,format,pim, autopass,theme,number,num,spchar,sc,pwd,cmplx,str_pwd):
    '''
    Format and Create encrypted disk space

    FILENAME  location to creat encrypted drive e.g "C:\privateVdisk\<NewFileName>.vc"
    '''
    if autopass:
        number = int(number)
        if(cmplx):
            pwd=passwordGenerator.generate_text(theme,number,num,spchar,sc,str_pwd)
        else:
            pwd=passwordGeneratorLC.generate_text(theme,number,num,spchar,sc,str_pwd)
    elif pwd == None:
        pwd = getpass.getpass()
        pwd2 = getpass.getpass("Confirm Password: ")
        #print (f'pass {pwd}')

        if pwd == "":
            click.echo("either set --autopass True or provied password --pwd ") 
            exit()
        elif pwd != pwd2:
            click.echo("Password and Confirm Password does not match") 
            exit()

    size =f'{str(size)}M' 
    createSuccess = createContainer.container(filename,size,pwd,encrypt,hash,format,pim)
    if (str_pwd == 'display'):
        click.echo(f'Save this password:- {pwd}')
    #click.echo(f'Save this password:- {pwd}')
    #print(createSuccess)




@click.command()
@click.argument('filename')#, type=click.Path(exists=True)
@click.option('--drive', required=True, help = "Available Alphabet to Mount Encrypted Drive")
@click.option('--pwd',type = str, help = "Password to encrypt drive can be Text or Environment Variable")
def mount(filename,drive,pwd):
    '''
    Mount Encrypted Drive 

    FILENAME  location of Encrypted Drive e.g "C:\privateVdisk\encryptvdisk1.vc"
    '''
    if (pwd == None):
        pwd = getpass.getpass()
    
    mountSuccess = mountDrive.mount_drive(filename,drive,pwd)
    #print(mountSuccess)





@click.command()
@click.argument('filename')#, type=click.Path(exists=True)
@click.option('--drive', required=True, help = "Mounted Drive ")
def unmount(filename,drive):
    '''
    Unmount Mounted Drive  

    FILENAME  location of Encrypted Drive e.g "C:\privateVdisk\encryptvdisk1.vc"
    '''
    
    mountSuccess = mountDrive.unmount(filename,drive)
    #print(mountSuccess)





@click.command()
@click.option('--theme',  type = click.Choice(['finances', 'harry_potter', 'medieval_fantasy', 'the_big_bang_theory','tourism']), default = 'finances', help = "pharase theem that will help in generate password")
@click.option('--number', type = click.Choice(['2', '3', '4', '5', '6', '7','8']), default = '2', help = "an integer value between 2-8 ")
@click.option('--num','--incert-number', type = bool, default = False, help = "When Set insert number in password")
@click.option('--spchar','--incert-spchar', type = bool, default = False, help = "When Set Insert sepcial character in password")
@click.option('--sc','--swap-case', type = bool, default = False, help = "When Set change case of password")
@click.option('--cmplx','--complexity', type = bool, default = False, help = "passsword complexity when True: Generate complex password")
@click.option('--str-pwd','--store-password', type = click.Choice(['display','file','ram']), default = 'file', help = "Option To Store Password")
def generatepassword(theme,number,num,spchar,sc,cmplx,str_pwd):
    '''
    Generate  Password  

    '''
    number = int(number)
    if(cmplx):
        password=passwordGenerator.generate_text(theme,number,num,spchar,sc,str_pwd)
    else:
        password=passwordGeneratorLC.generate_text(theme,number,num,spchar,sc,str_pwd)

    if (str_pwd == 'display'):
        click.echo(f'Save this password:- {password}')

@click.command()
@click.argument('locker_name')
@click.password_option(help = "Optional, Password for creating locker, it can be string or system variable")
def keepassC(locker_name,password):
    '''
    Create Locker  

    LOCKER-NAME  locker Name with absolute or relative path e.g "C:\privateVdisk\lockername"
    '''
    if not locker_name.endswith(".kdbx"):
        locker_name = locker_name+'.kdbx'
    if not file_exists(locker_name):
        createDb(locker_name,password)
        print('Locker Space created Succesfully')
    else:
        print('Locker space already exist')

@click.command()
@click.argument('locker_name')
@click.password_option(confirmation_prompt=False)
@click.option('--add_entry', is_flag=True, help ="To add new entry")
@click.option('--group', '-grp', required=False, help ="group name to creat or find entries inside a particular group" )
@click.option('--dname', '-d', required=False, help ="Domain name for which password to be stored")
@click.option('--uname', '-u', required=False, help ="User name for Domain")
@click.option('--pswd', '-p', required=False, help ="Password for Domain")
@click.option('--find_entries', is_flag=True, help="To find all entries if passed withouth any extra argument")
@click.option('--entry', '-ent', required=False)
@click.option('--delete', is_flag=True,help="To delete the specific entry in the locker")
@click.option('--view_pass', is_flag=True,help="To see the password of the specified field")
@click.option('--show', '-show', is_flag=True, help ="(Default) Required with \" view_pass \" password will be dispalyed at console")
@click.option('--copy', '-copy', is_flag=True, help ="Required with \" view_pass \" password will be copied to clipboard")
@click.option('--headkurter', is_flag=True, help ="it will activate headkurter prompt to perform multiple operation on logged in locker And to exit type \"exit\"")

def keepassdb(locker_name, password, group, add_entry, dname, uname, pswd, find_entries, entry, delete, view_pass,copy,show,headkurter):
    
    try:
        locker(locker_name,password)
    except:
        click.echo("Incorrect locker-name or password!!")
    else:

        if add_entry:

            if group:
                if not dname:
                    dname = click.prompt("Enter the Domain name")
                if not uname:
                    uname = click.prompt("Enter the username")
                if not pswd:
                    pswd = click.prompt("Enter the password")
                command = [True,True,group,dname,uname,pswd]
                click.echo(locker.createEntryinGrp(self=command))

            else:
                if not dname:
                    dname = click.prompt("Enter the Domain name")
                if not uname:
                    uname = click.prompt("Enter the username")
                if not pswd:
                    pswd = click.prompt("Enter the password")
                command = [True,dname,uname,pswd]
                click.echo(locker.adEntry(self=command))

        elif find_entries:
            if group:
                if entry:
                    command = [True, True, group, entry]
                    click.echo(locker.findEntryInGroup(self=command))
                else:
                    command = [True, True, group]
                    click.echo(locker.findEntryInGroup(self=command))
            elif dname:
                    command = [True, dname]
                    click.echo(locker.findEntries(self=command))
            else:
                command = [True]
                click.echo(locker.findEntries(self=command))
        
        elif delete:
            if group:
                command = [True, True, group]
                click.echo(locker.deleteG(self=command))
            elif dname:
                command = [True, dname]
                click.echo(locker.delete(self=command))
            else:
                c = click.prompt("Do you want to delete a grp (y/n)")
                if c =='Y' or c=='y':
                    group= click.prompt("Enter the group name:- ")
                    command = [True, True, group]
                    click.echo(locker.deleteG(self=command))
                else:
                    dname = click.prompt("Enter the domain you want to delete")
                    command = [True, dname]
                    click.echo(locker.delete(self=command))


        elif view_pass:
            if not dname:
                dname = click.prompt("Enter the Domain name")
            if show:
                command = [True, dname]
                click.echo(locker.retrivepass(self=command))
            if copy:
                command = [True,dname,copy]
                click.echo(locker.retrivepass(self=command))
            else:
                command = [True, dname]
                click.echo(locker.retrivepass(self=command))
        elif headkurter:
            while True:
                command = list(click.prompt('Headkurter~$').strip().replace('-','').split(" "))
                if command[0] == 'add_entry':
                    try:
                        click.echo(locker.adEntry(self=command))
                    except:
                        click.echo("Entry already exists in group")

                elif command[0] == 'find_entries':
                    click.echo(locker.findEntries(self=command))

                elif command[0] == 'delete':
                    click.echo(locker.delete(self=command))

                elif command[0] == 'view_pass':
                    click.echo(locker.retrivepass(self=command))

                elif command[0] == 'exit':
                    click.echo("ThankYou...!!")
                    break
                else:
                    click.echo('%s: command not found' % command[0])

@click.command()
def copycontent():
    '''
    Copy Content  

    To Enable context menu to copy content of file to clipboard
    '''
    try:
        rightclick.copyContent()
        click.echo("Activated successfully..!")
    except:
        click.echo("please check, You have administrator privileges to run this command!")

@click.command()
def stopcopycontent():
    '''
    To remove copy content from context menu
    '''
    
    
    try:
        rightclick.delet_key()
        click.echo("Copy Content deactivated successfully..!")
    except:
        click.echo("please check, You have administrator privileges to run this command!")
    
headkurter.add_command(create)
headkurter.add_command(mount)
headkurter.add_command(unmount)
headkurter.add_command(generatepassword)
headkurter.add_command(keepassdb)
headkurter.add_command(keepassC)
headkurter.add_command(copycontent)
headkurter.add_command(stopcopycontent)

if __name__ == "__main__" :
    headkurter()
