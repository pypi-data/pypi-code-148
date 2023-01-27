import os
import zipfile
import logging

def create_zip(zip_name, upload_file, version_name):
     # make sure not double / in path
    if upload_file.endswith("/"):
        upload_file = upload_file[:-1]
    # creating path from upload_file and version_name
    upload_file = upload_file + "/" + version_name
    #check if folder exists
    if os.path.isdir(upload_file):
        logging.info("Folder exists: " + upload_file)
    else:
        return "Folder not exist: " + upload_file
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(upload_file):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()