import pandas as pd
import numpy as np


class TimeLine(pd.Series):
    def __init__(self, *args, **kwargs):
        dtype = kwargs.pop('dtype', 'float64')
        name = kwargs.pop('name', 'value')
        super().__init__(*args, name=name, dtype=dtype, **kwargs)
        
    def add(self, other=None, **kwargs):
        """
            Add data to the TimeLine object.
        
            Parameters
            ----------
            self: Bluebelt TimeLine object
            other: the object to add, default None
                If the object is a TimeLine object a new object is created with
                a combined index.
                If the object is a tuple or list and the first two items in it are
                Pandas Timestamps or can be converted to Pandas Timestamps a new
                object is created with a combined index. If a third item is given
                the value will be the third items value, if not it will be 1.
                If the object is a dict with keys 'start' and 'end' that have
                Pandas Timestamp-like values a new object is created with a combined
                index. If a 'value' key is not in the dict the value will be 1.
                
                If the object is a Pandas Series of int the default Pandas add
                function is used.

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
        elif isinstance(other, (dict, tuple, list)):
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
        else:
            return super().add(other, **kwargs)
    
    def subtract(self, other=None, **kwargs):
        """
            Subtract data from the TimeLine object.
        
            Parameters
            ----------
            self: Bluebelt TimeLine object
            other: the object to subtract, default None
                If the object is a TimeLine object a new object is created with
                a combined index.
                If the object is a tuple or list and the first two items in it are
                Pandas Timestamps or can be converted to Pandas Timestamps a new
                object is created with a combined index. If a third item is given
                the value will be the third items value, if not it will be 1.
                If the object is a dict with keys 'start' and 'end' that have
                Pandas Timestamp-like values a new object is created with a combined
                index. If a 'value' key is not in the dict the value will be 1.
                
                If the object is a Pandas Series the default Pandas subtract
                function is used.

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
        elif isinstance(other, (dict, tuple, list)):
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
