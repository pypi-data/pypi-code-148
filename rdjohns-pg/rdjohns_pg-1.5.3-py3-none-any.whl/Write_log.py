import os, shutil
from datetime import datetime, date, timedelta
def writeLogTxt( name='_Log_for_Database_UNDEFINED.txt',data="Error",root_directory_name="rep",dir_name = '_LOG'):
    """Write log in .txt file

    Args:
        name (str, optional): _description_. Defaults to '_Log_for_Database_UNDEFINED.txt'.
        data (str, optional): _description_. Defaults to "Error".
        root_directory_name (str, optional): _description_. Defaults to "rep".
        dir_name (str, optional): _description_. Defaults to '_LOG'.
    """
    if root_directory_name:
        t = os.getcwd().split(root_directory_name)
        os.chdir(('/'.join(str(t[0]).split("\\")))+root_directory_name)
    if len(dir_name)>0:
        makeDirectrory(dir_name)
        os.chdir(dir_name)
    with open(name,'a', encoding=('utf-8')) as fic:
        fic.write(data)
    if len(dir_name)>0:
        os.chdir('..')
    if root_directory_name:
        os.chdir(root_directory_name.join(t))
    
def makeDirectrory(dir_name):
    """Make directory in local from the str or list in input

    Args:
        dir_name (str): name of the directory that we are going to create
    """
    if type(dir_name)==list:
        for i in dir_name:
            if not os.path.isdir(i):
                os.mkdir(i, mode=0o777, dir_fd=None)
    else:     
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name, mode=0o777, dir_fd=None)
def getNameFileOutput():
    """Return date with the form YYYYMMDD

    Returns:
        Date: YYYYMMDD
    """
    mydate = str(datetime.now()).split('.')[0]
    d = datetime.strptime(mydate, "%Y-%m-%d  %H:%M:%S")
    return d.strftime("%Y%m%d")