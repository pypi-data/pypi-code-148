from __future__ import annotations

from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class BusinessObjectQueryClause(TcBaseObj):
    """
    Business object query clause
    
    :var propName: Property Name.
    :var propValue: Property Value.
    :var mathOperator: Math Operator.  Legal math operators can be =, !=, >, >=, <, <=, Contain, IS_NULL or IS_NOT_NULL
    according to the property type.
    :var logicOperator: Logic Operator.  Legal logic operators are "AND" and "OR".
    """
    propName: str = ''
    propValue: str = ''
    mathOperator: str = ''
    logicOperator: str = ''


@dataclass
class BusinessObjectQueryInput(TcBaseObj):
    """
    Business Object Query Input
    
    :var typeName: Name of business object type
    :var clauses: Query clauses in serach criteria.
    :var maxNumToReturn: Specified maximum number of objects to return.
    :var requestId: Unique ID used to register the query execution task. This can be used by the caller to cancel the
    time consuming query, the value can be generated by any unique string generator.
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure. This is currently not yet used by the return data elements, the caller can leave it empty.
    """
    typeName: str = ''
    clauses: List[BusinessObjectQueryClause] = ()
    maxNumToReturn: int = 0
    requestId: str = ''
    clientId: str = ''
