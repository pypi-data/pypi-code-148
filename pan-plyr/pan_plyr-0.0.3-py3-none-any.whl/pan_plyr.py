
import pandas as pd
import numpy as np
import pandas as pd
from sqlite3 import connect
import sqlite3
import re



class pan_plyr:
    
    def __init__(self, df):
        """
        Initializes the class with a dataframe and creates a SQLite connection
        """
        self.df = df
        self.con = sqlite3.connect(':memory:')
        self.df.to_sql('df', self.con)
        self.query = 'SELECT * FROM df'
        self.query_exp = 'SELECT * FROM df'

        ## group by

    def group_by(self,group_var=None):
        """
        Groups the dataframe by the specified column
        
        Args:
            group_var: The column name to group the dataframe by
        
        Returns:
            self: the pan_plyr object with the grouped dataframe
        
        Example:
            df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8],'C': ['a','b','c','d']})
            pp = pan_plyr(df)
            op.group_by("C")
        """
        self.df = self.df.groupby(group_var)
        return self        
        
        
    def sort_by(self, column, ascending=True):
        
         """
        Sorts the dataframe by the specified column
        
        Args:
            column: The column name to sort the dataframe by
            ascending: A boolean value specifying the sorting order. Default value is True for ascending order.
        
        Returns:
            self: the pan_plyr object with the sorted dataframe
        
        Example:
            df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8],'C': ['a','b','c','d']})
            pp = pan_plyr(df)
            op.sort_by("A", False)
        """

         self.df = self.df.sort_values(by=column, ascending=ascending)
         return self   


    def select(self, *columns):
        """
        Selects specified columns from the dataframe
        
        Args:
            columns: The column names to select from the dataframe. This can be passed as multiple arguments.
        
        Returns:
            self: the pan_plyr object with the selected columns
        
        Example:
            df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8],'C': ['a','b','c','d']})
            pp = pan_plyr(df)
            op.select("A", "C")
        """
        self.df = self.df[list(columns)]
        return self
    
## drop columns
    def drop_col(self, column):
        """
        This method is used to drop a specified column from a DataFrame.

        Parameters:
        column (str): The name of the column to be dropped.

        Returns:
        DataFrame: The updated DataFrame with the specified column removed.

        Example:
        df = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        df_obj = pan_plyr(df)
        df_obj.drop_col("A")
        # The DataFrame now only contains column "B"
        """
        self.df = self.df.drop(columns=column,inplace=False)
        return self

    def rename_col(self,rename_cols):
        '''
        to rename columns, similar to rename in Pandas
        rename_cols: a dictionaray for renaiming the variable
        
        Example: 
        df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8],'C': ['a','b','c','d']})
        pp = pan_plyr(df)
        op.rename_col(
            {
                "A":"A_A",
                "B":"NEW_B_NAME"
            }
        )
        '''
        self.df = self.df.rename(columns=rename_cols)
        return self
    
 
    def filter(self, query):
        ''' 
        filter(query)
        Method to filter the DataFrame based on a given query.

        Parameters:
        query(str): A string containing the query to filter the DataFrame by. 
                    The query should be in the format of a valid pandas query, 
                    using the syntax df.query("column_name operator value")
                    
        Returns:
        - PandasDataFrame: The filtered DataFrame and a pan_plyr object

        df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8],'C': ['a','b','c','d']})
        pp = pan_plyr(df)
        op.filter("A > 2 & B > 7")

        df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8],'C': ['a','b','c','d']})
        pp = pan_plyr(df)
        op.filter("A>2 | C =='d'")
        '''
        self.df = self.df.query(query)
        return self

    
