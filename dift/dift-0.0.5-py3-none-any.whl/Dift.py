import json
def readData(file, ctype = True,seperator = ":",ignore=True) -> dict:
    """
    Read the data from a file and convert it into a dictionary

    :param file: The file to read data from
    :type file: TextIOWrapper


    :param ctype: Enable or disable the option to store int as int in dictionary
    :type ctype: bool

    :param seperator: The sign to seperate the key from the value
    :type seperator: string

    :param ignore: Ignore the error due to incorrect seperator or no value
    :type ignore: bool
    """

    
    name = []
    value = []
    d = dict()
    isvalue  = False
    com = False
    if ('.json' or '.Json')in file.name:
        
        return json.load(file)

    for line in file:
        if bool(line.strip()) == False:
            continue
        for word in line.strip():
            if word == "#":
                com = True
                break
            elif word != seperator and isvalue == False:
                name.append(word.strip())
            elif word == seperator:
                isvalue = True
            elif isvalue:
                value.append(word.strip())
        n ="".join(name)
        v = "".join(value)
        if com:
            com = False
        elif com==False and ctype == False:
            n ="".join(name)
            v = "".join(value)
            d[n.strip()] = v.strip()
            name = []
            value = []
            isvalue = False
            if ignore == False and v.strip() == '':
                raise Exception("Incorrect data in the file")
        elif com == False and ctype:
            n ="".join(name)
            v = "".join(value)
            try:
                int(v)
                d[n.strip()] = int(v.strip())
                name = []
                value = []
                isvalue = False
                if ignore == False and v.strip() == '':
                   raise Exception("Incorrect data in the file")
            except:
                d[n.strip()] = v.strip()
                name = []
                value = []
                isvalue = False
                if ignore == False and v.strip() == '':
                   raise Exception("Incorrect data in the file")
    return d    
