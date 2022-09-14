"""Checks for elemental types"""


def isBool(obj):
    if isInt(obj):
        return False
    return isinstance(obj, bool)

def isElemental(obj):
    return isStr(obj) or isList(obj) or isInt(obj) or isFloat(obj)

def isFloat(obj):
    if isInt(obj):
        return False
    return isinstance(obj, float)

def isInt(obj):
    return "int" in str(type(obj))

def isList(obj):
    if isStr(obj):
        return False
    return isinstance(obj, list)

def isStr(obj):
    return isinstance(obj, str)

