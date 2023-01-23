from utils import Dict as DictParent


class Dict(DictParent):
    OTHERS = 'Others'

    def __len__(self):
        return len(self.keys())

    @property
    def total(self):
        return sum(self.values())

    @property
    def d(self):
        return self.x

    def keys_sorted(self):
        return [item[0] for item in self.items_sorted()]

    def items_sorted(self):
        return sorted(self.items(), key=lambda x: x[1], reverse=True)

    def items_othered(self, max_p_other=0.001):
        p_other = 0
        items = []
        for item in self.items_sorted():
            p = item[1] / self.total
            if p < max_p_other:
                p_other += p
            else:
                items.append(item)
        items.append((self.OTHERS, p_other))
        return items

    @staticmethod
    def concat(dict_list):
        d = {}
        for _dict in dict_list:
            for k, v in _dict.items():
                d[k] = d.get(k, 0) + v
        return Dict(d)
