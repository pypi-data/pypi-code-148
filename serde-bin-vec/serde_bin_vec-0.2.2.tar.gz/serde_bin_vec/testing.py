import __init__
from random import random
from uuid import uuid4


filename = uuid4().hex
our_id = uuid4()
print('input', our_id.hex)
__init__.save(our_id.bytes, [random()]*512, filename)

output = __init__.read_all(filename)


print(output[0][0])
