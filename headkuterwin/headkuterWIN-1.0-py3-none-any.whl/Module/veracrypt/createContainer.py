"""
    Title: HeadKuarter
    Module Name: createContainer
    Language: Python
    Date Created: 7-05-2022
    Date Modified: 7-05-2022
    Description:
        ###############################################################
        ##  Encrypted container created with Veracrypt          ## 
         ###############################################################
 """

import subprocess 
import logging
import json
import os
import sys


creat_at = "C:\\privateVdisk\\encryptvdisk1.vc"
partition_size = "200M"
master_password = "MySuperSecurePassword1!"
encryption_method = "AES"
hash_method = "sha-512"
formate_filesystem= "ntfs"
pim = 0
script = f"\"C:\Program Files\VeraCrypt\VeraCrypt Format.exe\" /create \"{creat_at}\" /size \"{partition_size}\" /password {master_password} /encryption {encryption_method} /hash {hash_method} /filesystem {formate_filesystem} /pim {pim} /silent"

def win_creat(creat_at, partition_size, master_password,encryption_method,hash_method,formate_filesystem, pim):
    '''
       windows Contaner is to create encrypted virtual drive  
    '''

    success = False
    script = f"\"C:\Program Files\VeraCrypt\VeraCrypt Format.exe\" /create \"{creat_at}\" /size \"{partition_size}\" /password {master_password} /encryption {encryption_method} /hash {hash_method} /filesystem {formate_filesystem} /pim {pim} /silent"
    result = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    #print(result)
    if result.returncode:
            return success
        
    success = True
    return success

def linux_creat(creat_at, partition_size, master_password,encryption_method,hash_method,formate_filesystem, pim):
    '''
       Linux Container is to create encrypted virtual drive  
    '''

    success = False

    script = f"sudo veracrypt --text --create \"{creat_at}\" --size \"{partition_size}\" --password {master_password} --volume-type normal --encryption {encryption_method} --hash {hash_method} --filesystem {formate_filesystem} --pim {pim} --keyfiles \" \" --random-source --random-source randomdata.txt"
    result = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)


    if result.returncode:
            return success
        
    success = True
    return success

def container(creat_at, partition_size, master_password,encryption_method,hash_method,formate_filesystem, pim):
    '''
        Contaner is to create encrypted virtual drive 
    '''

    plt = sys.platform
    if plt=='win32':
        success = win_creat(creat_at, partition_size, master_password,encryption_method,hash_method,formate_filesystem, pim)
    elif plt=='linux':
        success = linux_creat(creat_at, partition_size, master_password,encryption_method,hash_method,formate_filesystem, pim)

    return success
