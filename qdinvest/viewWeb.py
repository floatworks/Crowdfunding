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
from  models import *

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

def account(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/account.html',context_dict,context)

def login(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == 'POST':
		u_name = request.POST.get('username','')
		u_pwd = request.POST.get('password','')
		print u_name,u_pwd
		if T.CheckExist(USERS,{'u_name':u_name,'u_pwd':u_pwd}):
			USERS_obj = USERS.objects.get(u_name = u_name,u_pwd=u_pwd)
			request.session['username'] = USERS_obj.u_name
			request.session['user_id'] = USERS_obj.id
			return HttpResponseRedirect('/c/account/')
		else:
			return HttpResponseRedirect('/c/login/')
	return render_to_response('qdinvest/login.html',context_dict,context)

def bdetail(request,t_id):
	context = RequestContext(request)	
	context_dict = {}
	if T.CheckExist(BOND,{'id':t_id}):
		BOND_obj = BOND.objects.get(id__exact = t_id)
		BOND_obj2 = INVEST_BOND.objects.filter(ib_bond__id__exact = t_id)
		context_dict['bond'] = BOND_obj
		context_dict['invest_bonds'] = BOND_obj2
	return render_to_response('qdinvest/bdetail.html',context_dict,context)

def sdetail(request,s_id):
	context = RequestContext(request)
	context_dict = {}
	if T.CheckExist(STOCK,{'id':s_id}):
		STOCK_obj = STOCK.objects.get(id__exact = s_id)	
		context_dict['stock'] = STOCK_obj
	STOCK_objs2 = INVEST_STOCK.objects.filter(is_stock__id__exact = s_id)
	context_dict['invest_stocks'] = STOCK_objs2
	return render_to_response('qdinvest/sdetail.html',context_dict,context)

def db(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/models_doc.html',context_dict,context)