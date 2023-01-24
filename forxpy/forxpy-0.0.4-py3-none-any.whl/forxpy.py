import os
import pandas as pd
import altair as alt
from datetime import datetime
import re

def retrieve_data(export_csv = False):

    """
    Retrieve historical daily currency exchange rates data for Canadian Dollar 
    in CSV format from Bank of Canada website. 
    The function pre-processes and cleans the data to transform it into a more usable format.     
    
    Parameters
    ----------
    export_csv : bool
        If the value is False then only display the data frame, If the value is True then write the file to the current working directory. 

    Returns
    -------
    file :
        cleaned and processed dataframe and csv file that includes historical 
        data on currency exchange rates
        
    >>> retrieve_data(export_csv = False)

    """
    # Read CSV file and reset the index
    url = 'https://raw.githubusercontent.com/mrnabiz/forx_source/main/data/raw/raw_data_cad.csv'
    data_raw = (pd.read_csv(url, delimiter=",")[38:]).reset_index()
    
    # Setting the first row as column names
    data_raw.columns = data_raw.iloc[0]
    data = data_raw.iloc[:, 1:]
    
    # Drop the first row of data
    data = data.drop(data.index[0])
    
    # Drop "FXMYRCAD", "FXTHBCAD", "FXVNDCAD" columns with many NA values
    data = data.drop(labels=["FXMYRCAD", "FXTHBCAD", "FXVNDCAD"], axis=1)
    
    
    # Convert date column to datetime format
    data['date'] = pd.to_datetime(data['date'])
    
    # Creating list of column names
    col_list = data.columns.tolist()
    
    # Remove the date column from the list
    col_list.remove('date')
    
    # Convert all columns in the list to numeric data type
    data[col_list] = data[col_list].apply(pd.to_numeric)
    
    # Wrangling column labels
    data.columns = data.columns.str.replace("FX", "")
    data.columns = data.columns.str.replace("CAD", "")
    
    # Add "CAD" column and assign a value of 1.0 to eahc row
    data['CAD'] = 1.0
    

    if export_csv == True:
        # Saving dataframe as CSV file if output=True
        data.to_csv("data_raw.csv")
    else:
        # Only display dataframe if output=False
        return data
    
    return data


def fastest_slowest_currency(start_date, end_date):
    """
    This function takes currency exchange rates data as input and returns a 
    list of two strings containing the fastest and slowest growing currency 
    exchange rate in relation to Canadian Dollar.
    The data provided contains currency code in the format FX***CAD, 
    the average exchange rate and the date.
    
    Parameters
    ----------
    start_date : string '%YYYY-%mm-%dd'
	    inputted starting date in the format specified '%YYYY-%mm-%dd'
	end_date : string '%YYYY-%mm-%dd'
	    inputted ending date in the format specified '%YYYY-%mm-%dd'

    Returns
    -------
    list
        list of lists containing the fastest currency name and its current 
        exchange rate with CAD and the slowest currency with its current exchange 
        rate with CAD for the specified date range.
    
    Examples
    >>> fastest_slowest_currency('2019-05-23', '2022-05-30')
    [['EUR', 1.4545], ['IDR', 8.9e-05]]
    """ 
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Check for invalid date format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", start_date) or not re.match(r"^\d{4}-\d{2}-\d{2}$", end_date):
        raise ValueError("Invalid date format. Please enter dates in the format '%YYYY-%mm-%dd'.")
    
    # Check for invalid date range
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    if start > end:
        raise ValueError("Invalid date range. Please ensure that the start date is before the end date.")

    # Extracting the data split to calculate the fastest and slowest currency for the given range
    data = retrieve_data()
    df = data[(data['date'] >= start) & (data['date'] <= end)]

    # Check for empty data
    if data.empty:
        raise ValueError("No data available for the specified date range.")

    # Computing the fastest growing currency and the slowest growing currency for the given range
    tepm = df[:1] 
    tepm = tepm.append(df[-1:], ignore_index=True)
    diff = tepm.diff()[-1:]
    diff = diff.abs()
    
    nums = pd.to_numeric(diff.drop(columns=['date', 'CAD']).loc[1])
    fastestcurr = nums.idxmax()
    slowestcurr = nums.idxmin()

    # calculates and stores the increase and decrease overall
    fastdiff = nums.max()
    slowdiff = nums.min()

    # Extracting the current rate of the slowest and the fastest currencies
    slow_current_rate = data.loc[data.shape[0]][slowestcurr]
    fast_current_rate = data.loc[data.shape[0]][fastestcurr]

    # returning the computed values
    return [[fastestcurr, fast_current_rate], [slowestcurr, slow_current_rate]]

