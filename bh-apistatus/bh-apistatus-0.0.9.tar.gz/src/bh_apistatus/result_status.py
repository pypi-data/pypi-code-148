"""
API ResultStatus.
"""
from __future__ import annotations
from typing import Union

from http import HTTPStatus

from .result_data import ResultData

class ResultStatus:
    """Encapsulate result status of server operations in response to client requests.

    Status includes a response code, an optional response message, an optional unique 
    web session identifier. It is assumed that, at the server-side, the web session identifier 
    also gets logged for each request, and so it should serve to identify the web sessions which 
    caused the errors.

    Finally, status can also include optional data, an instance of :py:class:`.result_data.ResultData`.

    Final result status can be can be serialised as a dictionary, and converted into JSON 
    and returned to (web) clients.

    :param int code: one of those HTTP codes defined in \
        `http — HTTP modules <https://docs.python.org/3/library/http.html#module-http>`_. \
        Default value is ``HTTPStatus.OK.value``.

    :param str text: an optional message.

    :param str session_id: an optional web session identifier.

    :param \**kwargs: keyword arguments for :doc:`result-data`:

    :Keyword Arguments:
        * *data* (``Union[dict, list]``) -- a dictionary or a list of dictionaries to be added.
        * *data_name* (``str``) -- associated name for ``data`` above.    
    """

    def __init__(self, code=HTTPStatus.OK.value, text='', session_id=None, **kwargs):
        self._code = code
        self._text = text
        self._session_id = session_id
        
        if ('data' in kwargs):
            self.add_data(kwargs.get('data'), kwargs.get('data_name', None))

    def add_data(self, data: Union[dict, list], name=None) -> ResultStatus:
        """Add a dictionary or a list of dictionaries to :attr:`~.ResultStatus.data`, which is \
            an instance of :py:class:`.result_data.ResultData`.

        :param data: the dictionary or the list of dictionaries to be added.
        :param str name: the associated name for :attr:`~.ResultStatus.data`.

        This method maintains chainability.

        :return: self.
        :rtype: :class:`ResultStatus`.
        """

        if (not hasattr(self, '_data')): 
            self._data = ResultData()

        self._data.add(data, name)
        
        return self

    def as_dict(self) -> dict:
        """Return result status as a dictionary whose root key is ``status``.

        I.e.::

            status = ResultStatus(text="I am okay...")

            status_dict = status.as_dict()

            # status_dict = {'status': {'code': 200, 'text': 'I am okay...'}}

            assert status_dict['status']['code'] == HTTPStatus.OK.value
            assert status_dict['status']['text'] == "I am okay..."

        :return: a dictionary representation of the result status.
        :rtype: dict.
        """        
        status = {
            'status': {
                'code': self._code,
                'text': self._text                
            }
        }

        if (self._session_id != None): 
            status['status']['session_id'] = self._session_id

        if hasattr(self, '_data'): 
            status['data'] = {}
            status['data'] = self._data.as_dict()['data']

        return status

    def copy_status_info(self, source: ResultStatus) -> ResultStatus:
        """Copy the values of :attr:`~.ResultStatus.code`, :attr:`~.ResultStatus.text` and \
            :attr:`~.ResultStatus.session_id` from an :class:`ResultStatus` instance.

        :param source: the instance whose status info are copied over.
        :type source: :class:`ResultStatus`

        This method maintains chainability.

        :return: self.
        :rtype: :class:`ResultStatus`.
        """        
        self._code = source.code
        self._text = source.text
        self._session_id = source.session_id
        return self

    def serialise_data(self) -> Union[dict, list]:
        """All :attr:`~.ResultStatus.data` consolidated as a dictionary whose root \
            key is ``data``. Return the value (object) of root key ``data``.
        
        This method is just a wrapper of :py:meth:`.result_data.ResultData.serialise_data`.

        :return: a dictionary or a list of dictionaries representation of all internal data.
        :rtype: Union[dict, list].        
        """

        return self._data.serialise_data()

    @property
    def code(self) -> int: 
        """Read and write property.

        Get and set internal HTTP status code.
        
        It's one of those HTTP codes defined in \
        `http — HTTP modules <https://docs.python.org/3/library/http.html#module-http>`_. \
        """
        return self._code

    @code.setter
    def code(self, value): 
        """Set internal HTTP status code. 
        """
        self._code = value

    @property
    def text(self) -> str: 
        """Read and write property.

        Get and set internal text message.
        """
        return self._text

    @text.setter
    def text(self, value): 
        """Set internal text message.
        """
        self._text = value

    @property
    def session_id(self) -> str: 
        """Read and write property.

        Get and set internal optional web session identifier.
        """
        return self._session_id

    @session_id.setter
    def session_id(self, value): 
        """Set internal optional session identifier.
        """
        self._session_id = value

    @property
    def has_data(self) -> bool: 
        """Read only property. Return ``True`` when :attr:`~.ResultStatus.data` is not \
            ``None``, False otherwise.
        """
        return hasattr(self, '_data')

    @property
    def data(self) -> ResultData:
        """Read only property. 

        Get internal data.
        
        It's an instance of :py:class:`.result_data.ResultData`.

        Its default value is ``None``.
        """
        return self._data if hasattr(self, '_data') else None

def make_status(code=HTTPStatus.OK.value, text='', session_id=None, **kwargs) -> ResultStatus:
    """Create an instance of :class:`ResultStatus`, with possibly all properities \
        have values assigned.

    For parameters documentation, please see :class:`ResultStatus`.

    :return: a :class:`ResultStatus` instance.
    """

    return ResultStatus(code, text, **kwargs)

def make_500_status(text, session_id=None, **kwargs) -> ResultStatus:
    """Create an instance of :class:`ResultStatus`, with possibly all properities \
        have values assigned.

    For parameters documentation, please see :class:`ResultStatus`.

    :attr:`~.ResultStatus.code` is assigned a value of ``500`` or \
        ``HTTPStatus.INTERNAL_SERVER_ERROR.value``.

    :return: a :class:`ResultStatus` instance.
    """

    return ResultStatus(HTTPStatus.INTERNAL_SERVER_ERROR.value, text, session_id, **kwargs)

def clone_status(source: ResultStatus) -> ResultStatus:
    """Create an instance of :class:`ResultStatus` using status information from an existing instance.

    Status information includes the following properties :attr:`~.ResultStatus.code`, \
        :attr:`~.ResultStatus.text` and :attr:`~.ResultStatus.session_id`. 

    :param source: the instance whose status info is used to create a new instance.
    :type source: :class:`ResultStatus`

    :return: a :class:`ResultStatus` instance.
    """
    return ResultStatus(source.code, source.text, source.session_id)