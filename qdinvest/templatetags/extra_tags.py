#coding=utf-8 
from django import template
register = template.Library()
from datetime import datetime

@register.filter(name='lastDays')
def lastDays(endDate):
	days = (endDate - datetime.now()).days
	if days < 0:
		days = 0
	return days
