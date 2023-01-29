def winput(query: str, acc: list):
    userin=''
    for i in acc:
        i = i.lower()
    while userin not in acc:
        userin = input(query).lower()
    return userin
