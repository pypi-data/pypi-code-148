from pypinyin import pinyin, lazy_pinyin

def pin(text: str):
    try:
        res_list = pinyin(text)
        res = []
        for s in res_list:
            res.append(s[0])
        return '-'.join(res)
    except:
        return False

def pin1(text: str):
    try:
        return '-'.join(lazy_pinyin(text))
    except:
        return False

def duoyin(text: str):
    try:
        res = pinyin(text, heteronym=True)
        res_list = []
        for s in res[0]:
            res_list.append(s)
        return '-'.join(res_list)
    except:
        return False
        