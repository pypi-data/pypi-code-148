# -*- coding:utf-8 -*-
"""
# Name:         transient_stability: bpa_dat
# Author:       MilkyDesk
# Date:         2021/6/29 9:59
# Description:
#   
"""
import os

from typing import List
import pandas as pd

from ..base import bpa_annotation
from ..base.bpa_uid import _OneNameUid
from . import bpa_dat_before_data, bpa_dat_data
from ..base.bpa_base import _to_card
from ..base.bpa_uid import *
from ..base.bpa_str import bpa_card_line

"""
dat结构：
一级语句
网络数据前的控制语句
网络数据
控制语句
一级语句
"""


class DAT:
    """
    定位：
    提供DAT_Card的管理工具
    行为：
    1. 初始化: 读取文件
    2. __str__: 反向文本化功能。应该与_Card的组织类似。
    @todo 未来要加入许多其他元件的数据结构，所以会考虑重写这部分
    数据基础：
    lines: List of _Cards
    基础索引(行号)：
    can, cdt, cc1, cc2
    高级对象:
    bus, branch, gen: List of _Cards
    高级索引: list编号, uid_str
    *_name: List of uid_str
    *_order: {uid_str: #*}
    *_indexs: {uid_str: _Cards}
    branch_bus_order: List of [#bus, #bus]
    gen_bus_order: List of #bus
    """
    annotation_card = {'.', ' ', 'C'}
    symmeyty_line_card_set = {'L ', 'LD', 'LM', 'T ', 'TP', 'R ', 'RZ', 'RV', 'RQ', 'RP', 'RN', 'RM'}
    asymmeyty_line_card_set = {'L+', 'E '}
    line_card_set = {'L ', 'LD', 'LM', 'T ', 'TP', 'R ', 'RZ', 'RV', 'RQ', 'RP', 'RN', 'RM', 'L+', 'E '}
    bus_card_set = {'B ', 'BV', 'BM', 'BQ', 'BS', 'BT', 'BE', 'BF', 'BJ', 'BK', 'BL', 'BX', 'BD', '+', 'X ','BA','BZ','BC'}
    zone_card_set = {'I'}
    PZ_card_set = {'PZ'}

    def __init__(self, *p):
        self.cards, self.can, self.cc1, self.cdt, self.cc2 = p
        self.cdt_branch = []
        self.cdt_bus = []
        self.cdt_zone = []
        self.cdt_PZ = []
        self.bus, self.bus_indexs, self.bus_order, self.bus_name, \
        self.branch, self.branch_indexs, self.branch_order, self.branch_name, self.branch_bus_order, \
        self.gen, self.gen_indexs, self.gen_order, self.gen_name, self.gen_bus_order,self.zone_exchange,self.PZ = self.get_data_struct()
        self.gen_info = None
        self.branch_y, self.y_matrix = None, None
        self.get_branch_y()
        self.get_Y_matrix()
        self.mva_base = 100
        self.load_level = 1.

        self.describe()

    def describe(self):
        """todo 汇报当前的dat长啥样"""
        pass

    def get_data_struct(self):
        """
        目标是建立起【不依赖文件结构的】电网对象的索引，包括：
        1. 全集: bus, branch
        2. 根据名称组织起来的卡片: bus_indexs, branch_indexs
        3. 根据出现次序给定的顺序：bus_order， branch_order
        4. 将所有bus，branch对象按照此顺序标上序号
        @note: 此后出现的数据结构里，只有order字段，没有name字段。
        @return:
        """
        bus_indexs, branch_indexs, bus_order, branch_order, gen_indexs, gen_order = {}, {}, {}, {}, {}, {}
        bus_name, branch_name, gen_name, gen_bus_order, branch_bus_order = [], [], [], [], []

        bus = [self.cards[f]
               for f in self.cdt
               if self.cards[f].type in DAT.bus_card_set]
        self.cdt_bus = [f
               for f in self.cdt
               if self.cards[f].type in DAT.bus_card_set]
        gen = []
        n_bus = 0
        n_gen = 0
        for i, b in enumerate(bus):
            if b.name in bus_indexs:
                bus_indexs[b.name] += [b]
            else:
                bus_indexs[b.name] = [b]
                bus_order[b.name] = n_bus
                bus_name += [b.name]
                n_bus += 1
            b.order = bus_order[b.name]
            b.index = i#能映射到实际文件行数
            if _bus_has_gen(b):
                g_name = b.name + ' '
                gen_indexs[g_name] = [b]  # 默认了每个节点只有一台发电机
                gen_order[g_name] = n_gen
                gen_name += [g_name]
                gen_bus_order += [bus_order[b.name]]
                gen += [b]
                n_gen += 1

        branch = [self.cards[f]
                  for f in self.cdt
                  if self.cards[f].type in DAT.line_card_set]
        self.cdt_branch = [f
                  for f in self.cdt
                  if self.cards[f].type in DAT.line_card_set]
        zone_exchange = [self.cards[f]
                         for f in self.cdt
                         if self.cards[f].type in DAT.zone_card_set]
        PZ_card = [self.cards[f]
                         for f in self.cc1
                         if self.cards[f].type in DAT.PZ_card_set]
        self.cdt_zone = [f
                         for f in self.cdt
                         if self.cards[f].type in DAT.zone_card_set]
        self.cdt_PZ = [f
                         for f in self.cc1
                         if self.cards[f].type in DAT.PZ_card_set]
        n_branch = 0
        for i, l in enumerate(branch):
            if l.name in branch_indexs:
                branch_indexs[l.name] += [l]
            else:
                branch_indexs[l.name] = [l]
                branch_order[l.name] = n_branch
                branch_bus_order.append([bus_order[l.name1], bus_order[l.name2]])
                branch_name += [l.name]
                n_branch += 1
            l.order = branch_order[l.name]
            l.index = i  # 能映射到实际文件行数
            l.order1 = bus_order[l.name1]
            l.order2 = bus_order[l.name2]

        branch_bus_order = np.array(branch_bus_order)
        return bus, bus_indexs, bus_order, bus_name, \
               branch, branch_indexs, branch_order, branch_name, branch_bus_order, \
               gen, gen_indexs, gen_order, gen_name, gen_bus_order,zone_exchange,PZ_card

    def __str__(self):
        """将结构化的card还原回str行"""
        return '\n'.join([x if type(x) is str else str(x) for x in self.cards]) + '\n'

    def save_to_file(self, path, text_prefix=None):
        """
        想写入哪里，直接写完整路径即可。会直接递归地创建路径。
        todo 未来与swi的方法合并
        :param path: 有没有以.dat结尾都可以。
        :param text_prefix: 正文的开头，用来记录一些信息的。
        :return:
        """
        if path[-4:].lower() != '.dat':
            path += '.dat'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = open(path, 'w')
        if text_prefix:
            file.write(text_prefix)
        file.write(str(self))
        file.close()

    def read_pfo(self, dat_path, pu=False, type ='BPA'):
        """
        #  1. 并不确定如何处理shuntQ:
         2022年11月5日 data.utils的处理，归入负荷。因为这些是静态的。Q1(使用的)+Q3(未投入), Q2(已有的)不包括在内
         参考：PSD-BPA潮流说明书4.5.3，P103最上
         "如果在潮流数据中设定了BE节点类型，为了保持该类型节点的电压值，程序计算时会在这些类型节点强制增加无功补偿，应查看潮流结果文件（PFO为后缀
         的文件）中“未安排无功的节点列表”，该列表中显示了所有BE节点强制增加的无功，如果为正值，表示增加了电容器，缺少无功，需要增加无功进行补偿；
         反之，表示增加了电抗器，无功较多，应减少无功补偿。"
        #  2. 并不确定如何处理恒功率负荷
        :param dat_path:
        :param pu: 是否对功率标幺化
        :return:
        """
        n_bus = len(self.bus_order)

        # 读pfo文件
        # pfo_lines = open(dat_path[:-4] + '.pfo', 'rb').readlines()
        if type=='BPA':
            pfo_lines = open(dat_path[:-4] + '.pfo', 'rb').readlines()
            # 检查是否收敛：
            key = '不收敛'.encode('gbk')
            for l in pfo_lines:
                if key in l:
                    return None

            # 只提取 bus_info_start_flag 那一段
            stl = [i for i, l in enumerate(pfo_lines) if '*  节点相关数据列表'.encode('gbk') in l]
            # 有些潮流结果有问题，但是又不想让程序中断
            if len(stl) == 0:
                return None
            stl = stl[0]
            edl = [i for i, l in enumerate(pfo_lines[stl:]) if '------'.encode('gbk') in l][1] + stl
            r = pfo_lines[stl:edl]
            sstl = []

            sstl = [i for i, l in enumerate(r) if b'\r\n' == l]
            if sstl:
                sstl = sstl[0] + 1
            else:
                sstl = 0
            r2 = r[sstl:]
            for i in range(len(r2)):
                s = r2[i]
                if s[45:46] == b' ':  # 'PF'
                    s = s[:45] + b'0' + s[46:]
                if s[97:98] == b' ':  # 'TYPE'
                    s = s[:97] + b'*' + s[98:]
                if s[102:103] == b' ':  # 'OWNER'  @todo 注意所有者代码是3个字节，因此这里应该用完全的三个字节进行比较。
                    s = s[:102] + b'*' + s[103:]
                if s[108:110] == b'  ':  # 'ZONE'
                    s = s[:108] + b'* ' + s[109:]
                r2[i] = s[:-2].decode('gbk', errors='ignore')
            df = pd.DataFrame(r2)[0].str.split(r'\s+|\s*/\s*|\n', expand=True).drop([0], axis=1)

            # 重命名、数据类型转换
            df.columns = [BUS_NAME_STR, BUS_BASE_STR, 'V',
                          GEN_P, GEN_Q, 'PF', LOAD_P, LOAD_Q,
                          'SHUNTQ1', 'SHUNTQ2', 'SHUNTQ3',
                          'TYPE', 'OWNER', 'ZONE', VOLTAGE, ANGLE]
            df[[BUS_NAME_STR, 'TYPE', 'OWNER', 'ZONE']] = df[[BUS_NAME_STR, 'TYPE', 'OWNER', 'ZONE']].astype('str',
                                                                                                             copy=False)
            df[[BUS_BASE_STR, 'V', GEN_P, GEN_Q, 'PF', LOAD_P, LOAD_Q, 'SHUNTQ1', 'SHUNTQ2', 'SHUNTQ3', VOLTAGE, ANGLE]] = \
                df[[BUS_BASE_STR, 'V', GEN_P, GEN_Q, 'PF', LOAD_P, LOAD_Q, 'SHUNTQ1', 'SHUNTQ2', 'SHUNTQ3', VOLTAGE,
                    ANGLE]].astype('float', copy=False)
            df.loc[df['TYPE'] == '*', 'TYPE'] = ' '
            df.loc[df['OWNER'] == '*', 'OWNER'] = ' '
            df.loc[df['ZONE'] == '*', 'ZONE'] = ' '

            # 标幺值转换
            if pu:
                df[[GEN_P, GEN_Q, 'PF', LOAD_P, LOAD_Q, 'SHUNTQ1', 'SHUNTQ2', 'SHUNTQ3']] /= self.mva_base
                # todo pfo中的pf是什么，为什么要标幺化？
                df['SHUNTB'] = df['SHUNTQ1'].copy().add(df['SHUNTQ3']).div(df[VOLTAGE]).div(df[VOLTAGE])
            else:
                print('dat.read_pfo:pu==False,没有计算SHUNTB，可能出错。')
            df[BUS_NAME_STR] = list(map(BNameFormatter.get_name, df[BUS_NAME_STR], df[BUS_BASE_STR]))

            df.index = [self.bus_order[name] for name in df[BUS_NAME_STR]]

            # todo
            #  1. 并不确定如何处理shuntQ
            #  2. 并不确定如何处理恒功率负荷
        elif type=='DSP':
            pfo_lines = open(dat_path, 'rb').readlines()
            # 检查是否收敛：
            key = '不收敛'.encode('gbk')
            for l in pfo_lines:
                if key in l:
                    return None

            # 针对粤西场景，需要提取场景相关线路的功率
            stl = [i for i, l in enumerate(pfo_lines) if '*  节点潮流数据列表'.encode('gbk') in l]
            # 有些潮流结果有问题，但是又不想让程序中断
            if len(stl) == 0:
                return None
            stl = stl[0]
            edl = [i for i, l in enumerate(pfo_lines[stl:]) if '------'.encode('gbk') in l][1] + stl
            r = pfo_lines[stl+1:edl]
            # sstl = []
            #
            # sstl = [i for i, l in enumerate(r) if b'\r\n' == l]
            # if sstl:
            #     sstl = sstl[0] + 1
            # else:
            #     sstl = 0
            tt = []
            for i in range(len(r)):
                s = r[i]#每一行
                if s[0:7] !=b'       ':#是首段节点
                    bus1_name = s[0:8].replace(b' ',b'').decode('gbk', errors='ignore')
                    bus1_base = s[9:14].replace(b' ',b'').decode('gbk', errors='ignore')
                    bus1_V = s[16:22].replace(b' ',b'').decode('gbk', errors='ignore')
                    bus1_theta = s[26:32].replace(b' ',b'').decode('gbk', errors='ignore')
                elif s[7:15] !=b'        ' and '直流'.encode('gbk') not in s:#是末端节点
                    bus2_name = s[7:15].replace(b' ',b'').decode('gbk', errors='ignore')
                    bus2_base = s[16:21].replace(b' ',b'').decode('gbk', errors='ignore')
                    line_flag = s[23:24].replace(b' ',b'').decode('gbk', errors='ignore')#支路并联号
                    P_line = s[37:44].replace(b' ',b'').decode('gbk', errors='ignore') #支路有功
                    Q_line = s[52:60].replace(b' ',b'').decode('gbk', errors='ignore') #支路无功
                    tt.append([bus1_name,bus1_base,bus1_V,bus1_theta,bus2_name,bus2_base,line_flag,P_line,Q_line])
                else:
                    pass
            df = pd.DataFrame(tt)
        return df.sort_index()

    def get_branch_y(self):
        if self.branch_y is not None:
            return self.branch_y
        n_line = len(self.branch_order)
        y = np.zeros([n_line, 4], dtype=np.complex_)
        for l in self.branch:
            try:
                y[l.order, :] += l.get_y()
            except:
                print('线路导纳没有被正确计算' + str(l))
        self.branch_y = y
        return self.branch_y

    def get_Y_matrix(self):
        """
        2021年11月4日 已与matpower所用的Ybus核对过一致。
        matlab: y = makeYbus(case39())
        @return:
        """
        if self.y_matrix is not None:
            return self.y_matrix
        # 需要 bus_dict{name: index}, line_dict
        n_bus = len(self.bus_order)
        n_line = len(self.branch_order)

        y = np.zeros([n_bus, n_bus], dtype=np.complex_)
        by = self.get_branch_y()
        for l in self.branch:
            try:
                idx = l.order
                bus1 = l.order1
                bus2 = l.order2
                y[bus1, bus1] += by[idx, 0]
                y[bus1, bus2] += by[idx, 1]
                y[bus2, bus1] += by[idx, 2]
                y[bus2, bus2] += by[idx, 3]
            except ValueError:
                print(l.name, ' is ignored. Line: ', str(l))

        self.y_matrix = y

        coo_mask = [[i, i] for i in range(n_bus)]
        coo_mask.extend([[self.branch_indexs[l][0].order1, self.branch_indexs[l][0].order2]
                         for l in self.branch_name])
        coo_mask.extend([[self.branch_indexs[l][0].order2, self.branch_indexs[l][0].order1]
                         for l in self.branch_name])

        self.coo_mask = np.array(coo_mask, dtype=np.int_).transpose()
        self.line_loc_in_coo = np.array([[n_bus + i, n_bus + n_line + i] for i in range(n_line)], dtype=np.int_)

        return self.y_matrix

    @staticmethod
    def build_from(path):
        """
        从文件夹或者文件中新建实例,如果是从文件夹，只会找文件夹中第一个出现的。
        :param path:
        :return:
        """
        if os.path.isfile(path):
            if '.dat' in path.lower():
                lines = open(path, 'rb').readlines()
                return DAT.build_from_lines(lines)
        elif os.path.isdir(path):
            for f in os.listdir(path):
                if '.dat' in f.lower():
                    lines = open(path + '/' + f, 'rb').readlines()
                    return DAT.build_from_lines(lines)
        raise ValueError('cannot find .dat file in path!')

    @staticmethod
    def std_dat(dat_path):
        # for f in os.listdir(folder_path):
        #     if '.dat' in f.lower():
            lines = open(dat_path, 'rb').readlines()
            lines = [bpa_card_line(line) for line in lines]
            dat_path = dat_path.replace('.DAT','_std.DAT')
            dat_path = dat_path.replace('.dat', '_std.dat')
            pathn = dat_path
            with open(pathn,'w') as filen:
                for linen in lines:
                    linen = str(linen, 'gbk')+'\n'
                    filen.write(linen)
            print('std=====>',pathn)
            filen.close()
            return pathn

    @staticmethod
    def build_from_lines(ll: List[str]):
        #ready_for_encoder:如果是解析后为修改DAT做准备，
        lines = []
        can = []
        cc1 = []
        cdt = []
        cc2 = []

        position = 1

        ll = [bpa_card_line(line) for line in ll]
        for i, l in enumerate(ll):
            if l == b'\n':
                lines.append('\n')
                continue

            c = _to_card(l, bpa_annotation.card_types)
            if c:
                lines.append(c)
                can.append(i)
                continue

            c = _to_card(l, bpa_dat_before_data.card_types)
            if c:
                lines.append(c)
                cc1.append(i)
                continue

            c = _to_card(l, bpa_dat_data.card_types)
            if c and position:
                lines.append(c)
                cdt.append(i)
                continue
            else:
                position = 0

            c = _to_card(l, bpa_dat_before_data.card_types)
            if c:
                lines.append(c)
                cc2.append(i)
                continue

            # raise ValueError('unknown bline!')
            print('unknown bline!: ', l)
            position = 1

        return DAT(lines, can, cc1, cdt, cc2)


def _bus_has_gen(bus: _OneNameUid):
    """
    作用:判断这个bus是否有发电机.
    DAT文件里面，并没有明确指出发电机，所以只能我们自己根据节点卡判断.
    怎么判断呢？就是检查这个bus类是否具有GEN_P这个字段，如果有，并且GEN_P这个字段对应的值不为0，那么就认为这个bus存在发电机。
    之所以要重复判断，是考虑到我们以后可能会开机但不安排有功无功
    @param bus:
    @return:
    """
    if (GEN_P in bus.field_index and bus.get_value(GEN_P)) \
            or (GEN_P_MAX in bus.field_index and bus.get_value(GEN_P_MAX)) \
            or (GEN_Q_MIN in bus.field_index and bus.get_value(GEN_Q_MIN)) \
            or (GEN_Q_MAX in bus.field_index and bus.get_value(GEN_Q_MAX)):
        return True
    return False

