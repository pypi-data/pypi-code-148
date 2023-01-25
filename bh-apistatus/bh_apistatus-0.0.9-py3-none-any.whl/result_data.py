"""
API ResultData.
"""
from inspect import getmembers, isroutine
from typing import Union

class ResultData: 
    """Provides ability to dynamically add and access data as either dictionaries or lists 
    during processing.

    Final data can be serialised as a dictionary, and converted into JSON and returned to 
    (web) clients.

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *data* (``Union[dict, list]``) -- a dictionary or a list of dictionaries to be added.
        * *data_name* (``str``) -- associated name for ``data`` above.
    """

    def __init__(self, **kwargs):
        self.__default = []

        if ('data' in kwargs):
            self.add(kwargs.get('data'), kwargs.get('data_name', None))        

    def __get_unique_name(self, name: str) -> str:
        """Prepend name with a unique non-0 leading integer till it becomes
        a unique attribute name.
        """
        if (not hasattr(self, name)): return name
        
        i = 1
        new_name = f"{name}_{i}"
        while (hasattr(self, new_name)):
            i += 1
            new_name = f"{name}_{i}"

        return new_name

    def __add(self, data):
        if (isinstance(data, list)):
            self.__default = data[:]

        elif (isinstance(data, dict)):
            for k, v in data.items():
                new_k = self.__get_unique_name(k)
                setattr(self, new_k, v)

    def add(self, data: Union[dict, list], name=None) -> None:
        """Add a dictionary or a list of dictionaries.

        :param data: the dictionary or the list of dictionaries to be added.
        :param str name: the associated name for ``data``, which become the instance \
            attribute name.

        :return: None.
        """

        setattr(self, name, data) if (name != None) else self.__add(data)

    def __has_custom_attribute(self):
        for n, v in getmembers(self):
            if (not isroutine(v)) and (n[0] != '_'): return True
        
        return False

    def as_dict(self) -> dict: 
        """Return all data as a dictionary whose root key is ``data``.

        I.e.::

            data = ResultData(data={'first_name': 'Be Hai','surname': 'Nguyen',})

            data_dict = data.as_dict()

            # data_dict = {'data': {'first_name': 'Be Hai', 'surname': 'Nguyen'}}

            assert data_dict['data']['first_name'] == 'Be Hai'
            assert data_dict['data']['surname'] == 'Nguyen'

        :return: a dictionary representation of all internal data. When there is no data, \
            an effectively empty dictionary is returned ``{'data': {}}``.
        :rtype: dict.
        """
        try:
            result = None

            has_custom_attribute = self.__has_custom_attribute()

            if len(self.__default) > 0:                
                result = {'data': self.__default[:] } if (not has_custom_attribute) \
                    else {'data': {'items': self.__default[:] }}

            if (result == None ): result = {'data': {}}

            for n, v in getmembers(self):
                if (not isroutine(v)) and (n[0] != '_'):
                    result['data'][n] = v
        finally:
            return result

    def serialise_data(self) -> Union[dict, list]:
        """All data consolidated as a dictionary whose root key is ``data``. \
            Return the value (object) of root key ``data``.

        I.e.::

            data = ResultData(data={'first_name': 'Be Hai','surname': 'Nguyen',})

            data_dict = data.serialise_data()

            # data_dict = {'first_name': 'Be Hai', 'surname': 'Nguyen'}

            assert data_dict['first_name'] == 'Be Hai'
            assert data_dict['surname'] == 'Nguyen'

        Or as a list of dictionaries (one in this example)::

            data = ResultData(data=[{'first_name': 'Be Hai','surname': 'Nguyen',}])

            data_dict = data.serialise_data()

            # data_dict = [{'first_name': 'Be Hai', 'surname': 'Nguyen'}]

            assert data_dict[0]['first_name'] == 'Be Hai'
            assert data_dict[0]['surname'] == 'Nguyen'

        Call method :meth:`as_dict` to do most of the work. The returned value can be \
            added as data to other instances of :class:`ResultData`. 

        When there is no data added prior, it just returns an empty dictionary ``{}``.            

        :return: a dictionary or a list of dictionaries representation of all internal data.
        :rtype: Union[dict, list].
        """        
        return self.as_dict()['data']

    def __getitem__(self, item): return self.__default[ item ]

    def __len__(self): return len(self.__default)