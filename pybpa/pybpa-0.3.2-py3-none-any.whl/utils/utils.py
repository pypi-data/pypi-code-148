# -*- coding:utf-8 -*-
"""
# Name:         dlgxa: utils
# Author:       MilkyDesk
# Date:         2022/3/10 16:17
# Description:
#   工具函数集合
# 1. 调潮流初始条件
# 2. 保证拓扑的情况下断线
"""

# ------------------------- params --------------------------


# ------------------------- params --------------------------
from typing import Union, Callable

import os
from scipy.stats import norm
from base.bpa_uid import GEN_P, LOAD_P, LOAD_Q, VMAX, GEN_Q, ANGLE
from dat.bpa_dat import DAT
import numpy as np
from numpy import random
import networkx as nx


# LHS要用到的正态分布反函数
from dat.bpa_dat_data import DatBS, DatBV, DatT, DatTP, DatR, DatBQ
from file_organize import DefaultOrganizer

NORM01 = norm(0, 1)
name_pqpqvt = ['LOAD_P', 'LOAD_Q', 'GEN_P', 'GEN_Q', 'VOLTAGE', 'VMAX']
idx_pl, idx_pg, idx_ql, idx_qg, idx_v, idx_t = [DatBV.field_index[LOAD_P], DatBV.field_index[GEN_P],
                                                DatBV.field_index[LOAD_Q], DatBV.field_index[GEN_Q],
                                                DatBV.field_index[VMAX], DatBS.field_index[ANGLE]]


class _DATGenerator:

    def _check_pqpqvt(self, pqpqvt):
        """
        根据dat的节点属性检查pqpqvt是否合法，不合法输出警告。
        :param pqpqvt:
        :return:
        """
        # 发电机、被允许的
        allowed = np.zeros([6, len(self.dat.bus)], dtype=np.bool_)
        # 发电机PV
        for i in self.dat.gen_bus_order:
            allowed[2, i] = True
            allowed[3, i] = True
        # 负荷PQ, 不新增负荷节点
        # 平衡机PQ
        for i, bus in enumerate(self.dat.bus):
            if bus.values[idx_pl] != 0 or bus.values[idx_ql] != 0:
                allowed[0, i] = True
                allowed[1, i] = True
            if isinstance(bus, DatBS):
                allowed[5, i] = True
                allowed[2, i] = False  # 平衡机P不可控

        conflict = []
        for i in range(6):
            for j in range(len(allowed[0])):
                if pqpqvt[i, j] and not allowed[i, j]:
                    conflict.append([name_pqpqvt[i], j])
                    pqpqvt[i, j] = False
        if len(conflict) > 0:
            # print(conflict)
            raise Warning(f'采样设置有误！{conflict}')
        return pqpqvt

    def set_sample_to_dat(self, sample, dat: DAT):
        for i in range(self.n_bus):
            for j in range(6):
                if self.pqpqvt[j, i]:
                    dat.bus[i].set_value(name_pqpqvt[j], sample[j, i], ignore_error=True)
        return dat

    def default_base(self, dat: DAT):
        base = np.zeros([6, len(dat.bus)])  # pl, ql, pg, qg, v, theta
        for i, bus in enumerate(dat.bus):
            base[0, i] = bus.values[idx_pl]
            base[1, i] = bus.values[idx_ql]
            base[2, i] = bus.values[idx_pg] if isinstance(bus, DatBQ) else 0
            base[3, i] = bus.values[idx_qg] if isinstance(bus, DatBQ) else 0
            base[4, i] = bus.values[idx_v] if isinstance(bus, (DatBQ, DatBS)) else 0
            base[5, i] = bus.values[idx_t] if isinstance(bus, DatBS) else 0
        return base

