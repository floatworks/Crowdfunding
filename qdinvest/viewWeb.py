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
import datetime
from datetime import timedelta
import datetime,time

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

	return render_to_response('qdinvest/index.html',context_dict,context)

def bond(request):
	context = RequestContext(request)	
	context_dict = {}
	kwargs = {}
	ct = request.GET.get('ct','')
	st = request.GET.get('st','')
	tr = request.GET.get('tr','')
	pt = request.GET.get('pt','')
	pageid = request.GET.get('page','1')
	context_dict['pageid'] = pageid	
	COM_TYPE_objs = COM_TYPE.objects.all()
	context_dict['com_types'] = COM_TYPE_objs	
	PRO_TYPE_objs = PRO_TYPE.objects.all()
	context_dict['pro_types'] = PRO_TYPE_objs
	
	if 	ct:			
		if ct == 'all':			
			request.session['ct_id'] = 'all2'
		else:
			request.session['ct_id'] = ct
			kwargs['bo_com_type'] = ct		
	else:
		if  request.session.has_key('ct_id'):			
			if  request.session['ct_id'] == 'all2':							
				ct = 1
			else:
				kwargs['bo_com_type'] = request.session['ct_id']
	if  st:
		if st == 'all':
			request.session['st_id'] = 'all2'
		else:
			request.session['st_id'] = st
	else:
		if  request.session.has_key('st_id'):
			ct=1
		else:			
			request.session['st_id'] = 'all2'



	if 	tr:			
		if tr == 'all':			
			request.session['tr_id'] = 'all2'
		else:
			if tr == '1':
				request.session['tr_id'] = 10		
				kwargs['bo_scale__lte'] = 10	
			if tr == '2':
				request.session['tr_id'] = 15	
				request.session['tr_id1'] = 10
				kwargs['bo_scale__lte'] = 15
				kwargs['bo_scale__gte'] = 10
			if tr == '3':
				request.session['tr_id'] = 20	
				request.session['tr_id1'] = 15
				kwargs['bo_scale__lte'] = 20
				kwargs['bo_scale__gte'] = 15
			if tr == '4':
				request.session['tr_id'] = 25	
				request.session['tr_id1'] = 20
				
				kwargs['bo_scale__gte'] = 20

	else:
		if  request.session.has_key('tr_id'):			
			if  request.session['tr_id'] == 'all2':							
				ct = 1
			else:
				if request.session['tr_id'] == 10:
					kwargs['bo_scale__lte'] = request.session['tr_id']
				if request.session['tr_id'] == 15:
					kwargs['bo_scale__lte'] = request.session['tr_id']
					kwargs['bo_scale__gte'] = request.session['tr_id1']
				if request.session['tr_id'] == 20:
					kwargs['bo_scale__lte'] = request.session['tr_id']
					kwargs['bo_scale__gte'] = request.session['tr_id1']
				if request.session['tr_id'] == 25:					
					kwargs['bo_scale__gte'] = request.session['tr_id1']

	if pt:	
		if pt == 'all':
			request.session['pt_id'] = 'all2'
		else: 
			request.session['pt_id'] = pt
			kwargs['bo_pro_type'] = pt		
	else:
		if  request.session.has_key('pt_id'):			
			if  request.session['pt_id'] == 'all2':				
				ct = 1	
			else:
				kwargs['bo_pro_type'] = request.session['pt_id']

	if kwargs or request.session.has_key('st_id'):	
		if  kwargs.has_key('bo_com_type'):
			context_dict['ct'] = int(kwargs['bo_com_type'])
		else:
			context_dict['ct'] = 'all'

		if  kwargs.has_key('bo_pro_type'):
			context_dict['pt'] = int(kwargs['bo_pro_type'])
		else:
			context_dict['pt'] = 'all'

		if  request.session.has_key('tr_id'):
			if request.session['tr_id'] == 'all2':
				context_dict['tr'] = 'all'
			if request.session['tr_id'] == 10:
				context_dict['tr'] = 1
			if request.session['tr_id'] == 15:
				context_dict['tr'] = 2
			if request.session['tr_id'] == 20:
				context_dict['tr'] = 3
			if request.session['tr_id'] == 25:
				context_dict['tr'] = 4




		if request.session.has_key('st_id'):
			if request.session['st_id'] == 'all2':
				BOND_objs1 = BOND.objects.filter(**kwargs)	
				context_dict['bonds'] = BOND_objs1
				context_dict['st'] = 'all'
			if request.session['st_id'] == '1':		
				dt = datetime.datetime.now() + datetime.timedelta(days = 90)			
				context_dict['bonds'] = BOND.objects.filter(**kwargs).filter(bo_end_time__lte = dt).filter(bo_end_time__gte = datetime.datetime.now())
				context_dict['st'] = 1
			if request.session['st_id'] == '2':	
				dt1 = datetime.datetime.now() + datetime.timedelta(days = 90)
				dt2 = dt1 + datetime.timedelta(days = 90)			
				context_dict['bonds'] = BOND.objects.filter(**kwargs).filter(bo_end_time__lte = dt2).filter(bo_end_time__gte = dt1)
				context_dict['st'] = 2
			if request.session['st_id'] == '3':	
				dt1 = datetime.datetime.now() + datetime.timedelta(days = 180)
				dt2 = dt1 + datetime.timedelta(days = 90)			
				context_dict['bonds'] = BOND.objects.filter(**kwargs).filter(bo_end_time__lte = dt2).filter(bo_end_time__gte = dt1)
				context_dict['st'] = 3
			if request.session['st_id'] == '4':	
				dt1 = datetime.datetime.now() + datetime.timedelta(days = 270)
				dt2 = dt1+ datetime.timedelta(days = 90)			
				context_dict['bonds'] = BOND.objects.filter(**kwargs).filter(bo_end_time__lte = dt2).filter(bo_end_time__gte = dt1)
				context_dict['st'] = 4
			if request.session['st_id'] == '5':	
				dt1 = datetime.datetime.now() + datetime.timedelta(days = 360)						
				context_dict['bonds'] = BOND.objects.filter(**kwargs).filter(bo_end_time__gte = dt1)
				context_dict['st'] = 5


	else:
		BOND_objs1 = BOND.objects.all()	
		context_dict['bonds'] = BOND_objs1	
		context_dict['ct'] = 'all'
		context_dict['st'] = 'all'
		context_dict['tr'] = 'all'
		context_dict['pt'] = 'all'
        
	context_dict['page_num'] = (len(context_dict['bonds'])+9)/10
	return render_to_response('qdinvest/bond.html',context_dict,context)

