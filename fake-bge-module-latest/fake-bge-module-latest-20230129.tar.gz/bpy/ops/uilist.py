import sys
import typing


def entry_add(list_path: str = "", active_idx_path: str = ""):
    ''' Add an entry to the list after the current active item

    :param list_path: list_path
    :type list_path: str
    :param active_idx_path: active_idx_path
    :type active_idx_path: str
    '''

    pass


def entry_move(list_path: str = "",
               active_idx_path: str = "",
               direction: typing.Union[int, str] = 'UP'):
    ''' Move an entry in the list up or down

    :param list_path: list_path
    :type list_path: str
    :param active_idx_path: active_idx_path
    :type active_idx_path: str
    :param direction: Direction * UP UP -- UP. * DOWN DOWN -- DOWN.
    :type direction: typing.Union[int, str]
    '''

    pass


def entry_remove(list_path: str = "", active_idx_path: str = ""):
    ''' Remove the selected entry from the list

    :param list_path: list_path
    :type list_path: str
    :param active_idx_path: active_idx_path
    :type active_idx_path: str
    '''

    pass
