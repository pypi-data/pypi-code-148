import numpy as np
import pandas as pd
import altair as alt

from scipy import stats
from tabulate import tabulate


def initialize_helper():
    """
    A function to enable plotting for large data sets.
    """
    alt.data_transformers.enable('data_server')


def num_dist_by_cat(num, cat, data, title_hist='', title_boxplot='', lab_num=None, lab_cat=None, num_on_x=True,
                    stat=True):
    """
    Create a pair of charts showing the distribution of the numeric variable and when grouped by the categorical variable.
    The one of the left is a histogram while the one on the left will be a boxplot on top of a violin plot.
    Basic test statistics will be printed for user reference.

    Parameter
    ---------
    num: string
        Column name for the numeric variable.
    cat: string
        Column name for the categorial variable.
    data: pandas.DataFrame
        Target data frame for visualization.
    title_hist: string, default ''
        Title for the histogram.
    title_boxplot: string, default ''
        Title for the boxplot
    lab_num: string
        Axis label for the numeric variable.
    lab_cat: string
        Axis label for the categorical variable.
    num_on_x: boolean, default True
        Whether the numeric variable is put on the x-axis in the boxplot.
    stat: boolean, default True
        Whether printing the test statistics and summary or not.
    
    Return
    ------
    altair.Chart
        A concatenated chart consists of a histogram and a boxplot.
    string
        Test statistics
    """
    hist = alt.Chart(data, title=title_hist).mark_bar().encode(
        x=alt.X(num, bin=alt.Bin(maxbins=20), title=lab_num),
        y=alt.Y('count()', title=lab_cat)
    ).properties(
        height=300,
        width=300
    )
    
    if num_on_x == True:
        boxplot = alt.Chart(data, title=title_boxplot).mark_boxplot(size=50).encode(
            x=alt.X(num, scale=alt.Scale(zero=False), title=lab_num),
            y=alt.Y(f'{cat}:N', title=lab_cat)
        ).properties(
            height=300,
            width=300
        )
    else:
        boxplot = alt.Chart(data, title=title_boxplot).mark_boxplot(size=50).encode(
            y=alt.Y(num, scale=alt.Scale(zero=False), title=lab_num),
            x=alt.X(f'{cat}:N', title=lab_cat)
        ).properties(
            height=300,
            width=300
        )
    
    group_list = data[cat].unique()
    n_group = len(group_list)
    
    if n_group == 0:
        print('Please use a data frame with data inside.\n')
    elif n_group == 1:
        print('Please consider using prelim_eda_helper.num_dist when only 1 class is used\n.')
    elif stat == True:
        if n_group == 2:
            if np.var(data[num]) == 0:
                print('A t test is not performed as the total variance is 0.\n')
            else:
                group_a = data[data[cat] == group_list[0]]
                group_b = data[data[cat] == group_list[1]]
                t_eq, p_eq = stats.ttest_ind(group_a[num], group_b[num])
                t_w, p_w = stats.ttest_ind(group_a[num], group_b[num], equal_var=False)
                table = [['Equal var. assumed', f'{t_eq:.2f}', f'{p_eq:.4f}'], ['Equal var. not assumed', f'{t_w:.2f}', f'{p_w:.4f}']]
                print(f'A t-test assuming equal variance yields a t value of {t_eq:.2f} with a p-value of {p_eq:.4f}.')
                print(
                    f'Assuming inequal variances, the Welch\'s t-test yields a t value of {t_w:.2f} with a p-value of {p_w:.4f}.')
                print(tabulate(table, headers=['Test', 't', 'p']))
        elif n_group > 2:
            vectors = dict()
            for i in group_list:
                vectors[i] = data[data[cat] == i][num]
            if (np.array([np.var(i) for i in list(vectors.values())]) == 0).any():
                print('F statistic is not defined when within group variance is 0 in at least one of the groups.\n')
            else:
                F, p = stats.f_oneway(*[list(i) for i in vectors.values()])
                table = [['One-way ANOVA', F, p]]
                print(f'An one-way ANOVA yields an F score of {F:.2f} with a p-value of {p:.4f}.')
                print(tabulate(table, headers=['Test', 'F', 'p']))
        print()
    
    return hist | boxplot


