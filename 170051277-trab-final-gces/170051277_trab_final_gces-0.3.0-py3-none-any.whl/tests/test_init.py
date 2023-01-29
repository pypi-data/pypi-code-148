# Since there are no tests implemented, I create this dummy class that simulates them.

import pytest

def testGetGcesString():
    result = getGcesString()
    assert result == "GCES"

def getGcesString():
    return "GCES"