class GridGenerator(_DATGenerator):
    """
    功能：在一个指定dat的基础上进行网格抽样。(与拓扑无关)
    初始化，采样，生成。
    """
    def __init__(self, dat: DAT, pqpqvt: np.ndarray,
                 maxx: Union[float, np.ndarray] = 3, minx: np.ndarray = None):
        self.dat = dat

        self.n_bus = len(dat.bus)
        self.n_gen = len(dat.gen)

        if minx is None:
            self.minx = 0

        if isinstance(maxx, float):
            self.maxx = self.default_base(dat) * maxx
        else:  # maxx: ndarray 表示是绝对值
            self.maxx = maxx

        # 检查和输出
        self.pqpqvt = self._check_pqpqvt(dat, pqpqvt)

        self.mean[self.pqpqvt == False] = 0
        self.std[self.pqpqvt == False] = 0

    def sample(self, n_sample):
        """采样得到pqpqvt格式的样本。(划掉。出于效率考虑目前并不是，因此需要采用自己的set方法
        由于网格采样结果与总采样数量有关，所以需要一次性输出所有采样结果"""
        x = []
        for i in range(len(self.pqpqvt)):
            for j in range(6):
                if self.pqpqvt[i][j]:
                    x.append(np.linspace(self.minx[i][j], self.maxx[i][j], n_sample))
        xs = np.meshgrid(*x)
        xs = [x.reshape(-1) for x in xs]
        xs = np.array(xs)
        return xs.T

    def set_sample_to_dat(self, sample, dat: DAT):
        count = 0
        for i in range(self.n_bus):
            for j in range(6):
                if self.pqpqvt[j, i]:
                    dat.bus[i].set_value(name_pqpqvt[j], sample[count], ignore_error=True)
                    count += 1
        assert count == len(sample)
        return dat


class LHSGenerator(_DATGenerator):
    """
    功能：在一个指定dat的基础上进行抽样。(与拓扑无关)
    初始化，采样，生成。
    """

    def __init__(self, dat: DAT, pqpqvt: np.ndarray, std: Union[float, np.ndarray]=0.1, mean=None,
                 truncate=1.0):
        self.dat = dat
        self.sampler = lhs_sampler_u
        self.truncate = truncate

        self.n_bus = len(dat.bus)
        self.n_gen = len(dat.gen)

        if mean is None:
            self.mean = self.default_base(dat)

        if isinstance(std, float) and std <= 1:
            self.std = self.mean * std
        else:  # std > 1 or std: ndarray 表示是绝对值
            self.std = std

        # 检查和输出
        self.pqpqvt = self._check_pqpqvt(dat, pqpqvt)

        self.mean[self.pqpqvt == False] = 0
        self.std[self.pqpqvt == False] = 0

    def sample(self, n_sample):
        """采样得到pqpqvt格式的样本"""
        return self.sampler(n_sample, self.mean, self.std, self.truncate)


