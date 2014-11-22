#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404

from models import *

def Index(request,id):
	context = RequestContext(request)
	context_dict = {}
	try:
		STOCK_obj = STOCK.objects.get(id__exact = id)
		context_dict['stock'] = STOCK_obj
	except STOCK.DoesNotExist:
		raise Http404
	print context_dict
	return render_to_response('wechat/index.html',context_dict,context)

#手机端详细页面HTML
def ProDetail(request,p_type,p_id):
	context = RequestContext(request)
	context_dict = {}
	if p_type == 's':
		try:
			STOCK_obj = STOCK.objects.get(id__exact = p_id)
			context_dict['stock'] = STOCK_obj
			return render_to_response('wechat/pro-details.html',context_dict,context)
		except STOCK.DoesNotExist:
			raise Http404
	elif p_type == 'b':
		try:
			BOND_obj = BOND.objects.get(id__exact = p_id)
			context_dict['bond'] = BOND_obj
			return render_to_response('wechat/pro-details.html',context_dict,context)
		except BOND.DoesNotExist:
			raise Http404
	else:
		raise Http404