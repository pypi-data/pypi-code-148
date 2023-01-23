# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 10:33:40 2023

@author: Jose Ribeiro


"""

import pandas as pd

class ConeXi():
    
    def __init__(self, top_n_rank):
        self.top_n_rank = top_n_rank
    
        
    def ExecuteConeXi(self, df_features_rank):
        df_features_rank_copy = df_features_rank.copy()
        df_features_rank_step1 = df_features_rank.copy()
        features = df_features_rank_copy['att_original_names'] #column names of experts/measures
        features_w = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #weights for each expert/measure.
        col = list(df_features_rank_copy.columns)
        col.remove('att_original_names')
        
        for idl,l in enumerate(features):
          for idc,c in enumerate(col):
            for idp,p in enumerate(df_features_rank_copy.loc[:,c]):
              if l == p:
                if idp >= self.top_n_rank:
                  df_features_rank_step1.loc[idl,c] = 0
                else:
                  df_features_rank_step1.loc[idl,c] = idp+1
        
        
        df_step_1 = df_features_rank_step1.copy()
        
        df_features_rank_step1 = df_features_rank_step1.set_index('att_original_names')
        
            
        # initialize data of lists.
        data = {}
        
        # Creates pandas DataFrame.
        df = pd.DataFrame(data, index=df_features_rank_step1.index)
        
        for idl,l in enumerate(features):
          s_line = 0
          for idc,c in enumerate(col):
            for i in range(1,11):
              if df_features_rank_step1.loc[l,c] <= i and df_features_rank_step1.loc[l,c] !=0 :
                s_line = (s_line + 1) * features_w[idc]
            df.loc[l,'S'] = s_line
        
        df_final = df.sort_values('S',ascending=False)
        return df_final, df_step_1
    
def main():
    
    #Simple example of utilization of ConeXi
    
    d = {'att_original_names': ['f1', 'f2','f3','f4','f5'], 
         'rank1': ['f3', 'f4','f1','f2','f5'],
         'rank2': ['f4','f1','f2','f3','f5'],
         'rank3':['f1','f2','f3','f4','f5']}
    df = pd.DataFrame(data=d)

    
    c = ConeXi(5)
    
    rank_final, data = c.ExecuteConeXi(df)
    
    print(rank_final)
    
if __name__ == "__main__":
    main()
