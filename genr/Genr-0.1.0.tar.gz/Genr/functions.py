import ast

def get_dict(string):
    lists = ast.literal_eval(string)
    dict_ = {k: [v] for k, v in lists}
    return dict_

def ensure_format_dict(string):
    string = string.strip()
    if string.startswith('[') and string.endswith(']'):
        string = string[1:-1].strip()
        items = string.split('],[')
        items = [item.strip() for item in items]
        res = []
        for item in items:
            if item.startswith('"') and item.endswith('"'):
                res.append('["' + item[1:-1] + '"]')
            elif item.startswith('[') and item.endswith(']'):
                res.append(ensure_format_dict(item))
            else:
                res.append('["' + item + '"]')
        return '[' + ','.join(res) + ']'
    else:
        return '[[\"' + string + '\"]]'


def ensure_format_list(string):
    if string.startswith('["') and string.endswith('"]'):
        return string
    elif string.startswith('["'):
        return string + '"]'
    elif string.endswith('"]'):
        return '["' + string
    elif string.startswith('[') and string.endswith(']'):
        return '["' + string[1:-1] + '"]'
    else:
        return '["' + string + '"]'
