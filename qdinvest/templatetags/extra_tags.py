#coding=utf-8 
from django import template
register = template.Library()
from datetime import datetime

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
