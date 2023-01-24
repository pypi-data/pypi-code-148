def subsets(set:list, deep:int):
    res = [set]
    if deep>0 or deep==-1:
        for e in set:
            sub = [x for x in set if x != e]
            if not sub in res:
                res.append(sub)
            if deep>1:
                subs = subsets(sub, deep-1)
                for s in subs:
                    if not s in res:
                        res.append(s)
            if deep==-1:
                subs = subsets(sub, deep)
                for s in subs:
                    if not s in res:
                        res.append(s)
    return res

s = [1,2,3,4,5,6]

print(subsets(s,-1))
