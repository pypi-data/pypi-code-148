#!/usr/bin/python
# -*- coding: gbk -*-


BPA_LINE_LEN = 80  # 稳定5.3版本是80，5.7版本是86

def str_slice(str, field_obj):
    n1 = field_obj.sp - 1
    n2 = field_obj.ep
    try:
        rstr = str[n1:n2].strip()
    except:
        rstr = ''
    return rstr


# 在字符型转成浮点型的时候，把空格看成0
def str2float(str):
    v = 0.
    try:
        v = float(str)
    except:
        pass
    return v


# 在字符型转成整型的时候，把空格看成0
def str2int(str):
    v = 0
    try:
        v = int(str)
    except:
        pass
    return v


# 产生新的字符串反映数据更新
# field 所在的数据卡项, name 新的数据卡项值
# 加入模式m, 用于PZ时保留两位小数，其余一位
# m=-1, 保留原小数点
def str_replace(str_data, value, field, m=-1):  # **args):
    """

    @param str_data:
    @param value:
    @param field:
    @param m:
    @return:
    """
    n1 = field.sp - 1
    n2 = field.ep
    n3 = n2 - n1

    # m = -1
    # if args.get('dec'):
    #    m = args.get('dec')

    if type(value) in [float, int]:  # 如果是数字
        if m == 0:
            str_rep = str(int(round(value, 0)))
        elif m > 0:
            str_rep = str(round(value, m))
        else:
            str_rep = str(value)

        if len(str_rep) > n3:
            if str_rep[0:2] == '0.':
                if len(str_rep) == n3 + 1:
                    str_rep = str_rep[1:]
                elif round(float(str_rep), n3 - 1) == 1.0:
                    str_rep = '1.0'
                else:  # 四舍五入
                    str_rep = str(round(float(str_rep), n3 - 1))[1:]
            elif str_rep[0:3] == '-0.':  # 四舍五入
                str_rep = str(round(float(str_rep), n3 - 2))
                str_rep = '-.' + str_rep[3:]
        str_rep = str_rep[0:n3].rjust(n3)
    else:  # 如果是字符串
        str_rep = value
        str_rep = str_rep[0:n3].ljust(n3)

    rev_data_str = str_data[0:n1].ljust(n1) + str_rep + str_data[n2:]
    return rev_data_str


# 把piece_str字符串替换str相应位置
# str原来的字串, piece_str要写的内容
def str_join(line_str, piece_str, field):
    """
    用piece_str替换line_str的field位置
    @param line_str: 
    @param piece_str: 
    @param field: 
    @return: 
    """
    n1 = field.sp - 1
    n2 = field.ep
    n3 = n2 - n1
    piece_str = piece_str[0:n3]
    piece_str = piece_str.ljust(n3)
    return line_str[0:n1].ljust(n1) + piece_str + line_str[n2:]


def bpa_str2float(s: str, f: int = None, default: float = 0):
    """
    F6.5，表示要求输入一个浮点数，占有的最大列数为6列，缺省小数点后的位数为5位。
    如果输入‘123456’，由于没有小数点，则程序缺省处理为1.23456；如果输入‘10’，程序读入后缺省处理，前面自动补零，小数点后截取5位，该数变成了0.00010。
    如果输入‘10.’，由于有小数点，程序读入后为10.0；如果填写‘.12345’，则程序读入后为0.12345。
    如果填写的浮点数没有占满指定的列，如对于格式F6.5输入‘10.’空3列，则忽略空格，与对整数中空格的处理方法一致。
    @param default:
    @param f:
    @param s:
    @return:
    """
    length = len(s)
    s = s.strip()
    if s:
        return (float(s + '0')) if '.' in s else (float(s) / (10 ** f))
    else:
        if default is None:
            raise ValueError('存在风险！')
        return default


def bpa_str(s: str):
    return s.strip()


def bpa_str2int(s: str, default: int = None):
    s = s.strip()
    if len(s) > 0:
        return int(s)
    else:
        if default is None:
            raise ValueError('存在风险！')
        return default


def bpa_str2x(s: str, t: type, f: int = None, default = None):
    if t == str:
        return bpa_str(s)
    elif t == int:
        return bpa_str2int(s, default=default)
    elif t == float:
        return bpa_str2float(s, f, default)


def bpa_card_line(bline: str):
    """
    规范化bpa文件行。
    对于不是纯换行的行，将输入的文件行补齐到BPA_LINE_LEN长度，去掉换行符
    """
    if bline == b'\r\n' or bline == b'\n':
        return b'\n'
    elif bline[-2:] == b'\r\n':
        return bline[:-2].ljust(BPA_LINE_LEN)
    elif bline[-1:] == b'\n':
        return bline[:-1].ljust(BPA_LINE_LEN)
    else:
        return bline.ljust(BPA_LINE_LEN)
    # # 出现有(END)
    # raise ValueError('遇到了不以\\n,\\r\\n结尾的行！')


class FFFloat2Str:
    def __init__(self, w, d):
        self.w = w
        self.d = d
        self.max = 10 ** (w - (1 if d else 0))
        self.min = -1 * 10 ** (w - 1 - (1 if d else 0))
        self.pfull = 10 ** (w - d - 1)
        self.nfull = -1 * 10 ** (w - d - 2)

    def write(self, fl):
        f = fl[0]
        if not f:
            return ' ' * self.w
        assert self.min < f < self.max

        f += 0.0
        if self.pfull < f < self.pfull * 10 or 10 * self.nfull < f < self.nfull:
            f *= 10 ** (3 * self.d)
            return ('{:.' + str(self.w) + 'f}').format(f)[:self.w].ljust(self.w)

        s = ('{:.' + str(self.w) + 'f}').format(abs(f))
        if s[:2] == '0.':
            s = s[1:]
        if f < 0:
            s = '-' + s
        return s[:self.w].ljust(self.w)


if __name__ == '__main__':
    import fortranformat as ff
    class t:
        def __init__(self, w, b):
            self.a = ff.FortranRecordReader('F' + str(w) + '.' + str(b))
            self.b = FFFloat2Str(w, b)
        def w(self, f):
            h = self.b.write([f])
            g = self.a.read(h)[0]
            return g == f, '\t'.join([str(f), h, str(g)])

    a = FFFloat2Str(6, 5)  # todo F6.5  读.00008,写成了8.0000
    print(a.write([.00008]))
    print(a.write([-321.12345]))
    print(a.write([.12345]))
    print(a.write([-.12345]))
    #
    # b = t(5, 4)
    # for i in range(1000000):
    #     f, s = b.w(i / 10000)
    #     if not f:
    #         print(i, '\t' + s)
