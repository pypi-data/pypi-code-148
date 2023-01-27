
import pandas as pd
import numpy as np
import pandas as pd
from sqlite3 import connect
import sqlite3
from importlib import resources
import io 

class pan_plyr:
    def __init__(self, df):
        self.df = df
        self.con = sqlite3.connect(':memory:')
        self.df.to_sql('df', self.con)
        self.query = 'SELECT * FROM df'
        self.query_exp = 'SELECT * FROM df'

        ## group by
    def group_by(self,group_var=None):
        self.df = self.df.groupby(group_var)
        return self        
        
        
    def sort_by(self, column, ascending=True):
        self.df = self.df.sort_values(by=column, ascending=ascending)
        return self   
## select columns
    def select(self, *columns):
        self.df = self.df[list(columns)]
        return self
    
## drop columns
    def drop_col(self, column):
        self.df = self.df.drop(columns=column,inplace=False,suffixes=('_x', '_y'))
        return self

    def rename_col(self,rename_cols):
        '''
        to rename columns, similar to rename in Pandas
        rename_cols =  dictionaray
        
        Example: 
        df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8],'C': ['a','b','c','d']})
        pp = pplyr(df)
        pp.rename_col(
            {
                "A":"A_A",
                "B":"NEW_B_NAME"
            }
        )

        '''
        self.df = self.df.rename(columns=rename_cols)
        return self
    
# filter rows by a query 
    def filter(self, query):
        self.df = self.df.query(query)
        return self

    
# mutate a new column based on an expression
   
    def mutate(self,new_var_name, expression):
        self.df[new_var_name] = self.df.eval(expression,inplace=False)
        return self
    
    # sql mutate with and withouth possibility of group by
    def sql_mutate(self,expression,new_var, group_var=None):
        if group_var is None:
            self.query = f'SELECT *, ({expression}) as {new_var} FROM ({self.query})'
        else:
            self.query = f'SELECT *, ({expression}) as {new_var} FROM ({self.query}) GROUP BY {group_var}'
        
        self.df = pd.read_sql(self.query, self.con)
        return self
            
# write any sql expression on the data frame fed to pplyr          
    def sql_exp(self,expression):
        self.query_exp = f'{expression}'
        self.df = pd.read_sql_query(self.query_exp, self.con)
        return self
    

    def case_when(self, cases, target_var):
        '''
        this is similar to case when function of SQL, 
        cases: the conditions is introduced in cases argument in a list of tuples [(),(),...]
        target_var: the target_var is the name of new column for the output of case_when
        if you would like to replace an existing column with the results, use it as a target_var
        Example 1: 
        df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8],'C': ['a','b','c','d']})
        pp = pplyr(df)

        pp.case_when(
            [
          ("C == 'a'","AAA"),
          ("C in ('b','c','d')","OTHER"),
            ],
        target_var="new_col") ## you could also replace new_col with C if you want to change the contents of C
        
        Example 2:
        
        df = pd.DataFrame({'a': [1,2,3,4], 'b':[10,20,30,40]})
        pp = pplyr(df)
        (pp.case_when(
            [
                ('a > 2', round(333.333,1)),
                ('b < 25', np.mean(df['b']))
            ],target_var="new_col")
        )
        
        '''
        if target_var is None:
            self.df[target_var] = np.nan # initialize new variable as NaN
            for cond, val in cases:
                self.df.loc[self.df.eval(cond), target_var] = val
        else:
            for cond, val in cases:
                self.df.loc[self.df.eval(cond), target_var] = val
        return self

    
    def summarize(self,group_var=None, var=None, agg_func=None):
        if group_var and var and agg_func:
            self.df = self.df.groupby(group_var)[var].agg(agg_func)
        elif var and agg_func:
            self.df = self.df[var].agg(agg_func)
        return self
        

    def join(self, other_df, by, join_type='inner'):
        '''
        join method to join the df of pplyr to other data frames
        by: the key by which the dataframes can be joined
        join_type: including 'inner','left', etc 
        
        Example: 
        df1 = pd.DataFrame({'key': ['A', 'B', 'C', 'D'], 'value': [1, 2, 3, 4]})
        df2 = pd.DataFrame({'key': ['B', 'D', 'E', 'F'], 'value': [5, 6, 7, 8]})
        pp = pplyr(df1)
        pp.join(df2, by='key')
        print(pp.to_df)
        '''
        self.df = self.df.merge(other_df, on=by, how=join_type)
        return self
    
    
    def distinct(self, column=None):
        '''
        This will return a new dataframe with only the unique rows of the original dataframe
        that was passed to the pplyr class.
        Example:
        df = pd.DataFrame({'key': ['A', 'B', 'C', 'D'], 'value': [1, 1, 1, 4]})
        pplyr(df).distinct('value')
        '''
        self.df = self.df.drop_duplicates(subset=column)
        return self
        
    def __call__(self, df):
        self.df = df
        return self
    
    def __repr__(self):
        return self.df.__repr__()
    
    @property
    def to_df(self):
        return pd.DataFrame(self.df)
