import ast

def get_dict(string):
    lists = ast.literal_eval(string)
    dict_ = {k: [v] for k, v in lists}
    return dict_