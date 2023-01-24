"""
Common generic JSON functions. Require `simplejson <https://simplejson.readthedocs.io>`_ 
package.

For usage examples, see ``./tests/test_json_funcs.py``.
"""
from datetime import date, datetime
from typing import Union
import simplejson as json

def serialise(obj) -> str:
    """JSON serialiser for objects not serialisable by default JSON code.

    :Reference: 
    
        * `How to overcome "datetime.datetime not JSON serializable"? \
            <https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable>`_

    :param obj: object to be serialisable. Currently recognising only \
        `datetime <https://docs.python.org/3/library/datetime.html>`_.

    :return: a string representation of param ``obj``. 
    :rtype: str.    

    - `datetime <https://docs.python.org/3/library/datetime.html>`_ values are serialised into the \
        Australian date format ``dd/mm/yyyy``.
	"""

    if isinstance(obj, (datetime, date)):
        # return obj.isoformat()
        return obj.strftime('%d/%m/%Y')

    raise TypeError ("Type %s not serializable" % type(obj))

def dumps(obj: Union[dict, list]) -> str:
    """Serialise a dictionary or a list to a JSON string.

    Date fields' values are converted into the Australian date format ``dd/mm/yyyy``.

    :param obj: the dictionary or the list to be converted to JSON string.

    :return: JSON string representation of param ``obj``.
    :rtype: str.
    """
    return json.dumps(obj, use_decimal=True, default=serialise, indent="  ")