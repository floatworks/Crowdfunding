#coding=utf-8 
from django import template
register = template.Library()
from datetime import datetime
import re

#求剩余天数
@register.filter(name='lastDays')
def lastDays(endDate):
	days = (endDate - datetime.now()).days
	if days < 0:
		days = 0
	return days

#转化为0位小数的万元
@register.filter(name='toTenThous')
def toTenThous(value):
	value = float(value)
	value /= 10000;
	value = int(value)
	return value

#转化金额 金额的千位分
@register.filter(name='money')
def money(value):
	value = float(value)
	left = int(value)
	right = value -left
	return strConv(left) + str(right)[1:]

def strConv(s):  
    s =  str(s)
    while True:
        (s,count) = re.subn(r"(\d)(\d{3})((:?,\d\d\d)*)$",r"\1,\2\3",s)
        if count == 0 : break
    return s