"""
    Title: HeadKuarter
    Title: rightclick.py
    Language: Python
    Date Created: 28-07-2022
    Date Modified: 12-08-2022
    Description: Add copy content functionality to context menu
        ###############################################################
        ##                     Main file                             ## 
        ###############################################################
 """
import os
import sys
import winreg as reg

def copyContent(): 

    # Get path of current working directory and python.exe
    cwd = os.getcwd()
    python_exe = sys.executable

    # optional hide python terminal in windows
    hidden_terminal = '\\'.join(python_exe.split('\\')[:-1])+"\\pythonw.exe"


    # Set the path of the context menu (right-click menu)
    key_path = r'txtfile\\shell\\CopyContent'

    # Create outer key
    key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path)
    reg.SetValue(key, '', reg.REG_SZ, '&Copy Content')  # Change 'Organise folder' to the function of your script

    # create inner key
    key1 = reg.CreateKey(key, r"command")
    reg.SetValue(key1, '', reg.REG_SZ, 'cmd /c clip < "%1"') 

def delet_key():
    cwd = os.getcwd()
    python_exe = sys.executable

    # optional hide python terminal in windows
    hidden_terminal = '\\'.join(python_exe.split('\\')[:-1])+"\\pythonw.exe"


    # Set the path of the context menu (right-click menu)
    key_path = r'txtfile\\shell\\CopyContent'
    key1_path = r'txtfile\\shell\\CopyContent\\command' # subkey

    # Create outer key
    key = reg.OpenKey(reg.HKEY_CLASSES_ROOT, key1_path)
    reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key1_path)
    reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_path)
   

    