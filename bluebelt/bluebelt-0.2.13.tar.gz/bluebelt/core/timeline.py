import pandas as pd
import numpy as np


class TimeLine(pd.Series):
    def __init__(self, *args, **kwargs):
        dtype = kwargs.pop('dtype', 'float64')
        name = kwargs.pop('name', 'value')
        super().__init__(*args, name=name, dtype=dtype, **kwargs)

    def add(self, other=None, start=None, end=None, value=None, **kwargs):
        """
            Add data to the TimeLine object.
        
            Parameters
            ----------
            self: Bluebelt TimeLine object
            other: the object to add, default None
                If the object is a TimeLine object a new object is created with
                a combined index.
                If the object is a Pandas Dataframe and 'start' and 'end' are
                provided every row in the dataframe is added to the timeline. A
                'value' column is optional.
                If the object is a tuple or list and the first two items in it are
                Pandas Timestamps or can be converted to Pandas Timestamps a new
                object is created with a combined index. If a third item is given
                the value will be the third items value, if not it will be 1.
                If the object is a dict with keys 'start' and 'end' that have
                Pandas Timestamp-like values a new object is created with a combined
                index. If a 'value' key is not in the dict the value will be 1.
                If the object is a Pandas Series of int the default Pandas add
                function is used.
            start: the column name with the start Timestamp data, default None
                Only used if 'other' is a Pandas DataFrame
            end: the column name with the end Timestamp data, default None
                Only used if 'other' is a Pandas DataFrame
            value: the columns with the value data, default None
                Only used if 'other' is a Pandas DataFrame

            Returns
            -------
            The new Bluebelt TimeLine or Pandas Series object

        """
        if isinstance(other, TimeLine):
                index = self.index.union(other.index)

                # reindex the TimeLine objects (returns pd.Series objects)
                t1 = self.reindex(index).ffill().fillna(0)
                t2 = other.reindex(index).ffill().fillna(0)

                return TimeLine(t1.add(t2))
        elif isinstance(other, (dict, tuple, list, np.ndarray)):
            # check if there are at least two timestamps or force an error
            if isinstance(other, dict):
                start = pd.Timestamp(other.get('start'))
                end = pd.Timestamp(other.get('end'))
                value = other.get('value', 1)
            else:
                start = pd.Timestamp(other[0])
                end = pd.Timestamp(other[1])
                value = other[2] if len(other)>2 else 1
            
            other_index = pd.Index([start, end], dtype='datetime64[ns]')
            new_index = self.index.union(other_index)

            # reindex the TimeLine objects (returns pd.Series objects)
            t1 = self.reindex(new_index).ffill().fillna(0)
            t2 = pd.Series(
                index = other_index,
                data = [value, 0],
            ).reindex(new_index).ffill().fillna(0)

            return TimeLine(t1.add(t2))

        elif isinstance(other, pd.DataFrame) and start is not None and end is not None:

            # remove rows with start == end
            # remove NaT values
            other = other[other[start]!=other[end]]
            other = other[~(other[start].isna() | other[end].isna())]

            # set new index
            index = pd.Index(other[start].values).union(pd.Index(other[end].values))

            # build input series
            if value:
                series = other.groupby([start, end])[value].sum().rename('value')
            else:
                series = other.groupby([start, end])[start].count().rename('value')

            # remove start == end
            series = series[series.index.get_level_values(0)!=series.index.get_level_values(1)]

            # remove NaT
            series = series[~series.isna()]

            array = np.zeros(index.size)

            for key, value in series.to_dict().items():
                array = np.add(array, np.multiply(((index.values >= key[0]) & (index.values < key[1])).astype(float), value))

            return TimeLine(self.reindex(index).ffill().fillna(0).add(pd.Series(index=index, data=array)))

        else:
            return TimeLine(super().add(other, **kwargs))
    
    def subtract(self, other=None, start=None, end=None, value=None, how=None, **kwargs):
        """
            Subtract data from the TimeLine object.
        
            Parameters
            ----------
            self: Bluebelt TimeLine object
            other: the object to subtract, default None
                If the object is a TimeLine object a new object is created with
                a combined index.
                If the object is a Pandas Dataframe and 'start' and 'end' are
                provided every row in the dataframe is added to the timeline. A
                'value' column is optional.
                If the object is a tuple or list and the first two items in it are
                Pandas Timestamps or can be converted to Pandas Timestamps a new
                object is created with a combined index. If a third item is given
                the value will be the third items value, if not it will be 1.
                If the object is a dict with keys 'start' and 'end' that have
                Pandas Timestamp-like values a new object is created with a combined
                index. If a 'value' key is not in the dict the value will be 1.
                If the object is a Pandas Series the default Pandas subtract
                function is used.
            start: the column name with the start Timestamp data, default None
                Only used if 'other' is a Pandas DataFrame
            end: the column name with the end Timestamp data, default None
                Only used if 'other' is a Pandas DataFrame
            value: the columns with the value data, default None
                Only used if 'other' is a Pandas DataFrame
            how: how to calculate when other is a Pandas Dataframe, default None
                If how='slow' a loop over all the values will be used which, as
                we know, one should never do. Otherwise a faster but memory-eating
                groupby method is tried. It is about three times faster but less
                memory-friendly.

            Returns
            -------
            The new Bluebelt TimeLine or Pandas Series object

        """
        if isinstance(other, TimeLine):
                index = self.index.union(other.index)

                # reindex the TimeLine objects (returns pd.Series objects)
                t1 = self.reindex(index).ffill().fillna(0)
                t2 = other.reindex(index).ffill().fillna(0)

                return TimeLine(t1.subtract(t2))
        elif isinstance(other, (dict, tuple, list, np.ndarray)):
            # check if there are at least two timestamps or force an error
            if isinstance(other, dict):
                start = pd.Timestamp(other.get('start'))
                end = pd.Timestamp(other.get('end'))
                value = other.get('value', 1)
            else:
                start = pd.Timestamp(other[0])
                end = pd.Timestamp(other[1])
                value = other[2] if len(other)>2 else 1
            
            other_index = pd.Index([start, end], dtype='datetime64[ns]')
            new_index = self.index.union(other_index)

            # reindex the TimeLine objects (returns pd.Series objects)
            t1 = self.reindex(new_index).ffill().fillna(0)
            t2 = pd.Series(
                index = other_index,
                data = [value, 0],
            ).reindex(new_index).ffill().fillna(0)

            return TimeLine(t1.subtract(t2))

        # slow but sort of memory friendly
        elif isinstance(other, pd.DataFrame) and start is not None and end is not None:

            # remove rows with start == end
            # remove NaT values
            other = other[other[start]!=other[end]]
            other = other[~(other[start].isna() | other[end].isna())]

            # set new index
            index = pd.Index(other[start].values).union(pd.Index(other[end].values))

            # build input series
            if value:
                series = other.groupby([start, end])[value].sum().rename('value')
            else:
                series = other.groupby([start, end])[start].count().rename('value')

            # remove start == end
            series = series[series.index.get_level_values(0)!=series.index.get_level_values(1)]

            # remove NaT
            series = series[~series.isna()]

            array = np.zeros(index.size)

            for key, value in series.to_dict().items():
                array = np.add(array, np.multiply(((index.values >= key[0]) & (index.values < key[1])).astype(float), value))

            return TimeLine(self.reindex(index).ffill().fillna(0).subtract(pd.Series(index=index, data=array)))
            
        else:
            return super().subtract(other, **kwargs)
        
    def reduce(self, *args, **kwargs):
        """
            Reduce the TimeLine object by grouping the index by value.
        
            Parameters
            ----------
            self: Bluebelt TimeLine object

            Returns
            -------
            The Bluebelt TimeLine object with a new index

        """
        return TimeLine(
            index = self.index[(self.values!=self.shift().values)],
            data = self.groupby((self.values!=self.shift().values).cumsum()).max().values            
        )
    
    def resample(self, rule='15T', *args, **kwargs):
        """
            Resample the TimeLine object.
        
            Parameters
            ----------
            self: Bluebelt TimeLine object
            rule: Pandas resample rule, default '15T'

            Returns
            -------
            The Bluebelt TimeLine object with a new index

        """
        # get the gcd in nanoseconds
        gcd = np.gcd.reduce(
            [int(x / np.timedelta64(1, 'ns')) for x in (self.index[1:] - self.index[:-1]).values]
        )
        
        # check if the rule >= gcd
        if pd.Timedelta(rule) >= np.timedelta64(gcd, 'ns'):
            gcd_rule = f'{gcd}ns'
        else: # rule < gcd
            gcd_rule = rule
            
        # first resample to gcd with ffill, then to desired rule with max
        return TimeLine(super().resample(gcd_rule).ffill().resample(rule).max())
    
    def reshape(self, rule='week', level='minute', aggfunc='max'):
        """
            Reshape the TimeLine object.
        
            Parameters
            ----------
            self: Bluebelt TimeLine object
            rule: reshaping rule, default 'week'
                Indicates the new index level, 'year', 'week', 'day', 'hour',
                'minute' or 'second'. The lower levels are converted to columns.
            level: the lowest level to return, default 'minute'
            aggfunc: the Pandas.pivot_table aggfunc, default 'max'
            
            Returns
            -------
            a Pandas DataFrame object

        """
        name = self.name
        levels = ['year', 'week', 'day', 'hour', 'minute', 'second']
        
        if not (rule in levels and level in levels):
            raise ValueError("Both rule and level should be 'year', 'week', 'day', 'hour', 'minute' or 'second'")
            
        # avoid trouble if the level has a lower index than rule 
        level = level if levels.index(rule) < levels.index(level) else rule
        
        frame = pd.DataFrame(self)
        frame.loc[:,['year', 'week', 'day']] = frame.index.isocalendar()
        frame['hour'] = frame.index.hour
        frame['minute'] = frame.index.minute
        frame['second'] = frame.index.second
        return frame.pivot_table(
            index=levels[:levels.index(rule)+1],
            columns=levels[levels.index(rule)+1:levels.index(level)+1],
            values=name,
            aggfunc=aggfunc,
        )
    
    def percentile(self, percentile=0.1, how='smallest', rule='week', level='minute'):
        """
            Reshape the TimeLine object and return a pandas Series for one period.
            The period is constructed as the percentile for every 'level' time slot
            over one 'rule' period.
        
            Parameters
            ----------
            self: Bluebelt TimeLine object
            percentile: the percentile to calculate, default 0.1
            how: calculate the percentile as 'smallest' or 'largest', default 'smallest'
            rule: reshaping rule, default 'week'
                Indicates the new index level, 'year', 'week', 'day', 'hour',
                'minute' or 'second'. The lower levels are converted to columns.
            level: the lowest level to return, default 'minute'
            
            Returns
            -------
            a Pandas DataFrame object

        """
        levels = ['year', 'week', 'day', 'hour', 'minute', 'second']
        
        # avoid trouble if the level has a lower index than rule 
        level = level if levels.index(rule) < levels.index(level) else levels[levels.index(rule)+1]
        
        # yes, reshape to the lowest level and return a series
        result = self.reshape(rule=level).iloc[:,0]
        
        # get n from percentile
        n = np.round(result.groupby(level=levels[:levels.index(rule)+1]).ngroups * percentile).astype(int)
        
        # set groupby_levels
        groupby_levels = levels[levels.index(rule)+1:levels.index(level)+1]
        
        # and now groupby levels down to 'rule'
        if how == 'largest':
            result = result.groupby(level=groupby_levels, group_keys=False).nlargest(n).groupby(level=groupby_levels, group_keys=False).nsmallest(1)
        elif how == 'smallest':
            result = result.groupby(level=groupby_levels, group_keys=False).nsmallest(n).groupby(level=groupby_levels, group_keys=False).nlargest(1)
        else:
            raise ValueError(f"parameter 'how' must be 'smallest' or 'largest', not {how}.")
            
        return result