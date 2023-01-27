import kraken_datatype as dt 
from kraken_schema_org import kraken_schema_org as k

def normalize_value(record_type, key, value):


    if key == '@type':
        return k.normalize_type(value)
        
    # normalize_value
    datatypes = k.get_datatype(record_type, key)
    normalized_value = None
    if datatypes:
        for i in datatypes:
            r = None
            try:
                r = dt.validate(i, value)
            except:
                a=1
            
            if r and r is True:
                try:
                    normalized_value = dt.normalize(i, value)
                    if normalized_value:
                        return normalized_value
                except:
                    a=1