class RandomDatGenerator:
    def __init__(self, n_sample: int, dat: DAT,
                 load: Union[bool, np.ndarray] = False,
                 load_q: Union[bool, np.ndarray] = False,
                 gen: Union[bool, np.ndarray] = False,
                 gen_v: Union[bool, np.ndarray] = False,
                 std: Union[float, list] = 0.1,
                 zero_correct=True):
        self.n_sample = n_sample
        self.dat = dat

        self.zero_correct = zero_correct

        self.n_bus = len(dat.bus)
        self.n_gen = len(dat.gen)
        self.idx_lp = dat.bus[0].field_index[LOAD_P]
        self.idx_lq = dat.bus[0].field_index[LOAD_Q]
        self.idx_gp = dat.bus[0].field_index[GEN_P]
        self.idx_gv = dat.bus[0].field_index[VMAX]

        if type(std) is not list:
            std = [std, std, std, std]

        # 变负荷的情况：load==True，按照dat；load==ndarray，按照load；
        if load:
            self.mean_lp = load if type(load) == np.ndarray else np.array([bus.get_value(LOAD_P) for bus in dat.bus])
            self.std_lp = std[0] * self.mean_lp
            self.lp_level = np.sum(self.mean_lp)
            self.load = True
        else:
            self.load = False

        if load_q:
            self.mean_lq = load_q if type(load_q) == np.ndarray else np.array([bus.get_value(LOAD_Q) for bus in dat.bus])
            self.std_lq = std[1] * np.abs(self.mean_lq)
            self.load_q = True
        else:
            self.load_q = False

        if gen:
            self.mean_gp = gen if type(gen) == np.ndarray else np.array([gen.get_value(GEN_P) for gen in dat.gen])
            self.std_gp = std[2] * self.mean_gp
            self.gen_p = True
        else:
            self.gen_p = False

        if gen_v:
            self.mean_gv = gen_v if type(gen_v) == np.ndarray else np.array([gen.get_value(VMAX) for gen in dat.gen])
            self.std_gv = std[3] * self.mean_gv
            self.gen_v = True
        else:
            self.gen_v = False

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count > self.n_sample:
            raise StopIteration
        self.count += 1

        if self.load:
            sample_lp = random.normal(self.mean_lp, self.std_lp, size=self.n_bus)
            if self.zero_correct:
                sample_lp[sample_lp < 0] = 0
            total_lp = np.sum(sample_lp)
            self.dat.load_level = total_lp / self.lp_level
            for j in range(self.n_bus):
                self.dat.bus[j].values[self.idx_lp] = sample_lp[j]
        else:
            total_lp = np.sum(self.mean_lp)

        if self.load_q:
            sample_lq = random.normal(self.mean_lq, self.std_lq, size=self.n_bus)
            for j in range(self.n_bus):
                self.dat.bus[j].values[self.idx_lq] = sample_lq[j]

        if self.gen_p:
            sample_gp = random.normal(self.mean_gp, self.std_gp, size=self.n_gen)
            if self.zero_correct:
                sample_gp[sample_gp < 0] = 0
            total_gp = np.sum(sample_gp)
            sample_gp = sample_gp / total_gp * total_lp
            for j in range(self.n_gen):
                self.dat.gen[j].values[self.idx_gp] = sample_gp[j]

        if self.gen_v:
            sample_gv = random.normal(self.mean_gv, self.mean_gv, size=self.n_gen)
            for j in range(self.n_gen):
                self.dat.gen[j].values[self.idx_gv] = sample_gv[j]

        return self.dat


def normal_sampler(n_sample, mean, std):
    """

    :param n_sample:
    :param mean:
    :param std:
    :return: shape of (n_sample, len(mean))
    """
    sample = random.normal(mean=mean, std=std, size=(n_sample, len(mean)))
    return sample


def lhs_sampler_u(n_sample, mean, std, truncate=1.0):
    """
    带有截断正态分布的拉丁超立方采样
    :param n_sample:
    :param mean:
    :param std:
    :param truncate:
    :return: shape: (n_sample, mean&std.shape)
    """
    samples = random.uniform(0, truncate / n_sample, size=mean.shape+(n_sample,))\
              + np.linspace((1-truncate)/2, (1+truncate)/2, n_sample, False)
    shape = samples.shape
    samples = samples.reshape(-1, n_sample)
    for i in range(len(samples)):
        np.random.shuffle(samples[i])
    axis = np.arange(len(shape)) - 1
    samples = samples.reshape(shape).transpose(*axis)
    return mean[np.newaxis] + std[np.newaxis] * 2 * (samples - 0.5)

def lhs_sampler_n(n_sample, mean, std, truncate=1.0):
    """
    带有截断正态分布的拉丁超立方采样
    :param n_sample:
    :param mean:
    :param std:
    :param truncate:
    :return: shape: (n_sample, mean&std.shape)
    """
    samples = random.uniform(0, truncate / n_sample, size=mean.shape+(n_sample,))\
              + np.linspace((1-truncate)/2, (1+truncate)/2, n_sample, False)
    shape = samples.shape
    samples = samples.reshape(-1, n_sample)
    for i in range(len(samples)):
        np.random.shuffle(samples[i])
    axis = np.arange(len(shape)) - 1
    samples = NORM01.ppf(samples).reshape(shape).transpose(*axis)
    return mean[np.newaxis] + std[np.newaxis] * samples


