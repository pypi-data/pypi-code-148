"""
    Title: HeadKuarter
    Module Name: mountDrive
    Language: Python
    Date Created: 7-05-2022
    Date Modified: 7-05-2022
    Description:
        ###############################################################
        ##  mounting Veracrypt Encrypted container                   ## 
        ###############################################################
 """

import subprocess 
import logging
import json
import os

creat_at = "C:\\privateVdisk\\encryptvdisk1.vc"
drive = "X" # any letter
master_password = "MySuperSecurePassword1!"

def mount_drive(creat_at,drive,master_password):
    
    '''
    mount the encryted file to the drive
    '''
    success = False

    script = f"\"C:\Program Files\VeraCrypt\VeraCrypt.exe\" /volume \"{creat_at}\" /letter {drive} /password {master_password} /a /quit /silent"
    result = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print(result)
    if result.returncode:
            return success
        
    success = True
    return success

def unmount(creat_at,drive):
    #unmount encrypted drive
    success = False
    script = f"\"C:\Program Files\VeraCrypt\VeraCrypt.exe\" /volume \"{creat_at}\" /dismount {drive}  /quit /silent"
    result = subprocess.run(script,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print(result)
    if result.returncode:
            return success
        
    success = True
    return success