def stock(request):
	context = RequestContext(request)
	context_dict = {}
	kwargs = {}
	ct = request.GET.get('ct','')
	pt = request.GET.get('pt','')
	it = request.GET.get('it','')
	prt = request.GET.get('prt','')
	pageid = request.GET.get('page','1')
	context_dict['pageid'] = pageid
	PRO_TYPE_objs = PRO_TYPE.objects.all()
	context_dict['pro_types'] = PRO_TYPE_objs
	COM_TYPE_objs = COM_TYPE.objects.all()
	context_dict['com_types'] = COM_TYPE_objs
	INDUSTRY_objs = INDUSTRY.objects.all()
	context_dict['industrys'] = INDUSTRY_objs
	PROVINCE_objs = PROVINCE.objects.all()
	context_dict['provinces'] = PROVINCE_objs
  
	if 	ct:			
		if ct == 'all':			
			request.session['ct_id'] = 'all2'
		else:
			request.session['ct_id'] = ct
			kwargs['st_com_type'] = ct		
	else:
		if  request.session.has_key('ct_id'):
			if  request.session['ct_id'] == 'all2':
				ct = 1
			else:
				kwargs['st_com_type'] = request.session['ct_id']
		
	if pt:	
		if pt == 'all':
			request.session['pt_id'] = 'all2'
		else: 
			request.session['pt_id'] = pt
			kwargs['st_pro_type'] = pt		
	else:
		if  request.session.has_key('pt_id'):			
			if  request.session['pt_id'] == 'all2':				
				ct = 1	
			else:
				kwargs['st_pro_type'] = request.session['pt_id']		


	if it:	
		if it == 'all':
			request.session['it_id'] = 'all2'
		else: 
			request.session['it_id'] = it
			kwargs['st_industry'] = it		
	else:
		if  request.session.has_key('it_id'):			
			if  request.session['it_id'] == 'all2':				
				ct = 1	
			else:
				kwargs['st_industry'] = request.session['it_id']
	if prt:	
		if prt == 'all':
			request.session['prt_id'] = 'all2'
		else: 
			request.session['prt_id'] = prt
			kwargs['st_province'] = prt		
	else:
		if  request.session.has_key('prt_id'):			
			if  request.session['prt_id'] == 'all2':				
				ct = 1	
			else:
				kwargs['st_province'] = request.session['prt_id']
	if kwargs:		
		STOCK_objs1 = STOCK.objects.filter(**kwargs)	
		context_dict['stocks'] = STOCK_objs1

		if  kwargs.has_key('st_com_type'):
			context_dict['ct'] = int(kwargs['st_com_type'])
		else:
			context_dict['ct'] = "all"

		if  kwargs.has_key('st_pro_type'):
			context_dict['pt'] = int(kwargs['st_pro_type'])
		else:
			context_dict['pt'] = "all"

		if  kwargs.has_key('st_industry'):
			context_dict['it'] = int(kwargs['st_industry'])
		else:
			context_dict['it'] = 'all'

		if  kwargs.has_key('st_province'):
			context_dict['prt'] = int(kwargs['st_province'])
		else:
			context_dict['prt'] = 'all'
	else:		
		STOCK_objs1 = STOCK.objects.all()	
		context_dict['stocks'] = STOCK_objs1	
		context_dict['ct'] = 'all'
		context_dict['pt'] = 'all'
		context_dict['it'] = 'all'
		context_dict['prt'] = 'all'
	context_dict['page_num'] = (len(context_dict['stocks'])+9)/10
	return render_to_response('qdinvest/stock.html',context_dict,context)