class GenLoadGenerator:
    def __init__(self, n_sample: int, dat: DAT,
                 load: Union[bool, np.ndarray] = False,
                 load_q: Union[bool, np.ndarray] = False,
                 gen: Union[bool, np.ndarray] = False,
                 gen_v: Union[bool, np.ndarray] = False,
                 std: Union[float, list] = 0.1,
                 zero_correct=True,
                 gen_load_balance=True,
                 sampler: str = 'normal'):
        self.n_sample = n_sample
        self.dat = dat
        self.zero_correct = zero_correct

        self.n_bus = len(dat.bus)
        self.n_gen = len(dat.gen)
        self.idx_lp = dat.bus[0].field_index[LOAD_P]
        self.idx_lq = dat.bus[0].field_index[LOAD_Q]
        self.idx_gp = dat.bus[0].field_index[GEN_P]
        self.idx_gv = dat.bus[0].field_index[VMAX]

        if sampler == 'normal':
            sampler = normal_sampler
        elif sampler == 'lhs':
            sampler = lhs_sampler_n
        else:
            raise ValueError('sampler!')

        if type(std) is not list:
            std = [std, std, std, std]

        # 变负荷的情况：load==True，按照dat；load==ndarray，按照load；
        if load:
            self.mean_lp = load if type(load) == np.ndarray else np.array([bus.get_value(LOAD_P) for bus in dat.bus])
            self.std_lp = std[0] * self.mean_lp
            self.sample_lp = lhs_sampler_n(n_sample,
                                         mean=self.mean_lp,
                                         std=self.std_lp)
            self.lp_level = np.sum(self.sample_lp, axis=1) / np.sum(self.mean_lp)  # n_sample * 1
            if self.zero_correct:
                self.sample_lp[self.sample_lp < 0] = 0
            self.load = True
        else:
            self.load = False

        if load_q:
            self.mean_lq = load_q if type(load_q) == np.ndarray else np.array([bus.get_value(LOAD_Q) for bus in dat.bus])
            self.std_lq = std[1] * np.abs(self.mean_lq)
            self.sample_lq = lhs_sampler_n(n_sample,
                                         mean=self.mean_lq,
                                         std=self.std_lq)
            self.load_q = True
        else:
            self.load_q = False

        if gen:
            self.mean_gp = gen if type(gen) == np.ndarray else np.array([gen.get_value(GEN_P) for gen in dat.gen])
            self.std_gp = std[2] * self.mean_gp
            self.sample_gp = lhs_sampler_n(n_sample,
                                         mean=self.mean_gp,
                                         std=self.std_gp)
            if gen_load_balance:
                gp_level = self.lp_level / np.sum(self.sample_gp, axis=1)
                self.sample_gp = self.sample_gp * gp_level

            self.gen_p = True
        else:
            self.gen_p = False

        if gen_v:
            self.mean_gv = gen_v if type(gen_v) == np.ndarray else np.array([gen.get_value(VMAX) for gen in dat.gen])
            self.std_gv = std[3] * self.mean_gv
            self.sample_gv = lhs_sampler_n(n_sample,
                                         mean=self.mean_gv,
                                         std=self.std_gv)
            self.gen_v = True
        else:
            self.gen_v = False

        # LHS需要记录分层信息，这超出了iter的处理范围，需要在这里完成


    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count >= self.n_sample:
            raise StopIteration

        if self.load:
            self.dat.load_level = self.lp_level[self.count]
            for j in range(self.n_bus):
                self.dat.bus[j].values[self.idx_lp] = self.sample_lp[self.count, j]

        if self.load_q:
            for j in range(self.n_bus):
                self.dat.bus[j].values[self.idx_lq] = self.sample_lq[self.count, j]

        if self.gen_p:
            for j in range(self.n_gen):
                self.dat.gen[j].values[self.idx_gp] = self.sample_gp[self.count, j]

        if self.gen_v:
            for j in range(self.n_gen):
                self.dat.gen[j].values[self.idx_gv] = self.sample_gv[self.count, j]

        self.count += 1
        return self.dat