def currency_convert(value, currency1, currency2):
    """
    This function takes a currency value and the currency type 
    to be converted to as input and returns the converted currency 
    value as per the current conversion rate.
    
    Parameters
    ----------
    value: float
        The value of the original currency to be converted

    currency1: str
        The type of currency originally
    
    currency2: str
        The type of currency that the currency1 will be converted to
    
    Returns
    -------
    converted: numeric
        Returns converted numeric currency
    
    Examples
    >>> currency_convert(23, 'USD', 'CAD')
    """
    df_conv_rates = retrieve_data()
    
    names = {'AUD':1,'BRL':2,'CNY':3, 'EUR':4, 'HKD':5, 'INR':6, 'IDR':7, 
         'JPY':8, 'MXN':9, 'NZD':10, 'NOK':11, 'PEN':12, 
         'RUB':13, 'SAR':14, 'SGD':15, 'ZAR':16, 'KRW':17, 'SEK':18, 
         'CHF':19, 'TWD':20, 'TRY':21, 'GBP':22, 'USD':23} # helps to locate the data in the df
    
    if currency1 not in names: # check whether the currency to be converted is in our data
        if currency1 != 'CAD':
            raise ValueError("The currency to be converted is invalid!")
        
    if currency2 not in names: # check whether the currency to be converted to is in our data
        if currency2 != 'CAD':
            raise ValueError("The currency to be converted to is invalid!")
    if value <= 0:
        raise ValueError("Please enter an positive amount!")
    
    if currency2 == 'CAD' : # situation of convert a specific currency to CAD
        if currency1 == 'CAD':
            return(round(value,3)) 
        
        else:
            amount = round(value*float(df_conv_rates.iloc[-1][names[currency1]]),3)
            return amount 
    
    elif currency1 == 'CAD': # situation of convert CAD to a specific currency
        if currency2 == 'CAD':
            return(round(value,3))
        
        else: 
            amount = round(value/(float(df_conv_rates.iloc[-1][names[currency2]])),3)
            return amount
    
    else: 
            amount = round(value*(float(df_conv_rates.iloc[-1][names[currency1]])) # situation of convert a specific currency to another currency 
                 /(float(df_conv_rates.iloc[-1][names[currency2]])),3)              # which are neither CAD 
            
            return amount
    

def plot_historical(start_date, end_date, currency1, currency2):
    """
    Plots the historical rate of the entered currencies within a specific period
    of time.

    Parameters
    ----------
	start_date : string '%YYYY-%mm-%dd'
	    inputted starting date in the format specified '%YYYY-%mm-%dd'
	end_date : string '%YYYY-%mm-%dd'
	    inputted ending date in the format specified '%YYYY-%mm-%dd'
    currency1 : str
        The type of based currency asked for plotting
    currency2 : str
        The type of exchange currency asked for plotting

    Returns
    -------
    plot object
        A plot showing the performance of the currency.

    Examples
    --------
    >>> plot_historical('2020-05-23', '2022-05-30', 'USD', 'CAD')
    """
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Data filtration
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    ratio = currency1 + '/' + currency2
    data = retrieve_data()
    data[ratio] = data[currency1]/data[currency2]
    data_plt = data[(data['date'] >= start) &
                    (data['date'] <= end)][['date', ratio]]
    
    # Building the base chart
    base_chart = alt.Chart(data_plt).mark_line().encode(
        alt.X('date', title='Date'),
        alt.Y(ratio, scale=alt.Scale(zero=False)),
        tooltip=['date', ratio]).properties(width=900, height=200)
    dot_line_chart = base_chart + base_chart.mark_point(size=2)

    # Building interactivity
    brush = alt.selection_interval(encodings=['x'])
    lower_chart = base_chart.properties(height=60).add_selection(brush)
    upper_chart = dot_line_chart.encode(alt.X('date:T', 
                                            scale=alt.Scale(domain=brush)))

    plt_title = 'How many ' + currency2 + ' does 1 ' + currency1 + ' worth?'
    sbs_plot = (upper_chart & lower_chart).properties(
        title=plt_title
                                        ).configure_title(
        fontSize=18, font='Cambria', anchor='start').configure_axis(
            labelFontSize=10, titleFontSize=10, 
            labelFont='Cambria', titleFont='Cambria'
            )
    
    # Unit tests to test the function input
    assert end >= data['date'].min(), 'The end date is out of the range'
    assert start <= data['date'].max(), 'The start date is out of the range'
    assert currency1 in data.columns.to_list(), 'Currency 1 is not supported'
    assert currency2 in data.columns.to_list(), 'Currency 1 is not supported'

    # Unit tests to test the plot object
    assert base_chart.to_dict()['mark'] == 'line', 'Chart type is not line'
    assert base_chart.to_dict()['encoding']['x']['type'] == 'temporal', 'Datetype is not temporal'
    assert base_chart.to_dict()['encoding']['y']['type'] == 'quantitative', 'Rates are not numeric'
    assert sbs_plot.title == plt_title, 'The final plot has not formed correctly'

    return sbs_plot