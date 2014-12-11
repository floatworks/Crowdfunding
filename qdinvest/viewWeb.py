#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q
from qdinvest.forms import USERSFORM

import tools as T
import simplejson as json
import datetime
from datetime import timedelta
import datetime,time
import re

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
		else:
			request.session['tr_id'] = 'all2'



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
				context_dict['tr'] ='all'
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
			BOND_objs1 = BOND.objects.filter(**kwargs)	
			context_dict['bonds'] = BOND_objs1



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




#用户登录
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
			return HttpResponseRedirect('/c/account_list/')
		else:
			if u_name and u_pwd:
				context_dict['errors'] = '用户名与密码不匹配，请重新输入'
				return render_to_response('qdinvest/login.html',context_dict,context)
	return render_to_response('qdinvest/login.html',context_dict,context)	

#用户名注销
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

#用户注册
def register(request):
	context = RequestContext(request)
	context_dict = {}
	registered = False
	if request.method == 'POST':						
		userData = request.POST.copy()
		userData.appendlist('u_status',0)
		userForm = USERSFORM(data = userData)	
		
		if userForm.is_valid():			
			registered = True
			userForm.save()
			context_dict['registered'] = registered
			return render_to_response('qdinvest/login.html',context_dict,context)
		else:
			print userForm.errors	
	context_dict['registered'] = registered		
	return render_to_response('qdinvest/register.html',context_dict,context)



