#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q

import tools as T
import simplejson as json
from datetime import datetime,timedelta
from  models import STOCK,PRO_TYPE,BOND

def testUeditor(request):
	context = RequestContext(request)
	context_dict = {}
	STOCK_obj = STOCK.objects.get(id__exact = 10)
	context_dict['stock'] = STOCK_obj
	return render_to_response('qdinvest/testUeditor.html',context_dict,context)

def index(request):
	context = RequestContext(request)
	context_dict = {}
	STOCK_objs=STOCK.objects.filter(st_pro_type__pt_name__contains = "筹资中")[:3]
	STOCK_objs2=STOCK.objects.filter(st_pro_type__pt_name__contains = "即将开始")[:3] 
	STOCK_objs3=STOCK.objects.filter(st_pro_type__pt_name__contains = "成功项目")[:3]  
	BOND_objs=BOND.objects.filter(bo_pro_type__pt_name__contains = "即将开始")[:3]
	BOND_objs2=BOND.objects.filter(bo_pro_type__pt_name__contains = "筹资中")[:3]
	BOND_objs3=BOND.objects.filter(bo_pro_type__pt_name__contains = "成功项目")[:3]
	context_dict['stocks'] = STOCK_objs 
	context_dict['stocks2'] = STOCK_objs2 
	context_dict['stocks3'] = STOCK_objs3 
	context_dict['bonds'] = BOND_objs
	context_dict['bonds2'] = BOND_objs2
	context_dict['bonds3'] = BOND_objs3
	return render_to_response('qdinvest/index.html',context_dict,context)

def bond(request):
	context = RequestContext(request)	
	context_dict = {}	
	BOND_objs=BOND.objects.all()[:6]
	context_dict['bonds'] = BOND_objs
	return render_to_response('qdinvest/bond.html',context_dict,context)


def stock(request):
	context = RequestContext(request)
	context_dict = {}
	STOCK_objs=STOCK.objects.all()[:11]
	context_dict['stocks'] = STOCK_objs
	return render_to_response('qdinvest/stock.html',context_dict,context)

def transfer(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/transfer.html',context_dict,context)

def bdetail(request,t_id):
	context = RequestContext(request)	
	context_dict = {}
	if T.CheckExist(BOND,{'id':t_id}):
		BOND_obj = BOND.objects.get(id__exact = t_id)
		context_dict['bond'] = BOND_obj
	return render_to_response('qdinvest/bdetail.html',context_dict,context)

def sdetail(request,s_id):
	context = RequestContext(request)
	context_dict = {}
	if T.CheckExist(STOCK,{'id':s_id}):
		STOCK_obj = STOCK.objects.get(id__exact = s_id)
		context_dict['stock'] = STOCK_obj
	return render_to_response('qdinvest/sdetail.html',context_dict,context)

def db(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/models_doc.html',context_dict,context)