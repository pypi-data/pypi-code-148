import json
import os

class myCredentials:
    '''
    This is a class of my Credentials to 
    import various credentials for use with LexisNexis APIs
    '''
    
    def __init__(self):
       
        print('i think this worked')
        check_file_exists()
        f=json_file_path()
        with open(f,"r") as outfile:
            dict = json.load(outfile)
        self.__dict__.update(dict)
    def setKey(self,myDict):
        '''
        Send a dictionary of the keys to store
        '''
        import json
        self.__dict__.update(myDict)
        f=json_file_path()
        with open(f,"w") as outfile:
            json.dump(self.__dict__, outfile, indent=4)
    def getCredentials(self):
        import pprint as pp
        pp.pprint(self.__dict__)
def blankCredentials():
    dict={
          "Metabase_Search_Key": "",
          "Metabase_Filters_Key": "",
          "Metabase_Portal_UN": "",
          "Metabase_Portal_PW": "",
          "WSAPI_client_id": "",
          "WSAPI_secret": ""
         }
    return dict
def check_file_exists():
    from os.path import exists
    f=json_file_path()
    file_exists = exists(f)
    if not file_exists:
        with open(f, "w") as outfile:
            json.dump(blankCredentials(),outfile)
def json_file_path():
    path = os.path.dirname(os.path.abspath(__file__))
    json_file_name = 'myCredentials.json'
    json_file_path = os.path.join(path,json_file_name)
    return json_file_path
        
        