import random 
import string

def generate():
    
    num = random.choices(range(0,10), k=random.randint(1,4))
    num = "".join(str(n) for n in num)

    alphaNumeric = "".join(random.choices(string.ascii_letters+string.digits ,k=9))

    special = "".join(random.choices("@$",k=1))
    
    
    
    password = alphaNumeric+special+num
    
    
    return password[:12]