# mutate a new column based on an expression
   
    def mutate(self, expression,new_var_name):
        
        """
        This method allows you to create a new column in your dataframe by applying an expression to existing columns.

        :param new_var_name: str, name of the new column
        :param expression: str, valid pandas expression to create new column
        :return: the pan_plyr object with the new column added to the dataframe

        Example:
        df = pandas.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        pp = pan_plyr(df)
        op.mutate('C', 'A + B')
        op.df
        # Output:
        A B C
        0 1 4 5
        1 2 5 7
        2 3 6 9
        """
        self.df[new_var_name] = self.df.eval(expression,inplace=False)
        return self
    
    # sql mutate with and withouth possibility of group by
    def sql_mutate(self,new_var, expression, group_var=None):
        """
        Creates a new variable in the dataframe by performing a SQL mutate operation on an existing variable or an expression.
        
        Parameters:
        expression (str): The expression to be evaluated. This can be a single column name or an expression involving multiple columns.
        new_var (str): The name of the new variable to be created.
        group_var (str, optional): The column to group by. If not provided, the expression will be evaluated for the entire dataframe.
        
        Returns:
        self: The pan_plyr object with the new variable added to the dataframe.
        
        Example:
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        pp = pan_plyr(df)
        op.sql_mutate('x + y', 'sum')
        print(op.df)
        # Output:
        #    x  y  sum
        # 0  1  4   5
        # 1  2  5   7
        # 2  3  6   9
        """
        if group_var is None:
            self.query = f'SELECT *, ({expression}) as {new_var} FROM ({self.query})'
        else:
            self.query = f'SELECT *, ({expression}) as {new_var} FROM ({self.query}) GROUP BY {group_var}'
        
        self.df = pd.read_sql(self.query, self.con)
        return self
            
