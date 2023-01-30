from reactivex import operators, empty


def ignore_errors():
    return operators.catch(lambda *_: empty())