def num_dist_scatter(num1, num2, data, title='', stat=False, trend=None):
    '''
    Creates a scatter plot given two numerical features. Plot can provide regression trendline as linear, polynomial, or loess.
    Statistics such as number of NaNs, mean, median, and standard deviations will be returned as options.
    Spearman and Pearson's correlation will also be returned to aid the user to determining feature relationship.

    Parameter
    ---------
    num1: string
        Name of the column for the first numeric feature.
    num2: string
        Name of the column for the second numeric feature.
    data: pandas.DataFrame
        Target data frame for visualization.
    title: string, default ''
        Title for the chart.
    stat: bool, default False
        Boolean to provide simple statistics.
    trend: string, default None
        Type of trendline. Options are: 'None', lin', 'poly'.
    
    Return
    ------
    altair.Chart
        A chart consists of a scatterplot with out without trendlines.
    string
        Spearman and Pearson's correlation numbers.
    '''
    data1 = data.copy()
    # check if feature is numeric
    assert data[num1].dtype.kind in 'iufc', 'num1 column must be numeric!'
    assert data[num2].dtype.kind in 'iufc', 'num2 column must be numeric!'
    assert data[num1].nunique() != 1, 'num1 column is constant, consider using functions for categorical variables'
    assert data[num2].nunique() != 1, 'num1 column is constant, consider using functions for categorical variables'
    
    # feature statistics
    stats_df = pd.DataFrame()
    feat_list = [num1, num2]
    
    for i in feat_list:
        output = []
        output.append(data[i].isna().sum())
        output.append(round(np.mean(data[i]), 3))
        output.append(np.median(data[i]))
        output.append(round(np.std(data[i], ddof=1), 3))  # calculates sample standard deviation
        stats_df[i] = output
    
    stats_df = stats_df.T.rename(columns={0: 'Num NaN', 1: 'Mean', 2: 'median', 3: 'Stdev'})
    if stat == True:
        print(stats_df)
    
    # replace NaN (if any) with mean column value
    if stats_df.iloc[0, 0] != 0:
        data1[num1] = data1[num1].fillna(stats_df.iloc[0, 1])
        print(f'**num1 NaN replaced with mean {stats_df.iloc[0, 1]:.2f}**')
    if stats_df.iloc[1, 0] != 0:
        data1[num2] = data1[num2].fillna(stats_df.iloc[1, 1])
        print(f'**num2 NaN replaced with mean {stats_df.iloc[1, 1]:.2f}**')
    
    # correlation statistics
    pear = stats.pearsonr(data1[num1], data1[num2])[0]
    pear_p = stats.pearsonr(data1[num1], data1[num2])[1]
    spear = stats.spearmanr(data1[num1], data1[num2]).correlation
    spear_p = stats.spearmanr(data1[num1], data1[num2]).pvalue
    
    table = [ [ 'Pearson\'s', f'{pear:.2f}', f'{pear_p:.4f}'], [ 'Spearman\'s', f'{spear:.2f}', f'{spear_p:.4f}']]
    #print(f"The Pearson's correlation is {pear:.2f} with p-value of {pear_p:.4f}.")
    #print(f"The Spearman's correlation is {spear:.2f} with p-value of {spear_p:.4f}.")
    print( tabulate( table, headers = [ '', 'Correlation', 'p']))
    
    # scatter plot
    scatter = alt.Chart(data1).mark_point(opacity=0.8).encode(
        alt.X(num1, title=num1, scale=alt.Scale(zero=False)),
        alt.Y(num2, title=num2, scale=alt.Scale(zero=False))
    ).properties(
        height=300,
        width=300,
        title=title
    )
    
    # linear regression line
    lr = scatter.mark_line(size=2, color='red').transform_regression(
        num1, num2)
    
    # polynomial line
    poly = scatter.mark_line(size=3, color='red').transform_regression(
        num1, num2, method='poly')
    
    # loess line, 'locally estimated scatterplot smoothing'
    loess = scatter.mark_line(size=3, color='red').transform_loess(
        num1, num2)
    
    if trend == 'lin':
        plot = scatter + lr
    elif trend == 'poly':
        plot = scatter + poly
    elif trend == 'loess':
        plot = scatter + loess
    else:
        plot = scatter
    
    return plot


