import math
from collections import Counter 

def mean(data):
    """
    Returns the mean of the list data
    """
    Mean = sum(data) / len(data)
    return round(Mean, 1)

def grt(data, value):
    """
    Returns the mean of the list data for values greater than value
    """
    data = [i for i in data if i > value]
    Mean = mean(data)
    
    return round(Mean, 1)

def grtEqual(data, value):
    """
    Returns the mean of the list data for values greater or equal to value
    """
    
    data = [i for i in data if i >= value]
    Mean = mean(data)
    
    return round(Mean, 1)
    
def less(data, value):
    """
    Returns the mean of the list data for values less than value
    """
    
    data = [i for i in data if i < value]
    Mean = mean(data)
    
    return round(Mean, 1)
    

def lessEqual(data, value):
    """
    Returns the mean of the list data for values less or equal to value
    """
    data = [i for i in data if i <= value]
    Mean = mean(data)
    
    return round(Mean, 1)

def notEqual(data, value):
    """
    Returns the mean of the list data for values not equal to value
    """
    data = [i for i in data if i != value]
    Mean = mean(data)
    
    return round(Mean, 1)


def outlier(data, low, high):
    
    """
    Removes the outliers from list data
    """
    
    fix = [i for i in data if i >= low and i <= high]
    
    return fix
    
def imputate(data, low, high):
    """
    Replaces invalid values in the data with the mean of the filtered data.
    """
    # create a copy of the data without outliers
    data_copy = outlier(data, low, high)
    
    # compute mean of the filtered data
    mean_val = mean(data_copy)
    
    # replace the invalid value with the mean
    
    for i in data:
        if i > high or i < low:
            data[data.index(i)] = round(mean_val, 1)  
            
    return data

def median(data):
    """
    Returns the median of the list data
    """
    data.sort()
    if len(data)% 2 == 0:
        median = (data[int(len(data)/2)-1] + data[int(len(data)/2)])/2
    else:
        median = (data[int(len(data)/2)])
    return median

def mode(data):
    """
    Returns the mode of the list data
    """
    frequency = Counter(data)
    mode = [k for k, v in frequency.items() if v == max(list(frequency.values()))]
    if len(mode) == len(data):
        return None
    else:
        return mode
    
def Help():
    print(".mean(data) - Returns the mean of the list data\n")
    print(".grt(data, high) - Returns the mean of the list data for values greater than value\n")
    print(".grtEqual(data, low) - Returns the mean of the list data for values greater or equal to value\n")
    print(".less(data, high) - Returns the mean of the list data for values less than value\n")
    print(".lessEqual(data, high) - Returns the mean of the list data for values less or equal to value\n")
    print(".notEqual(data, num) - Returns the mean of the list data for values not equal to value\n")
    print(".outlier(data, low, high) - Removes the outliers from the list data\n")
    print(".imputate(data, low, high) - Replaces invalid values in the data with the mean of the filtered list data.\n")
    print(".median(data) - Returns the median of the list data\n")
    print(".mode(data) - Returns the mode of the list data - if there is no repition will return 'None' -"
    "If there is equal repitition will return a list of equal values\n")
    print(".Help - Shows you this!\n")

