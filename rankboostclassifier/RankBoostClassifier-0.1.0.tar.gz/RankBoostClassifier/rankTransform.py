import pandas as pd
from scipy.stats import rankdata
import pickle as pkl
import numpy as np
import os

def read_pickle_file(file_path):
    with open(file_path, 'rb') as f:
        return pkl.load(f)

def rank_transform_exp(feats):
        '''converts features to exp ranks'''
        rows = []
        cols = list(feats.columns)
#       ind = list(feats.index)
        for ind in feats.index.to_list():
                c_r = []
                for col in cols:
                        c_r.append(feats.loc[ind,col])
                k = len(cols)
                rows.append([int(x)*np.exp(-1*(int(x)/k)) for x in rankdata(c_r)])
        feats = pd.DataFrame(rows)
        feats.columns = cols
#       feats.index = ind
        return feats

def rank_transform(feats):
        '''converts features to ranks'''
        rows = []
        cols = list(feats.columns)
#       ind = list(feats.index)
        for ind in feats.index.to_list():
                c_r = []
                for col in cols:
                        c_r.append(feats.loc[ind,col])
                rows.append([int(x) for x in rankdata(c_r)])
        feats = pd.DataFrame(rows)
        feats.columns = cols
#       feats.index = ind
        return feats

def rank_transform_de_exp(feats, path):
        '''converts DE gene features to ranks'''
        de_gene_dic = read_pickle_file(path)

    # get gene rank in each celltype
        rows = []
        cols = list(feats.columns)
#       ind = list(feats.index)
        for ind in feats.index.to_list():
                de_gene_value_dic = {x:{y:0 for y in de_gene_dic[x]} for x in de_gene_dic}
                de_gene_rank_dic = {x:{y:0 for y in de_gene_dic[x]} for x in de_gene_dic}
                c_r = []
#               print(de_gene_value_dic)
                for col in cols:
                        c_r.append(feats.loc[ind,col])
                        for x in de_gene_value_dic:
                                if col in de_gene_value_dic[x]:
                                        de_gene_value_dic[x][col] = feats.loc[ind,col]
                for x in de_gene_rank_dic:
                        de_gene_rank_dic[x] = {key: rank for rank, key in enumerate(sorted(de_gene_value_dic[x], key=de_gene_value_dic[x].get, reverse=True), 1)}

                for x in de_gene_rank_dic:
                        di = de_gene_rank_dic[x]
                        for i,col in enumerate(cols):
                                if col in di:
                                        denom = de_gene_rank_dic[x][col] * np.exp((-1*de_gene_rank_dic[x][col])/len(de_gene_rank_dic[x]))
                                        c_r[i]/=denom
                rows.append(c_r)
        feats = pd.DataFrame(rows)
        feats.columns = cols
#       feats.index = ind
        return feats

def rank_transform_de(feats, path):
        '''converts DE gene features to ranks'''
        de_gene_dic = read_pickle_file(path)

    # get gene rank in each celltype
        rows = []
        cols = list(feats.columns)
#       ind = list(feats.index)
        for ind in feats.index.to_list():
                de_gene_value_dic = {x:{y:0 for y in de_gene_dic[x]} for x in de_gene_dic}
                de_gene_rank_dic = {x:{y:0 for y in de_gene_dic[x]} for x in de_gene_dic}
                c_r = []
#               print(de_gene_value_dic)
                for col in cols:
                        c_r.append(feats.loc[ind,col])
                        for x in de_gene_value_dic:
                                if col in de_gene_value_dic[x]:
                                        de_gene_value_dic[x][col] = feats.loc[ind,col]
                for x in de_gene_rank_dic:
                        de_gene_rank_dic[x] = {key: rank for rank, key in enumerate(sorted(de_gene_value_dic[x], key=de_gene_value_dic[x].get, reverse=True), 1)}

                for x in de_gene_rank_dic:
                        di = de_gene_rank_dic[x]
                        for i,col in enumerate(cols):
                                if col in di:
                                        c_r[i]/=de_gene_rank_dic[x][col]
                rows.append(c_r)
        feats = pd.DataFrame(rows)
        feats.columns = cols
        feats.index = ind
        return feats
