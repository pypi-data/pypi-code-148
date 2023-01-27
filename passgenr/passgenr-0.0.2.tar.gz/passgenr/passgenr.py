import random
import string

def passgenr(n_letter, n_digit, n_symbol):
    letters = ''.join((random.choice(string.ascii_letters) for i in range(n_letter)))
    digits = ''.join((random.choice(string.digits) for i in range(n_digit)))
    symbols = ''.join((random.choice(string.punctuation) for i in range(n_symbol)))

    # Convert resultant string to list and shuffle it to mix letters and digits
    sample_list = list(letters + digits + symbols)
    random.shuffle(sample_list)

    # convert list to string
    final_string = ''.join(sample_list)
    return final_string

# calling function
# print(passgenr(6, 2, 2))
