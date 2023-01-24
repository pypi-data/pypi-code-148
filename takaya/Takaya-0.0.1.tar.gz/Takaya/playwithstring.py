
def reverse_string(string):
    '''
    This function takes a string and returns it reversed.
    '''
    return string[::-1]

def count_vowels(string):
    """
    This function takes a string and returns the number of vowels in it.
    """
    vowels = 'aeiou'
    count = 0
    for char in string:
        if char in vowels:
            count +=1
    
    return count

def remove_punctuation(string):
    """
    This function takes a string and removes all puncutation marks.
    """
    punctuation = '!@#$%^&*()_-+={}[]|\:;"<>,.?/~`'
    new_string = ''
    for char in string:
        if char not in punctuation:
            new_string += char
    return new_string