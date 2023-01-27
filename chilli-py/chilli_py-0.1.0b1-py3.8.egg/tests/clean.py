import os

""" Clean script """

delete = ['chilli.h5'
]

for d in delete:
    try:
        os.remove(d)
        print(f"File {d} Removed!")
    except BaseException:
        'Nothing'
