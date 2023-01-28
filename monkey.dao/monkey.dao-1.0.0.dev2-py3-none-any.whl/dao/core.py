# -*- coding: utf-8 -*-

import logging

ASC = ASCENDING = 1
"""Ascending sort order"""

DESC = DESCENDING = -1
"""Descending sort order"""


class PersistenceError(Exception):
    """Exception class for generic persistence error"""

    def __init__(self, message='Persistence error', cause=None):
        self.message = message
        self.cause = cause


class DuplicateKeyError(PersistenceError):
    """Exception class for duplicate key error"""

    def __init__(self, data_set, key, cause=None):
        super().__init__('Duplicate key error : {} already exist in data set \'{}\'.', cause)
        self.data_set = data_set
        self.key = key


class ObjectNotFoundError(PersistenceError):
    """Exception class for object not found error"""

    def __init__(self, data_set, key, cause=None):
        super().__init__('Not object found with key {} in data set \'{}\'', cause)
        self.data_set = data_set
        self.key = key


class DAO:
    """Generic definition of Data Access Object"""

    def __init__(self):
        """Instantiates a new DAO """
        self.logger = logging.getLogger(self.__class__.__name__)

    def find_one_by_key(self, key):
        """Finds a record by its key
        :param key: key of the record
        :return: the found record (if there is one)
        :raise: ObjectNotFoundError
        """
        raise NotImplementedError()

    def find_all(self, skip=0, limit=0, sort=None, **kwargs):
        """Finds all records
        :param skip: the number of record to omit (from the start of the result set) when returning the results
        :param limit: the maximum number of records to return
        :param sort: a list of (key, direction) pairs specifying the sort order for this list
        :param kwargs: implementation specific arguments
        :return: a list of records
        """
        return self.find(query=None, skip=skip, limit=limit, sort=sort, **kwargs)

    def find(self, query=None, skip=0, limit=0, sort=None, **kwargs):
        """Finds records matching the specified query
        :param query:
        :param skip: the number of record to omit (from the start of the result set) when returning the results
        :param limit: the maximum number of records to return
        :param sort: a list of (key, direction) pairs specifying the sort order for this list
        :param kwargs: implementation specific arguments
        :return: a list of records
        """
        raise NotImplementedError()

    def count(self):
        """Counts the number of records
        :return: the total number of records
        """
        raise NotImplementedError()

    def delete(self, key):
        """Deletes the record with specified key
        :param key: key of the record to delete
        :return: count of deleted record (0 or 1)
        """
        raise NotImplementedError()