def cat_dist_heatmap(cat_1, cat_2, data, title=None,
                     lab_1=None, lab_2=None, heatmap=True, barchart=True):
    """
    Create concatenated charts showing the heatmap of two categorical variables and the bar charts for occurrence of
    these variables.
    Heatmap will be on the left and the two bar charts will be on the right in the same column.

    Parameter
    ---------
    cat_1: string
        Name of the column name for the first categorical variable.
    cat_2: string
        Name of the column name for the second categorical variable.
    data: pandas.DataFrame
        Target data frame for visualization.
    title: string, default ''
        Title for the chart.
    lab_1: string
        Axis label for the first categorical variable (x-axis).
    lab_2: string
        Axis label for the second categorical variable (y-axis).
    heatmap: boolean, default True
        Whether to include a heatmap plot or not.
    barchart: boolean, default True
        Whether to include the barchart or not.

    Return
    ------
    altair.Chart
        A concatenated chart consists of a heatmap and 2 bar charts.
    """
    # Sanity check
    n_rows = data.shape[0]
    if n_rows < 1:
        raise Exception(f"Dataset must have at least one row of data.")
    if data[cat_1].nunique() == n_rows:
        raise Exception(f"{cat_1} does not appear to be a valid categorical column. Please double check the input.")
    if data[cat_2].nunique() == n_rows:
        raise Exception(f"{cat_2} does not appear to be a valid categorical column. Please double check the input.")
    
    # # Alternative option: check if the column has category datatype, but it won't fit in our test dataframe
    # categorical_columns = data.select_dtypes(include='category').columns
    # if data[cat_1].name not in categorical_columns:
    #     raise Exception(f"{cat_1} does not appear to be a valid categorical column. Please double check the input.")
    # if data[cat_2].name not in categorical_columns:
    #     raise Exception(f"{cat_2} does not appear to be a valid categorical column. Please double check the input.")
    
    if not title:
        title = f"{cat_1} vs. {cat_2}"
    if not lab_1:
        lab_1 = cat_1
    if not lab_2:
        lab_2 = cat_2
    cat_heatmap = alt.Chart(data).mark_rect().encode(
        x=alt.X(cat_1, axis=alt.Axis(title=lab_1)),
        y=alt.Y(cat_2, axis=alt.Axis(title=lab_2)),
        color='count()').properties(
        height=300,
        width=300
    )
    cat_barcharts = alt.Chart(data).mark_bar().encode(
        x='count()',
        y=alt.X(cat_1, axis=alt.Axis(title=lab_1)),
        color=alt.Color(cat_1, legend=alt.Legend(title=lab_1))
    ).facet(
        row=alt.Facet(cat_2, title=lab_2)
    )
    if heatmap and barchart:
        concat_chart = alt.hconcat(cat_heatmap, cat_barcharts, title=title)
        return concat_chart
    elif heatmap:
        return cat_heatmap
    elif barchart:
        return cat_barcharts
    else:
        raise Exception("At least one of the plot options (heatmap or barchart) needs to be selected (set to TRUE).")


def num_dist_summary(num, data, title='', lab=None, thresh_corr=0.0, stat=True):
    """
    Create a distribution plot of the numeric variable in general and statistical summary of the feature.
    In addition, the correlation values of the input variable with other features based on a threshold will also be returned.

    Parameter
    ---------
    num: string
        Name of the column name for the numeric variable.
    data: pandas.DataFrame
        Target data frame for visualization.
    title: string, default ''
        Title for the chart.
    lab: string
        Axis label for the numeric variable.
    thresh_corr: Float, default 0.0
        value to check for correlation
    stat : Boolean , default True
        whether to print summary statistic or not
    
    Return
    ------
    altair.Chart and Table
        A histogram chart 
    string
         correlation values to other features and Summary statistics 
    """
    ## check if data is present
    if data.shape[0] ==0 : 
        return 'Please use a data frame with data inside.'
    
    ## check if thresh_corris numeric 
    if  not isinstance(thresh_corr, (int, float,  complex)) : 
        return 'Please use a numeric value for threshold'
    
    ## check if title is string
    if not isinstance(title, str) :
        return "Please enter the title as string"
    
    ## check if stat is boolean 
    if not isinstance(stat, bool) :
        return "Please enter the value for stat be  as boolean true or false"
    
    
    ## check if label is string 
    if lab != None and ( not isinstance(lab, str)) : 
        return "Please enter axis label as string"
    

    column_names = data.columns.tolist()
    numeric_col = data.select_dtypes(include=np.number).columns.tolist()
    if  not isinstance(num, str) :
        return "Please enter the column name as string"
    if  num not in column_names :
        return  num +  " not present in the dataset"
    elif num  not in numeric_col : 
        return num + " is not a numeric feature " 
    else : 
        hist = alt.Chart(data , title = title).mark_bar().encode(
            x = alt.X(num, bin = alt.Bin(maxbins = 20), title = lab),
            y = alt.Y( 'count()', title = 'Count')
        ).properties(
            height = 300,
            width = 300
        )

        ## find the correlation values based on the threshold and add them to the chart 
        corr_list = [["Feature ", "Correlation value"]]
        for col in numeric_col : 
            r = data[num].corr(data[col])
            if r >= thresh_corr  and r != 1: 
                out = [col , round(r,2)]
                corr_list.append(out)
        
                
        if len(corr_list) > 1  : 
            print(f"These features below are possibly correlated with {num}:","\n")
            print(tabulate(corr_list,headers='firstrow') ,"\n") 

        if stat == True : 
            mean = data[num].mean()
            median = data[num].median()
            std = data[num].std()
            print("Statistical Summary is as : ")
            stat = [['mean', f'{mean:.2f}'], ['median', f'{median:.2f}'],['standard deviated', f'{std:.2f}'] ]
            print(tabulate(stat) ,"\n") 
        return hist
