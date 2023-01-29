def win_logic(usr, cmp):
    """

    :param usr: input user choice
    :param cmp: random generated choice
    :return: True/False
    """

    if (usr == 'R' and cmp == 'S') \
            or \
            (usr == 'S' and cmp == 'P') \
            or \
            (usr == 'P' and cmp == 'R'):
        return True
