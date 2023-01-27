import json

""" Read and write data"""

def write_file(data,f_name="output.dct"):
    """
        Write data to a file f_name. 

        Used by
            - class BenchmarkSet 
    """
    with open(f_name, 'w') as handle:
        json_string = json.dumps(data,indent=4)
        json.dump(json_string, handle)

def read_file(f_name="output.dct"):
    """
        Read data from a file f_name. 

        Used by 
            - class BenchmarkSet
    """
    with open(f_name) as handle:
        json_data = json.load(handle)
        data = json.loads(json_data)
    return data