#验证输入的用户名
def register1(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method=='GET':		
		username=request.GET.get('u_name','')
		if not username:			
			context_dict['msg'] = '请输入用户名'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")		
		m = re.match(r"^[a-zA-Z0-9]{1}[0-9a-zA-Z]{1,}$",username)		
		if not m:			
			context_dict['msg'] = '用户名为6至15位数字或字母'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		if len(username)<6:		
			context_dict['msg'] ='用户名长度不能小于6!'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		if len(username)>15:			
			context_dict['msg'] ='用户名长度不能大于15!'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		user = USERS.objects.filter(u_name=username)
		if user:			
			context_dict['msg'] ='该用户名已被占用！'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:			
			context_dict['msg'] = 'success'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")


#验证用户输入的手机号码
def register2(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method=='GET':		
		usertel=request.GET.get('u_tel','')
		if not usertel:			
			context_dict['msg'] = '请输入手机号码'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")		
		m = re.match(r"^13[0-9]{9}|15[012356789][0-9]{8}|18[0256789][0-9]{8}|147[0-9]{8}$",usertel)		
		if not m:			
			context_dict['msg'] = '你输入的电话号码无效'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		if len(usertel)!=11:
			context_dict['msg'] ='电话号码长度应为11位!'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")		
		user = USERS.objects.filter(u_tel=usertel)
		if user:			
			context_dict['msg'] ='该电话号码已被占用！'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:			
			context_dict['msg'] = 'success'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
# 点击手机获取验证码与验证码存入数据库
def test(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method=='GET':		
		usertel=request.GET.get('u_telephone','')
		if usertel:
			if T.SendRandomCode(usertel):
				context_dict['msg'] = 'success'
				return HttpResponse(json.dumps(context_dict),content_type="application/json")
			else:
				context_dict['msg'] = '请重新点击获取验证码'
				return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:
			context_dict['msg'] = '请重新输入手机号码'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")

#判断输入验证码正确性
def test1(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method=='GET':			
		test1=request.GET.get('u_test','')
		usertel=request.GET.get('u_telephone','')		
		if T.CheckRandomCode(usertel,test1):					
			context_dict['msg'] = 'success'		
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:		
			context_dict['msg'] = '验证码输入错误'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")


#找回密码
def  forget(request):
	context = RequestContext(request)
	context_dict = {}
	kwargs={}
	if request.method=='POST':		
		test=request.POST.get('rc_code','')
		telephone=request.POST.get('u_tel','')	
		password=request.POST.get('u_pwd','')
		print test,telephone,password		
		if T.CheckExist(RANDOMCODE,{'rc_tel':telephone,'rc_code':test}):			
			USERS.objects.filter(u_tel=telephone).update(u_pwd=password)
			return HttpResponseRedirect('/c/login/')
		else:			
			context_dict['error'] = '手机号码与验证码不符'
	return render_to_response('qdinvest/forget.html',context_dict,context)

#找回页面用户名的验证
def forget1(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == 'GET':			
		username=request.GET.get('u_name','')					
		if T.CheckExist(USERS,{'u_name':username}):			
			context_dict['msg'] = 'success'		
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:		
			context_dict['msg'] = '此用户名未注册过,无法找回密码'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")


def forget3(request):
	context = RequestContext(request)
	context_dict = {}	
	if request.method == 'GET':			
		usertel=request.GET.get('u_tel','')
		username=request.GET.get('username','')
		if not usertel:			
			context_dict['msg'] = '请输入手机号码'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")		
		m = re.match(r"^13[0-9]{9}|15[012356789][0-9]{8}|18[0256789][0-9]{8}|147[0-9]{8}$",usertel)		
		if not m:			
			context_dict['msg'] = '你输入的电话号码无效'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		if len(usertel)!=11:
			context_dict['msg'] ='电话号码长度应为11位!'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")		
		user = USERS.objects.filter(u_tel=usertel,u_name=username)
		if user:			
			context_dict['msg'] ='success'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:			
			context_dict['msg'] = '你输入的手机号码与用户名不相符'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")

#获取手机验证码
def forget4(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method=='GET':		
		usertel=request.GET.get('u_telephone','')
		if usertel:
			if T.SendRandomCode(usertel):
				context_dict['msg'] = 'success'
				return HttpResponse(json.dumps(context_dict),content_type="application/json")
			else:
				context_dict['msg'] = '请重新点击获取验证码'
				return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:
			context_dict['msg'] = '输入有误，请重新输入手机号码'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
#检验验证码
def forget5(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method=='GET':			
		test1=request.GET.get('tcod','')
		usertel=request.GET.get('telephone1','')		
		if T.CheckRandomCode(usertel,test1):			
			context_dict['msg'] = 'success'		
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		else:		
			context_dict['msg'] = '验证码输入错误'
			return HttpResponse(json.dumps(context_dict),content_type="application/json")
		





#个人中心页面中账户信息的显示
def account_list(request):
	context = RequestContext(request)
	context_dict = {}
	if request.session.has_key('username'):	
		u_name = request.session['username']	
		ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__u_name = u_name)	
		context_dict['account'] = ACCOUNT_objs	
		context_dict['account_list'] =1
	else:
		return HttpResponseRedirect('/c/login/')
	return render_to_response('qdinvest/account_list.html',context_dict,context)

#个人页面中股权项目页面的显示
def stock_list(request):
	context = RequestContext(request)
	context_dict = {}	
	invest = []
	st_invest_price = 0
	if request.session.has_key('username'):
		u_name = request.session['username']		
		STOCK_objs1 = INVEST_STOCK.objects.filter(is_user__u_name = u_name)
		context_dict['invest_stocks'] = STOCK_objs1
		if STOCK_objs1:
			for STOCK_obj in STOCK_objs1:					
				st_invest_price += STOCK_obj.is_amount		
			STOCK_ids = INVEST_STOCK.objects.filter(is_user__u_name = u_name).values('is_stock').distinct()				
			if 	STOCK_ids:
				for STOCK_id in STOCK_ids:			
					STOCK_obj = STOCK.objects.get(id__exact = STOCK_id['is_stock'])
					invest.append({'id':STOCK_obj.id,'st_brief':STOCK_obj.st_brief,'st_com_type':STOCK_obj.st_com_type,'st_pro_type':STOCK_obj.st_pro_type,'st_industry':STOCK_obj.st_industry})	
			context_dict['stocks'] = invest
		context_dict['invest_price'] = st_invest_price
		context_dict['stock_list'] = 1
	else:
		return HttpResponseRedirect('/c/login/')
	return render_to_response('qdinvest/stock_list.html',context_dict,context)

#个人页面中债权项目页面的显示
def bond_list(request):
	context = RequestContext(request)
	context_dict = {}	
	invest = []
	ib_invest_price = 0
	if request.session.has_key('username'):
		u_name = request.session['username']		
		BOND_objs1 = INVEST_BOND.objects.filter(ib_user__u_name = u_name)
		context_dict['invest_bonds'] = BOND_objs1
		if BOND_objs1:
			for BOND_obj in BOND_objs1:					
				ib_invest_price += BOND_obj.ib_amount				
			BOND_ids = INVEST_BOND.objects.filter(ib_user__u_name = u_name).values('ib_bond').distinct()
			if	BOND_ids:		
				for BOND_id in BOND_ids:			
					BOND_obj = BOND.objects.get(id__exact = BOND_id['ib_bond'])
					invest.append({'id':BOND_obj.id,'bo_title':BOND_obj.bo_title,'bo_com_type':BOND_obj.bo_com_type,'bo_pro_type':BOND_obj.bo_pro_type,'bo_industry':BOND_obj.bo_industry})	
			context_dict['bonds'] = invest
		context_dict['invest_price'] = ib_invest_price
		context_dict['bond_list'] = 1
	else:
		return HttpResponseRedirect('/c/login/')
	return render_to_response('qdinvest/bond_list.html',context_dict,context)

#个人页面中消息页面的显示
def news(request):
	context = RequestContext(request)
	context_dict = {}
	if request.session.has_key('username'):
		u_name = request.session['username']
		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:			
			notices = []
			notice_user=[]
			NOTICE_objs = NOTICE.objects.filter(no_is_delete__exact = 0).order_by('-no_time')	
			if 	NOTICE_objs:				
				for NOTICE_obj in NOTICE_objs:					
					notice_data = {}
					notice_data['id'] = NOTICE_obj.id
					notice_data['no_title'] = NOTICE_obj.no_title				
					notice_data['no_time'] = NOTICE_obj.no_time
					notice_data['no_type'] = NOTICE_obj.no_type				
					notice_data['type'] = 'sys'				
					if T.CheckExist(NOTICE_READ,{'nr_user':USERS_objs[0],'nr_notice':NOTICE_obj}):
						notice_data['no_is_read'] = 1
					else:
						notice_data['no_is_read'] = 0						
					notices.append(notice_data)
					context_dict['notices'] = notices	
					# print 		context_dict['notices'][0]			
			NOTICE_USER_objs = NOTICE_USER.objects.filter(nu_is_delete__exact = 0,nu_user__exact = USERS_objs[0]).order_by('-nu_time')
			if  NOTICE_USER_objs:
				for NOTICE_USER_obj in NOTICE_USER_objs:					
					notice_data1= {}
					notice_data1['id'] = NOTICE_USER_obj.id
					notice_data1['nu_title'] = NOTICE_USER_obj.nu_title
					# print notice_data1['nu_title']
					notice_data1['nu_time'] = NOTICE_USER_obj.nu_time
					notice_data1['nu_type'] = NOTICE_USER_obj.nu_type
					notice_data1['nu_is_read'] = NOTICE_USER_obj.nu_is_read							
					notice_data1['type'] = 'user'					
					notice_user.append(notice_data1)
					#按照时间的倒序进行排列			
					context_dict['notice_users'] = notice_user
					print  context_dict['notice_users'][0]

			context_dict['status'] = 1	

		else:
			context_dict['status'] = 0	
		context_dict['news'] = 1
	return render_to_response('qdinvest/news.html',context_dict,context)

def news2(request):	
	context = RequestContext(request)
	context_dict = {}
	if request.session.has_key('username'):
		u_name = request.session['username']
	if request.method == 'GET':
		n_type = request.GET.get('type','')
		n_id = request.GET.get('id','-1')
		context_dict['type'] = n_type
		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
				if n_type == 'sys':
					NOTICE_objs = NOTICE.objects.filter(id__exact = n_id)
					context_dict['notices'] = NOTICE_objs
					if NOTICE_objs:						
						if not T.CheckExist(NOTICE_READ,{'nr_user':USERS_objs[0],'nr_notice':NOTICE_objs[0]}):
							NOTICE_READ_new = NOTICE_READ(nr_user = USERS_objs[0],nr_notice = NOTICE_objs[0])
							NOTICE_READ_new.save()
							ACCOUNT_obj = ACCOUNT.objects.get(ac_user = USERS_objs[0])
							ACCOUNT_obj.ac_infos -= 1
							ACCOUNT_obj.save()					
				elif n_type == 'user':
					NOTICE_USER_objs = NOTICE_USER.objects.filter(id__exact = n_id)
					context_dict['notice_users'] = NOTICE_USER_objs
					if NOTICE_USER_objs:											
						if NOTICE_USER_objs[0].nu_is_read == 0:
							ACCOUNT_obj = ACCOUNT.objects.get(ac_user = USERS_objs[0])
							ACCOUNT_obj.ac_infos -= 1
							ACCOUNT_obj.save()
						#标记为已经阅读
						NOTICE_USER_objs[0].nu_is_read = 1
						NOTICE_USER_objs[0].save()	
		context_dict['news2'] = 1
	return render_to_response('qdinvest/news2.html',context_dict,context)