def topo_generator(depth, target_depth, dat: DAT, target_root_path, n_sample, generator, candidates=None, graph=None,
                   prefix: list=[], make0=True, lsd_writer=None, op_selector=None, organizer=None):
    """
    命名规则：k_100_B1...BN
    dat第一行：详细信息
    :param depth:
    :param dat:
    :param candidates: 候选列表
    :param generator:
    :param source_root_path:
    :param target_root_path:
    :return:
    """
    # 0. 初始化
    if organizer is None:
        organizer = DefaultOrganizer(target_root_path)
    # 假设已经有了
    if candidates is None:
        candidates = [i for i, b in enumerate(dat.branch) if not (b.is_commented or isinstance(b, (DatT, DatTP, DatR)))]
    if graph is None:
        graph = nx.Graph([dat.branch_bus_order[b] for b in candidates])
    # 视情况决定是否生成 0_xx_0
    if make0:
        samples = generator.sample(n_sample)
        for j, sample in enumerate(samples):
            # 4. 输出文件
            operation_name = organizer.get_op_name(info=j, pre_cut_line_list=prefix)
            generator.set_sample_to_dat(sample, dat)
            dat.save_to_file(organizer.get_dat_path(op_name=operation_name),
                             prefix='.' + ' '.join(['operation_name', 'load_level']) + '\n.'
                                    + ' '.join([operation_name, 'load_level']) + '\n')
            if lsd_writer:
                lsd_writer.write(path=target_root_path + operation_name, op_name=operation_name,
                                 ban_branch=prefix)
    # 1. 搜索
    if depth >= target_depth:
        return

    for i, b in enumerate(candidates):
        # 1. 去掉线路
        graph.remove_edge(*(dat.branch_bus_order[b]))
        dat.branch[b].commented()

        # 2. 检查去掉线路后是否是孤岛，是的话跳到 6
        if nx.is_connected(graph):  # nx.number_connected_components(graph) == 1
            # 3. 调整负荷或发电
            samples = generator.sample(n_sample)
            if op_selector is None or op_selector(dat=dat, depth=depth, target_depth=target_depth, graph=graph,
                                                  branch_order=b, prefix=prefix):
                for j, sample in enumerate(samples):
                    # 4. 输出文件
                    operation_name = organizer.get_op_name(info=j, pre_cut_line_list=prefix + [str(b)])
                    generator.set_sample_to_dat(sample, dat)
                    dat.save_to_file(organizer.get_dat_path(op_name=operation_name),
                                     text_prefix='.' + ' '.join(['operation_name', 'load_level']) + '\n.' + ' '.join(
                                         [operation_name, 'load_level']) + '\n')
                    if lsd_writer:
                        lsd_writer.write(organizer.get_lsd_path(op_name=operation_name),
                                         ban_branch=(prefix + [str(b)]))
                    print(depth+1, '\t', operation_name)
                    # print('debug, prefix, b: ', prefix, b)
            # 5. 下一层拓扑搜索
            if depth + 1 < target_depth:  # 这里已经是输出了depth+1的结果了，因此应该+1
                topo_generator(depth+1, target_depth, dat, target_root_path, n_sample, generator, candidates[(i+1):],
                               graph, prefix + [str(b)], make0=False, lsd_writer=lsd_writer)
        # 6. 接回线路
        graph.add_edge(*(dat.branch_bus_order[b]))
        dat.branch[b].uncommented()


class LSDWriter:

    def __init__(self, full_lsd_path):
        f = open(full_lsd_path, 'r')
        self.lines = f.readlines()
        faults = []
        for i, l in enumerate(self.lines):
            if 'NR_FG' == l[:5]:
                faults.append([i, l[5:].strip().split('-')])  # Fault结构：NR_FG fault_line_order-fault_bus_name
        print(f'num of faults: {len(faults)}, they are: {faults}')
        self.faults = faults

    def write(self, path, op_name, ban_branch=[]):
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path + '/' + op_name + '.lsd', 'w')
        for fault in self.faults:
            if fault[1][0] not in ban_branch:
                f.writelines(self.lines[fault[0]:fault[0]+3])
        f.close()
