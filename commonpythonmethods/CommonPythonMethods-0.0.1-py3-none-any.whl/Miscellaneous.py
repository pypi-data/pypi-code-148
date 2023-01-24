import math
import operator


def Convert_List_To_Dict(list1, list2):
    """Simple method to convert list to dict"""
    dictionary = dict(zip(list1, list2))
    print(dictionary)
    return dictionary


def Index_List_Of_Duplicates(seq, item):
    """Simple method to get index"""
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at + 1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


def Repeated_Text_MultipleTimes(character):
    """ Create repeatedwords for api """
    word = character * 257
    return word


def Calculate_Sqrt(number):
    """calculate sqrt"""
    return math.sqrt(number)


def Sorted_Dict(d, number):
    """sort_dict in ascending order"""
    num = int(number)
    sorted_d = dict(sorted(d.items(), key=operator.itemgetter(num)))
    return dict(sorted_d)


def Sorted_Reverse_Dict(d, number):
    """sort dict in descending order"""
    num = int(number)
    sorted_d = dict(sorted(d.items(), key=operator.itemgetter(num), reverse=True))
    return dict(sorted_d)
