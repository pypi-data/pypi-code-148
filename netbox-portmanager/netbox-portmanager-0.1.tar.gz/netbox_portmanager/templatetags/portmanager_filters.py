from django import template

register = template.Library()


def keyvalue(dictionary, key):    
    return dictionary.get(str(key), None)


def getpsmax(if_ps_max, if_ps_enable):
    return "" if if_ps_enable == 2 else if_ps_max

register.filter("keyvalue", keyvalue)
register.filter("getpsmax", getpsmax)