# write any sql expression on the data frame fed to pplyr          
    def sql_plyr(self,expression):

        """
        This method allows to perform SQL queries on the dataframe using the SQLite connection. 
        The resulting dataframe is updated with the query results.
        When refering to the datat frame inside the query, you should use 'df' no matter what the name of your
        dataframe is.
        
        Parameters:
        expression (str): SQL expression to be executed
        
        Returns:
        pan_plyr: Returns the updated pan_plyr object
        
        Example:
        df_with_a_name = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        pp = pan_plyr(df_with_a_name)
        op.sql_plyr('SELECT * FROM df WHERE x > 2')
        """
        self.query_exp = f'{expression}'
        self.df = pd.read_sql_query(self.query_exp, self.con)
        return self
    
    def case_when(self, cases, target_var):
        '''
        this is similar to case when function of SQL, 
        cases: the conditions is introduced in cases argument in a list of tuples [(),(),...]
        
        target_var: the target_var is the name of new column for the output of case_when
        if you would like to replace an existing column with the results, use it as a target_var
        
        Example: 
        df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [5, 6, 7, 8],'C': ['a','b','c','d']})
        pp = pan_plyr(df)

        op.case_when(
            [
          (" C == 'a' ","AAA"),
          ("C in ('b','c','d')","OTHER"),
            ],
        target_var="new_col"
        ) ## you could also replace new_col with C if you want to change the contents of C
        
        Example 2:
        
        df = pd.DataFrame({'a': [1,2,3,4], 'b':[10,20,30,40]})
        pp = pan_plyr(df)
        (op.case_when(
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
        """
    This method allows to perform groupby and aggregation on the dataframe.

        Parameters:
        group_var (str): The variable to group the dataframe by.
        var (str): The variable to perform the aggregation on.
        agg_func (str or function): The aggregation function to apply to the variable.
        Can be a string for built-in aggregation functions such as 'mean' or 'sum'
        or a user-defined function.

        Returns:
        pan_plyr: Returns the updated pan_plyr object with the summarized dataframe.

        Example:
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6],'z':['a','b','a']})
        pp = pan_plyr(df)
        op.summarize(group_var='z',var='y',agg_func='mean').to_df
        or to apply the agg_func to the whole dataframe
        op.summarize(var='y',agg_func='mean').to_df
        """
        if group_var and var and agg_func:
            self.df = self.df.groupby(group_var)[var].agg(agg_func)
        elif var and agg_func:
            self.df = self.df[var].agg(agg_func)
        return self
        

    def join(self, other_df, by, join_type='inner'):
        '''
        join method to join the df of pplyr to other data frames
        by: the key by which the dataframes can be joined
        join_type: type of the join including 'inner','left', etc 
        
        Example: 
        df1 = pd.DataFrame({'key': ['A', 'B', 'C', 'D'], 'value': [1, 2, 3, 4]})
        df2 = pd.DataFrame({'key': ['B', 'D', 'E', 'F'], 'value': [5, 6, 7, 8]})
        pp = pan_plyr(df1)
        op.join(df2, by='key')
        print(op.to_df)
        '''
        self.df = self.df.merge(other_df, on=by, how=join_type)
        return self
    

    def count_na(self, var=None):
      if var is None:
          # count missing values for all columns
          cols = self.df.columns
      else:
          cols = var
      for col in cols:
          missing_values = self.df[col].isnull().sum()
          if self.df[col].dtype == 'object' or self.df[col].dtype == 'category':
              categories = self.df[col].unique()
              print(f"Column: {col}\n \t **Number of Missing Values: {missing_values}\n\t Categories: {categories}")
          else:
              print(f"Column: {col}\n \t Missing Values: {missing_values}")
    
    def distinct(self, column=None):
        '''
        This will return a new dataframe with only the unique rows of the original dataframe
        that was passed to the pplyr class.
        Example:
        df = pd.DataFrame({'key': ['A', 'B', 'C', 'D'], 'value': [1, 1, 1, 4]})
        pan_plyr(df).distinct('value')
        '''
        self.df = self.df.drop_duplicates(subset=column)
        return self


    def skim(self):
        """
        Summary statistics of a dataframe.

        This method provides a compact overview of the key characteristics of a dataframe. It includes information about data types, missing values, unique values, categories (for categorical variables), minimum and maximum values, mean, median, skewness, standard deviation, 25th, 50th, and 75th percentiles. The output table adjusts its width to display the full content of its columns. 

        Returns:
    -------
        DataFrame: A dataframe with the summary statistics for each column in the original dataframe.

        """
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)
        result = {}
        result['Types'] = self.df.dtypes
        result['Number of Missing Values'] = self.df.isna().sum()
        result['Number of Unique Values'] = self.df.nunique()
        categories = {}
        for col in self.df.columns:
            if self.df[col].dtype == "object" or self.df[col].dtype == "category":
                unique_vals = self.df[col].dropna().unique()
                categories[col] = [f"{i+1}-{val}" for i, val in enumerate(unique_vals)]
        
        result['Categories'] = pd.Series(categories)
        result['Minimum'] = self.df.min()
        result['Maximum'] = self.df.max()
        result['Mean'] = self.df.mean()
        result['Skewness'] = self.df.skew()
        result['Standard Deviation'] = self.df.std()
        result['25th Percentile'] = self.df.quantile(0.25)
        result['50th Percentile'] = self.df.quantile(0.50)
        result['75th Percentile'] = self.df.quantile(0.75)
        
        
        result_df = pd.DataFrame(result).sort_values("Types").fillna(value='-')
        pd.options.display.max_colwidth = 1000

        return result_df
        

    def clean_names(self):
        """
        it cleans the name of variables, 
        """
        self.df.columns = [re.sub('[^0-9a-zA-Z]+', '_', col) for col in self.df.columns]
        self.df.columns = [col.lower() for col in df.columns]
        return self

        
    def __call__(self, df):
        self.df = df
        return self
    
    def __repr__(self):
        return self.df.__repr__()
    
    @property
    def to_df(self):
        """
        @property to_df
        This property allows to convert the dataframe of the pan_plyr object to a standard pandas dataframe.
        It returns a pandas DataFrame object with the same data as the original dataframe.
        Example:
        df_with_a_name = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        pp = pan_plyr(df_with_a_name)
        df = op.to_df
        """
        return pd.DataFrame(self.df)
