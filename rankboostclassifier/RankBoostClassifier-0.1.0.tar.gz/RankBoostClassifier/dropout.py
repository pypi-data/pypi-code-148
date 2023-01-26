import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def fit_regression(E, D):
        clf = LinearRegression()
        if (np.sum(np.isnan(E)) > 1):
                print("Error")
                return 1, 0
        if (np.sum(np.isnan(D)) > 1):
                print("Error2")
                return 1, 0
        clf.fit(np.reshape(E, (E.shape[0], 1)), D)
        return (clf.coef_, clf.intercept_)

def calc_dropout(df):
        pg = []
        for col in df:
                pg.append(np.sum(df[col] == 0)/len(df))
        pg = np.array(pg)
        return pg

def get_prob_of_less_than(val, k):
        if np.random.random() < k:
                return 0
        else:
                return val
        
def inductive_dropout(df, f=0.5):
        p_g = calc_dropout(df)
        p_g[p_g <= 0] = 1e-6
        p_g[p_g >= 1] = 1 - 1e-6
        D_g = np.log(p_g/(1-p_g))
        R_g = np.array([df[col].mean() for col in list(df.columns)])
        E_g = np.log2(R_g + 1)
        beta, alpha = fit_regression(E_g, D_g)

        E_g_prime = f * E_g
        delta_g = beta*(E_g_prime - E_g)
        D_g_prime = D_g + delta_g

        p_g_prime = 1/ (1 + np.exp(-1*D_g_prime))
        R_g_prime = np.power(2, E_g_prime) - 1

        for i in range(len(df.columns)):
                df[df.columns[i]] = df[df.columns[i]].apply(lambda x : get_prob_of_less_than(x, p_g_prime[i]-p_g[i]))
                R_g_i = np.mean(df[df.columns[i]])
#               df[df.columns[i]] += R_g_i - R_g_prime[i]
                df[df.columns[i]] *= (R_g_prime[i]/(R_g_i + 1e-4))
        return df

def apply_dropout2(data, celltypes, f_list):
        """
        INPUT:
                data: dataframe containing cell-gene expression matrix
                celltype: pd series of cell types
                f: dropout concentration
        """
        new_df = pd.DataFrame(data.copy())
        celltypes = celltypes.tolist()
        new_celltypes = celltypes*(len(f_list) + 1)
        for f in f_list:
                new_data = inductive_dropout(data.copy(), f)
                new_df = pd.concat((new_df, new_data))
        new_df['celltype'] = new_celltypes
        return new_df

def apply_dropout(data, celltypes, n_iter, f = 0.8):
        """
        INPUT:
                data: dataframe containing cell-gene expression matrix
                n_iter: no of times to apply dropout
                f: dropout concentration
        """
        new_df = pd.DataFrame(data.copy())
        celltypes = celltypes.tolist()
        new_celltypes = celltypes*(n_iter + 1)
        for i in range(n_iter):
                data = inductive_dropout(data.copy(), f)
                new_df = pd.concat((new_df, data))
        new_df['celltype'] = new_celltypes
        return new_df