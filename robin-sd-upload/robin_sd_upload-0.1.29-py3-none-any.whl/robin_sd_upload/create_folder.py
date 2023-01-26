import os

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("Folder created: " + folder)
        print("Folder path: " + os.path.abspath(folder))
        print('try to run script again')
        exit()
    else:
        print("Folder exists: " + folder)