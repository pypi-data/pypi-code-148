import gridfs
from pymongo import MongoClient
def mongo_conn():
    global url 
    url = input("Enter your MongoUrl:")
    try:
        conn = MongoClient(url)
        print("Connected to Database")
        return conn.grid_file
    except Exception  as e:
        print(e)

def upload_file(file_url,file_name,db1):
    file_location = file_url
    #Create a object of GridFs for the above database.
    file_data = open(file_location,"rb")
    fs = gridfs.GridFS(db1)
    data = file_data.read()
    fs.put(data,filename = file_name)
    print("upload successful")
def download_file(download_path,file_name,db1):
    fs1 = gridfs.GridFS(db1)
    #define an image object with the location.
    data = db1.fs.files.find_one({'filename':file_name})
    my_id = data['_id']
    #Open the image in read-only format.
    outputdata = fs1.get(my_id).read()
    download_location = download_path
    output = open(download_location,"wb")
    output.write(outputdata)
    output.close()
    print('download completed')