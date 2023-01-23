import os
import zipfile

def create_zip(zip_name, folder_name):
    #check if folder exists
    if os.path.isdir(folder_name):
        print("Folder exists: " + folder_name)
    else:
        return "Folder not exist: " + folder_name
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()