def account(request):	
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/account.html',context_dict,context)

def login(request):
	context = RequestContext(request)
	context_dict = {}	
	if request.method == 'POST':
		if 'username' in request.POST:
			u_name = request.POST.get('username','')
			if not u_name:
				context_dict['errors1']='请输入姓名'
			else:
				context_dict['username'] = u_name
		if  'password' in  request.POST:
			u_pwd = request.POST.get('password','')
			if  not u_pwd:
				context_dict['errors2']='请输入密码'
			else:
				context_dict['password'] = u_pwd
		print u_name,u_pwd
		if T.CheckExist(USERS,{'u_name':u_name,'u_pwd':u_pwd}):
			USERS_obj = USERS.objects.get(u_name = u_name,u_pwd=u_pwd)
			request.session['username'] = USERS_obj.u_name
			request.session['user_id'] = USERS_obj.id			
			return HttpResponseRedirect('/c/account/')
		else:
			if u_name and u_pwd:
				context_dict['errors'] = '用户名与密码不匹配，请重新输入'
				return render_to_response('qdinvest/login.html',context_dict,context)
	return render_to_response('qdinvest/login.html',context_dict,context)	


def logout(request):
	context = RequestContext(request)
	context_dict = {}
	if request.session.has_key('username'):
		del request.session['username']
		del request.session['user_id']	
		return HttpResponseRedirect('/c/login/')
	else:	
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
def register(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/register.html',context_dict,context)