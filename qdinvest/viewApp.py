#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q
from django.conf import settings
from django.http import Http404

from models import *
from forms import *
import tools as T

import requests
import simplejson as json
from datetime import datetime,timedelta
from xml.etree import ElementTree
import operator

#手机端用户注册接口
def Register(request):
	response_dict = {}

	if request.method == 'POST':
		userData = request.POST.copy()
		u_name = userData.get('u_name','')
		u_tel = userData.get('u_tel','')
		code = userData.get('code','')
		if T.CheckExist(USERS,{'u_name':u_name}):
			response_dict['status'] = 2
		elif T.CheckExist(USERS,{'u_tel':u_tel}):
			response_dict['status'] = 3
		elif not CheckRandomCode(u_tel,code):
			response_dict['status'] = 4
		else:
			userData.appendlist('u_status',0)
			userForm = USERSFORM(data = userData)
			if userForm.is_valid():
				userForm.save()
				#创建用户的时候同时需要创建用户账户
				USERS_obj = USERS.objects.get(u_name__exact = u_name)
				ACCOUNT_new = ACCOUNT(ac_user=USERS_obj,ac_like=0,ac_support=0,ac_sponsor=0,ac_infos=0,
							ac_stock_invest=0,ac_bond_invest=0,ac_total_invest=0,ac_stock_profit=0,ac_bond_profit=0,
							ac_total_profit=0,ac_subscription=0,ac_total_subscription=0)
				ACCOUNT_new.save()
				response_dict['status'] = 1
			else:
				response_dict['status'] = 0
				if settings.DEBUG:
					response_dict['error'] = userForm.errors
					print userForm.errors
	
	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#手机端用户获取账户信息
def GetAccount(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__exact = USERS_objs[0])
				if ACCOUNT_objs:
					response_dict['status'] = 1
					account = json.loads(serializers.serialize("json", ACCOUNT_objs))[0]['fields']
					account['u_name'] = u_name
					response_dict['account'] = account
				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#判断用户的验证码是否错误或者超时 5min
def CheckRandomCode(u_tel,code):
	randomCode_obj = RANDOMCODE.objects.filter(rc_tel__exact = u_tel)
	if randomCode_obj:
		if randomCode_obj[0].rc_code == code and (datetime.now() - randomCode_obj[0].rc_time).seconds < 300:
			return True
		else:
			return False
	else:
		return False

#手机端用户获取验证码
def GetRandomCode(request):
	response_dict = {}
	if request.method == 'GET':
		u_tel = request.GET.get('u_tel','')
		u_type = request.GET.get('type','')
		if u_tel and u_type:
			print u_tel,u_type
			if u_type == 'reg':
				if T.CheckExist(USERS,{'u_tel':u_tel}):
					response_dict['status'] = 2
				elif T.SendRandomCode(u_tel):
					response_dict['status'] = 1
				else:
					response_dict['status'] = 0
			elif u_type == 'forget':
				if not T.CheckExist(USERS,{'u_tel':u_tel}):
					response_dict['status'] = 2
				elif T.SendRandomCode(u_tel):
					response_dict['status'] = 1
				else:
					response_dict['status'] = 0
		else:
			response_dict['status'] = 0


	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")


#手机端用户登录接口
def Login(request):
	response_dict = {}

	if request.method == 'POST':
		u_name = request.POST.get('u_name','')
		u_pwd = request.POST.get('u_pwd','')

		if u_name and u_pwd:
			USERS_objs = USERS.objects.filter(u_name__exact = u_name,u_pwd__exact = u_pwd)
			if USERS_objs:
				response_dict['status'] = 1
				token = T.GenToken()
				response_dict['token'] = token
				T.CheckToken(USERS_objs[0],token,1)
			else:
				response_dict['status'] = 0
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#APP端用户修改密码
def RePassWord(request):
	response_dict = {}

	if request.method == 'POST':
		token = request.POST.get('token','')
		u_name = request.POST.get('u_name','')
		u_pwd = request.POST.get('u_pwd','')
		u_npwd = request.POST.get('u_npwd','')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				if u_pwd:
					if USERS_objs[0].u_pwd == u_pwd:
						USERS_objs[0].u_pwd = u_npwd
						USERS_objs[0].save()
						response_dict['status'] = 1
					else:
						response_dict['status'] = 2
				else:
					USERS_objs[0].u_pwd = u_npwd
					USERS_objs[0].save()
					response_dict['status'] = 1
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#APP密码找回
def Forget(request):
	response_dict = {}

	if request.method == 'POST':
		u_tel = request.POST.get('u_tel','')
		code = request.POST.get('code','')

		if CheckRandomCode(u_tel,code):
			response_dict['status'] = 1
			USERS_objs = USERS.objects.filter(u_tel__exact = u_tel)
			if USERS_objs:
				token = T.GenToken()
				T.CheckToken(USERS_objs[0],token,1)
				response_dict['u_name'] = USERS_objs[0].u_name
				response_dict['token'] = token
			else:
				response_dict['status'] = 0
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#获取项目列表
def GetProjects(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')
		num = request.GET.get('num','')
		if not num:
			num = 0
		num = int(num)
		print token,num

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				response_dict['status'] = 1
				stocks_data = []
				STOCK_objs = STOCK.objects.order_by('-st_create_time')[num*20:(num+1)*20]
				for STOCK_obj in STOCK_objs:
					stocks_per = {}
					stocks_per['id'] = STOCK_obj.id
					stocks_per['st_title'] = STOCK_obj.st_title
					stocks_per['st_image'] = str(STOCK_obj.st_image)
					stocks_per['st_pro_type'] = STOCK_obj.st_pro_type.pt_name
					stocks_per['st_province'] = STOCK_obj.st_province.pr_name
					stocks_per['st_industry'] = STOCK_obj.st_industry.in_name
					stocks_per['st_com_type'] = STOCK_obj.st_com_type.ct_name
					stocks_per['st_view_count'] = STOCK_obj.st_view_count
					stocks_per['st_like_count'] = STOCK_obj.st_like_count
					stocks_per['st_invest_count'] = STOCK_obj.st_invest_count
					stocks_per['st_current_price'] = STOCK_obj.st_current_price
					stocks_per['st_total_price'] = STOCK_obj.st_total_price
					stocks_per['st_min_price'] = STOCK_obj.st_min_price
					stocks_per['st_create_time'] = STOCK_obj.st_create_time.strftime('%Y-%m-%d %H:%M:%S')
					stocks_data.append(stocks_per)
				response_dict['stocks'] = stocks_data
				bonds_data = []
				BOND_objs = BOND.objects.order_by('-bo_create_time')[num*20:(num+1)*20]
				for BOND_obj in BOND_objs:
					bonds_per = {}
					bonds_per['id'] = BOND_obj.id
					bonds_per['bo_title'] = BOND_obj.bo_title
					bonds_per['bo_image'] = str(BOND_obj.bo_image)
					bonds_per['bo_com_name'] = BOND_obj.bo_com_name
					bonds_per['bo_pro_type'] = BOND_obj.bo_pro_type.pt_name
					bonds_per['bo_brief'] = BOND_obj.bo_brief
					bonds_per['bo_scale'] = BOND_obj.bo_scale
					bonds_per['bo_total_price'] = BOND_obj.bo_total_price
					bonds_per['bo_current_price'] = BOND_obj.bo_current_price
					bonds_per['bo_min_price'] = BOND_obj.bo_min_price
					bonds_per['bo_create_time'] = BOND_obj.bo_create_time.strftime('%Y-%m-%d %H:%M:%S')
					bonds_data.append(bonds_per)
				response_dict['bonds'] = bonds_data
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#用户获取与之相关的数据
def GetMyProjects(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				response_dict['status'] = 1
				stocks_data = []
				STOCK_ids = INVEST_STOCK.objects.filter(is_user__exact = USERS_objs[0]).values('is_stock').distinct()
				for STOCK_id in STOCK_ids:
					INVEST_STOCK_obj = STOCK.objects.get(id__exact = STOCK_id['is_stock'])
					stocks_per = {}
					stocks_per['id'] = INVEST_STOCK_obj.id
					stocks_per['st_title'] = INVEST_STOCK_obj.st_title
					stocks_per['st_image'] = str(INVEST_STOCK_obj.st_image)
					stocks_per['st_total_price'] = INVEST_STOCK_obj.st_total_price
					#stocks_per['is_amount'] = INVEST_STOCK_obj.is_amount
					st_status_list = list(INVEST_STOCK.objects.filter(is_user__exact = USERS_objs[0],is_stock__exact = INVEST_STOCK_obj).values('is_status').distinct())
					is_status = []
					for st_status_l in st_status_list:
						is_status.append(st_status_l['is_status'])
					stocks_per['is_status'] = is_status
					#stocks_per['is_status'] = INVEST_STOCK_obj.is_status
					stocks_per['st_brief'] = INVEST_STOCK_obj.st_brief 
					#求最新一条记录的时间
					INVEST_STOCK_objs = INVEST_STOCK.objects.filter(is_user__exact = USERS_objs[0],is_stock__exact = INVEST_STOCK_obj).order_by('-is_date')
					if INVEST_STOCK_objs:
						stocks_per['is_date'] = INVEST_STOCK_objs[0].is_date.strftime('%Y-%m-%d %H:%M:%S')
					stocks_data.append(stocks_per)
				response_dict['invest_stocks'] = stocks_data
				bonds_data = []
				BOND_ids = INVEST_BOND.objects.filter(ib_user__exact = USERS_objs[0]).values('ib_bond').distinct()
				for BOND_id in BOND_ids:
					INVEST_BOND_obj = BOND.objects.get(id__exact = BOND_id['ib_bond'])
					bonds_per = {}
					bonds_per['id'] = INVEST_BOND_obj.id
					bonds_per['bo_title'] = INVEST_BOND_obj.bo_title
					bonds_per['bo_image'] = str(INVEST_BOND_obj.bo_image)
					bonds_per['bo_total_price'] = INVEST_BOND_obj.bo_total_price
					#bonds_per['ib_amount'] = INVEST_BOND_obj.ib_amount
					bo_status_list =  list(INVEST_BOND.objects.filter(ib_user__exact = USERS_objs[0],ib_bond__exact = INVEST_BOND_obj).values('ib_status').distinct())
					ib_status = []
					for bo_status_l in bo_status_list:
						ib_status.append(bo_status_l['ib_status'])
					bonds_per['ib_status'] = ib_status
					#bonds_per['ib_status'] = INVEST_BOND_obj.ib_status
					bonds_per['bo_brief'] = INVEST_BOND_obj.bo_brief
					#求最新一条记录的时间
					INVEST_BOND_objs = INVEST_BOND.objects.filter(ib_user__exact = USERS_objs[0],ib_bond__exact = INVEST_BOND_obj).order_by('-ib_date')
					if INVEST_BOND_objs:
						bonds_per['ib_date'] = INVEST_BOND_objs[0].ib_date.strftime('%Y-%m-%d %H:%M:%S')
					bonds_data.append(bonds_per)
				response_dict['invest_bonds'] = bonds_data
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#获取项目相关的认购列表，同时返回项目基本信息
def ProjectInvest(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')
		p_type = request.GET.get('type','')
		p_id = request.GET.get('id','-1')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				if p_type == 'stock':
					if T.CheckExist(STOCK,{'id':p_id}):
						response_dict['status'] = 1
						STOCK_obj = STOCK.objects.get(id__exact = p_id)
						project = {}
						project['id'] = STOCK_obj.id
						project['st_title'] = STOCK_obj.st_title
						project['st_image'] = str(STOCK_obj.st_image)
						project['st_brief'] = STOCK_obj.st_brief
						project['st_total_price'] = STOCK_obj.st_total_price
						project['st_current_price'] = STOCK_obj.st_current_price
						invests = []
						st_invest_price = 0
						INVEST_STOCK_objs = INVEST_STOCK.objects.filter(is_user = USERS_objs[0],is_stock = STOCK_obj)
						for INVEST_STOCK_obj in INVEST_STOCK_objs:
							invests.append({'is_amount':INVEST_STOCK_obj.is_amount,'is_date':INVEST_STOCK_obj.is_date.strftime('%Y-%m-%d'),'is_status':INVEST_STOCK_obj.is_status.id})
							st_invest_price += INVEST_STOCK_obj.is_amount
						#判断是否已经交定金
						if T.CheckExist(PAYMENT,{'pa_user':USERS_objs[0],'pa_stock':STOCK_obj,'pa_status':0}):
							project['is_payment'] = 1
						else:
							project['is_payment'] = 0
						project['st_invest_price'] = st_invest_price
						response_dict['project'] = project
						response_dict['invests'] = invests
					else:
						response_dict['status'] = 0
				elif p_type == 'bond':
					if T.CheckExist(BOND,{'id':p_id}):
						response_dict['status'] = 1
						BOND_obj = BOND.objects.get(id__exact = p_id)
						project = {}
						project['id'] = BOND_obj.id
						project['bo_title'] = BOND_obj.bo_title
						project['bo_image'] = str(BOND_obj.bo_image)
						project['bo_brief'] = BOND_obj.bo_brief
						project['bo_total_price'] = BOND_obj.bo_total_price
						project['bo_current_price'] = BOND_obj.bo_current_price
						invests = []
						bo_invest_price = 0
						INVEST_BOND_objs = INVEST_BOND.objects.filter(ib_user = USERS_objs[0],ib_bond = BOND_obj)
						for INVEST_BOND_obj in INVEST_BOND_objs:
							invests.append({'ib_amount':INVEST_BOND_obj.ib_amount,'ib_date':INVEST_BOND_obj.ib_date.strftime('%Y-%m-%d'),'ib_status':INVEST_BOND_obj.ib_status.id})
							bo_invest_price += INVEST_BOND_obj.ib_amount
						#判断是否已经交定金
						if T.CheckExist(PAYMENT,{'pa_user':USERS_objs[0],'pa_bond':BOND_obj,'pa_status':0}):
							project['is_payment'] = 1
						else:
							project['is_payment'] = 0
						project['bo_invest_price'] = bo_invest_price
						response_dict['project'] = project
						response_dict['invests'] = invests
					else:
						response_dict['status'] = 0
				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#根据排序获取项目列表
def GetProjectsSort(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')
		num = request.GET.get('num','')
		if not num:
			num = 0
		num = int(num)
		print token,num

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				response_dict['status'] = 1
				stocks_data = []
				STOCK_objs = STOCK.objects.order_by('st_sort')[num*20:(num+1)*20]
				for STOCK_obj in STOCK_objs:
					stocks_per = {}
					stocks_per['id'] = STOCK_obj.id
					stocks_per['st_title'] = STOCK_obj.st_title
					stocks_per['st_image'] = str(STOCK_obj.st_image)
					stocks_per['st_pro_type'] = STOCK_obj.st_pro_type.pt_name
					stocks_per['st_province'] = STOCK_obj.st_province.pr_name
					stocks_per['st_industry'] = STOCK_obj.st_industry.in_name
					stocks_per['st_com_type'] = STOCK_obj.st_com_type.ct_name
					stocks_per['st_like_count'] = STOCK_obj.st_like_count
					stocks_per['st_invest_count'] = STOCK_obj.st_invest_count
					stocks_per['st_current_price'] = STOCK_obj.st_current_price
					stocks_per['st_total_price'] = STOCK_obj.st_total_price
					stocks_per['st_min_price'] = STOCK_obj.st_min_price
					stocks_per['st_create_time'] = STOCK_obj.st_create_time.strftime('%Y-%m-%d %H:%M:%S')
					stocks_data.append(stocks_per)
				response_dict['stocks'] = stocks_data
				bonds_data = []
				BOND_objs = BOND.objects.order_by('bo_sort')[num*20:(num+1)*20]
				for BOND_obj in BOND_objs:
					bonds_per = {}
					bonds_per['id'] = BOND_obj.id
					bonds_per['bo_title'] = BOND_obj.bo_title
					bonds_per['bo_image'] = str(BOND_obj.bo_image)
					bonds_per['bo_com_name'] = BOND_obj.bo_com_name
					bonds_per['bo_pro_type'] = BOND_obj.bo_pro_type.pt_name
					bonds_per['bo_brief'] = BOND_obj.bo_brief
					bonds_per['bo_scale'] = BOND_obj.bo_scale
					bonds_per['bo_total_price'] = BOND_obj.bo_total_price
					bonds_per['bo_current_price'] = BOND_obj.bo_current_price
					bonds_per['bo_min_price'] = BOND_obj.bo_min_price
					bonds_per['bo_create_time'] = BOND_obj.bo_create_time.strftime('%Y-%m-%d %H:%M:%S')
					bonds_data.append(bonds_per)
				response_dict['bonds'] = bonds_data
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")


#APP端根据关键字搜索项目
def SearchProject(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')
		num = request.GET.get('num','')
		keyword = request.GET.get('keyword','')
		if not num:
			num = 0
		num = int(num)
		print token,num

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				response_dict['status'] = 1
				stocks_data = []
				STOCK_objs = STOCK.objects.filter(st_title__contains = keyword).order_by('st_sort')[num*20:(num+1)*20]
				for STOCK_obj in STOCK_objs:
					stocks_per = {}
					stocks_per['id'] = STOCK_obj.id
					stocks_per['st_title'] = STOCK_obj.st_title
					stocks_per['st_image'] = str(STOCK_obj.st_image)
					stocks_per['st_pro_type'] = STOCK_obj.st_pro_type.pt_name
					stocks_per['st_province'] = STOCK_obj.st_province.pr_name
					stocks_per['st_industry'] = STOCK_obj.st_industry.in_name
					stocks_per['st_com_type'] = STOCK_obj.st_com_type.ct_name
					stocks_per['st_like_count'] = STOCK_obj.st_like_count
					stocks_per['st_invest_count'] = STOCK_obj.st_invest_count
					stocks_per['st_current_price'] = STOCK_obj.st_current_price
					stocks_per['st_total_price'] = STOCK_obj.st_total_price
					stocks_per['st_min_price'] = STOCK_obj.st_min_price
					stocks_per['st_create_time'] = STOCK_obj.st_create_time.strftime('%Y-%m-%d %H:%M:%S')
					stocks_data.append(stocks_per)
				response_dict['stocks'] = stocks_data
				bonds_data = []
				BOND_objs = BOND.objects.filter(bo_title__contains = keyword).order_by('bo_sort')[num*20:(num+1)*20]
				for BOND_obj in BOND_objs:
					bonds_per = {}
					bonds_per['id'] = BOND_obj.id
					bonds_per['bo_title'] = BOND_obj.bo_title
					bonds_per['bo_image'] = str(BOND_obj.bo_image)
					bonds_per['bo_com_name'] = BOND_obj.bo_com_name
					bonds_per['bo_pro_type'] = BOND_obj.bo_pro_type.pt_name
					bonds_per['bo_brief'] = BOND_obj.bo_brief
					bonds_per['bo_scale'] = BOND_obj.bo_scale
					bonds_per['bo_total_price'] = BOND_obj.bo_total_price
					bonds_per['bo_current_price'] = BOND_obj.bo_current_price
					bonds_per['bo_min_price'] = BOND_obj.bo_min_price
					bonds_per['bo_create_time'] = BOND_obj.bo_create_time.strftime('%Y-%m-%d %H:%M:%S')
					bonds_data.append(bonds_per)
				response_dict['bonds'] = bonds_data
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#获取项目基础信息
def ProjectBase(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')
		p_type = request.GET.get('type','')
		p_id = request.GET.get('id','-1')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				if p_type == 'stock':
					if T.CheckExist(STOCK,{'id':p_id}):
						stock_dict = {}
						STOCK_obj = STOCK.objects.get(id__exact = p_id)
						response_dict['status'] = 1
						stock_dict['st_image'] = str(STOCK_obj.st_image)
						stock_dict['st_title'] = STOCK_obj.st_title
						stock_dict['st_like_count'] = STOCK_obj.st_like_count
						stock_dict['st_invest_count'] = STOCK_obj.st_invest_count
						stock_dict['st_view_count'] = STOCK_obj.st_view_count
						stock_dict['st_province'] = STOCK_obj.st_province.pr_name
						stock_dict['st_industry'] = STOCK_obj.st_industry.in_name
						stock_dict['st_com_type'] = STOCK_obj.st_com_type.ct_name
						stock_dict['st_pro_type'] = STOCK_obj.st_pro_type.pt_name
						stock_dict['st_end_time'] = STOCK_obj.st_end_time.strftime('%Y-%m-%d %H:%M:%S')
						stock_dict['st_current_price'] = STOCK_obj.st_current_price
						stock_dict['st_total_price'] = STOCK_obj.st_total_price
						stock_dict['st_min_price'] = STOCK_obj.st_min_price
						stock_dict['st_invest_count'] = STOCK_obj.st_invest_count
						stock_dict['st_detail'] = '/w/prodetail/tsd'+p_id
						#获取用户是否已经关注
						if T.CheckExist(USER_FOCUS,{'uf_user':USERS_objs[0],'uf_stock':STOCK_obj}):
							stock_dict['st_if_like'] = 1
						else:
							stock_dict['st_if_like'] = 0
						response_dict['project'] = stock_dict
						#热度增加1
						STOCK_obj.st_view_count += 1
						STOCK_obj.save()
					else:
						response_dict['status'] = 0
				elif p_type == 'bond':
					if T.CheckExist(BOND,{'id':p_id}):
						bond_dict = {}
						BOND_obj = BOND.objects.get(id__exact = p_id)
						response_dict['status'] = 1
						bond_dict['bo_image'] = str(BOND_obj.bo_image)
						bond_dict['bo_title'] = BOND_obj.bo_title
						bond_dict['bo_like_count'] = BOND_obj.bo_like_count
						bond_dict['bo_view_count'] = BOND_obj.bo_view_count
						bond_dict['bo_province'] = BOND_obj.bo_province.pr_name
						bond_dict['bo_industry'] = BOND_obj.bo_industry.in_name
						bond_dict['bo_com_type'] = BOND_obj.bo_com_type.ct_name
						bond_dict['bo_pro_type'] = BOND_obj.bo_pro_type.pt_name
						bond_dict['bo_end_time'] = BOND_obj.bo_end_time.strftime('%Y-%m-%d %H:%M:%S')
						bond_dict['bo_current_price'] = BOND_obj.bo_current_price
						bond_dict['bo_total_price'] = BOND_obj.bo_total_price
						bond_dict['bo_scale'] = BOND_obj.bo_scale
						bond_dict['bo_invest_count'] = BOND_obj.bo_invest_count
						bond_dict['bo_detail'] = '/w/prodetail/tbd'+p_id
						#获取用户是否已经关注
						if T.CheckExist(USER_FOCUS,{'uf_user':USERS_objs[0],'uf_bond':BOND_obj}):
							bond_dict['bo_if_like'] = 1
						else:
							bond_dict['bo_if_like'] = 0
						response_dict['project'] = bond_dict
						BOND_obj.bo_view_count += 1
						BOND_obj.save()
					else:
						response_dict['status'] = 0
				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#用户关注或取消关注某个项目
#代码写得这么烂，十年前你自己知道不？
def ProLike(request):
	response_dict = {}

	if request.method == 'POST':
		token = request.POST.get('token','')
		u_name = request.POST.get('u_name','')
		p_type = request.POST.get('type','')
		p_id = request.POST.get('id','-1')
		focus = request.POST.get('focus','')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				if focus == 'like':
					if p_type == 'stock':
						STOCK_objs = STOCK.objects.filter(id__exact = p_id)
						if STOCK_objs:
							if T.CheckExist(USER_FOCUS,{'uf_user':USERS_objs[0],'uf_stock':STOCK_objs[0]}):
								response_dict['status'] = 2
							else:
								USER_FOCUS_new = USER_FOCUS(uf_user = USERS_objs[0],uf_stock = STOCK_objs[0],uf_update_time = datetime.now())
								USER_FOCUS_new.save()
								ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__exact = USERS_objs[0])
								if ACCOUNT_objs:
									ACCOUNT_objs[0].ac_like += 1
									ACCOUNT_objs[0].save()
								STOCK_objs[0].st_like_count += 1
								STOCK_objs[0].save()
								response_dict['status'] = 1
						else:
							response_dict['status'] = 0
					elif p_type == 'bond':
						BOND_objs = BOND.objects.filter(id__exact = p_id)
						if BOND_objs:
							if T.CheckExist(USER_FOCUS,{'uf_user':USERS_objs[0],'uf_bond':BOND_objs[0]}):
								response_dict['status'] = 2
							else:
								USER_FOCUS_new = USER_FOCUS(uf_user = USERS_objs[0],uf_bond = BOND_objs[0],uf_update_time = datetime.now())
								USER_FOCUS_new.save()
								ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__exact = USERS_objs[0])
								if ACCOUNT_objs:
									ACCOUNT_objs[0].ac_like += 1
									ACCOUNT_objs[0].save()
								BOND_objs[0].bo_like_count += 1
								BOND_objs[0].save()
								response_dict['status'] = 1
						else:
							response_dict['status'] = 0
					else:
						response_dict['status'] = 0
				elif focus == 'unlike':
					if p_type == 'stock':
						STOCK_objs = STOCK.objects.filter(id__exact = p_id)
						if STOCK_objs:
							USER_FOCUS_objs = USER_FOCUS.objects.filter(uf_user = USERS_objs[0],uf_stock = STOCK_objs[0])
							if USER_FOCUS_objs:
								USER_FOCUS_objs[0].delete()
								ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__exact = USERS_objs[0])
								if ACCOUNT_objs:
									ACCOUNT_objs[0].ac_like -= 1
									ACCOUNT_objs[0].save()
								STOCK_objs[0].st_like_count -= 1
								STOCK_objs[0].save()
								response_dict['status'] = 1
							else:
								response_dict['status'] = 2
						else:
							response_dict['status'] = 0
					elif p_type == 'bond':
						BOND_objs = BOND.objects.filter(id__exact = p_id)
						if BOND_objs:
							USER_FOCUS_objs = USER_FOCUS.objects.filter(uf_user = USERS_objs[0],uf_bond = BOND_objs[0])
							if USER_FOCUS_objs:
								USER_FOCUS_objs[0].delete()
								ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__exact = USERS_objs[0])
								if ACCOUNT_objs:
									ACCOUNT_objs[0].ac_like -= 1
									ACCOUNT_objs[0].save()
								BOND_objs[0].bo_like_count -= 1
								BOND_objs[0].save()
								response_dict['status'] = 1
							else:
								response_dict['status'] = 2
						else:
							response_dict['status'] = 0
					else:
						response_dict['status'] = 0
				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#用户认购
def Invest(request):
	response_dict = {}

	if request.method == 'POST':
		token = request.POST.get('token','')
		u_name = request.POST.get('u_name','')
		p_type = request.POST.get('type','')
		p_id = request.POST.get('id','-1')
		price = request.POST.get('price','0')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				if float(price) > 0:
					if p_type == 'stock':
						STOCK_objs = STOCK.objects.filter(id__exact = p_id)
						if STOCK_objs:
							response_dict['status'] = 1
							INVEST_STATUS_obj = INVEST_STATUS.objects.get(id__exact = 1)
							INVEST_STOCK_new = INVEST_STOCK(is_user = USERS_objs[0],is_stock = STOCK_objs[0],is_amount = price,is_date = datetime.now(),is_status = INVEST_STATUS_obj)
							INVEST_STOCK_new.save()
							# try:
							# 	ACCOUNT_obj = ACCOUNT.objects.get(ac_user = USERS_objs[0])
							# 	ACCOUNT_obj.ac_total_subscription = str(float(ACCOUNT_obj.ac_total_subscription)+float(price))
							# 	ACCOUNT_obj.save()
							# except ACCOUNT.DoesNotExist:
							# 	raise Http404
						else:
							response_dict['status'] = 0
					elif p_type == 'bond':
						BOND_objs = BOND.objects.filter(id__exact = p_id)
						if BOND_objs:
							response_dict['status'] = 1
							INVEST_STATUS_obj = INVEST_STATUS.objects.get(id__exact = 1)
							INVEST_BOND_new = INVEST_BOND(ib_user = USERS_objs[0],ib_bond = BOND_objs[0],ib_amount = price,ib_date = datetime.now(),ib_status = INVEST_STATUS_obj)
							INVEST_BOND_new.save()
							# try:
							# 	ACCOUNT_obj = ACCOUNT.objects.get(ac_user = USERS_objs[0])
							# 	ACCOUNT_obj.ac_total_subscription = str(float(ACCOUNT_obj.ac_total_subscription)+float(price))
							# 	ACCOUNT_obj.save()
							# except ACCOUNT.DoesNotExist:
							# 	raise Http500
						else:
							response_dict['status'] = 0
					else:
						response_dict['status'] = 0
				else:
					response_dict['status'] = 2
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#获取用户的投资列表
def InvestList(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')
		p_type = request.GET.get('type','')
		p_id = request.GET.get('id','-1')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				if p_type == 'stock':
					if T.CheckExist(STOCK,{'id':p_id}):
						invest_stock_list = []
						response_dict['status'] = 1
						INVEST_STOCK_objs = INVEST_STOCK.objects.filter(is_stock__exact = p_id)
						for INVEST_STOCK_obj in INVEST_STOCK_objs:
							invest_stock_per = {}
							invest_stock_per['is_user'] = INVEST_STOCK_obj.is_user.u_name
							invest_stock_per['is_date'] = INVEST_STOCK_obj.is_date.strftime('%Y-%m-%d')
							invest_stock_per['is_amount'] = INVEST_STOCK_obj.is_amount
							invest_stock_list.append(invest_stock_per)
						response_dict['invest_stocks'] = invest_stock_list
					else:
						response_dict['status'] = 0
				elif p_type == 'bond':
					if T.CheckExist(BOND,{'id':p_id}):
						invest_bond_list = []
						response_dict['status'] = 1
						INVEST_BOND_objs = INVEST_BOND.objects.filter(ib_bond__exact = p_id)
						for INVEST_BOND_obj in INVEST_BOND_objs:
							invest_bond_per = {}
							invest_bond_per['ib_user'] = INVEST_BOND_obj.ib_user.u_name
							invest_bond_per['ib_date'] = INVEST_BOND_obj.ib_date.strftime('%Y-%m-%d')
							invest_bond_per['ib_amount'] = INVEST_BOND_obj.ib_amount
							invest_bond_list.append(invest_bond_per)
						response_dict['invest_bonds'] = invest_bond_list
					else:
						response_dict['status'] = 0
				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0
	else:
		response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#用户获取通知列表
def GetNotices(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				notices = []
				NOTICE_objs = NOTICE.objects.filter(no_is_delete__exact = 0).order_by('-no_time')
				for NOTICE_obj in NOTICE_objs:
					notice_data = {}
					notice_data['id'] = NOTICE_obj.id
					notice_data['no_title'] = NOTICE_obj.no_title
					notice_data['no_brief'] = NOTICE_obj.no_brief
					notice_data['time'] = NOTICE_obj.no_time.strftime('%Y-%m-%d %H:%M:%S')
					notice_data['no_type'] = NOTICE_obj.no_type
					notice_data['no_sort'] = NOTICE_obj.no_sort
					notice_data['type'] = 'sys'
					if T.CheckExist(NOTICE_READ,{'nr_user':USERS_objs[0],'nr_notice':NOTICE_obj}):
						notice_data['no_is_read'] = 1
					else:
						notice_data['no_is_read'] = 0
					notices.append(notice_data)
				NOTICE_USER_objs = NOTICE_USER.objects.filter(nu_is_delete__exact = 0,nu_user__exact = USERS_objs[0]).order_by('-nu_time')
				for NOTICE_USER_obj in NOTICE_USER_objs:
					notice_data = {}
					notice_data['id'] = NOTICE_USER_obj.id
					notice_data['nu_title'] = NOTICE_USER_obj.nu_title
					notice_data['nu_brief'] = NOTICE_USER_obj.nu_brief
					notice_data['time'] = NOTICE_USER_obj.nu_time.strftime('%Y-%m-%d %H:%M:%S')
					notice_data['nu_type'] = NOTICE_USER_obj.nu_type
					notice_data['nu_is_read'] = NOTICE_USER_obj.nu_is_read
					notice_data['type'] = 'user'
					notices.append(notice_data)
				#按照时间的倒序进行排列
				notices = sorted(notices,key = operator.itemgetter('time'),reverse=True)
				response_dict['notices'] = notices
				response_dict['status'] = 1
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#用户获取通知详情
def NoticeDetail(request):
	response_dict = {}
	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')
		n_type = request.GET.get('type','')
		n_id = request.GET.get('id','-1')
		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				if n_type == 'sys':
					NOTICE_objs = NOTICE.objects.filter(id__exact = n_id)
					if NOTICE_objs:
						response_dict['status'] = 1
						# notice = {}
						# notice['title'] = NOTICE_objs[0].no_title
						# notice['body'] = NOTICE_objs[0].no_body
						# notice['time'] = NOTICE_objs[0].no_time.strftime('%Y-%m-%d %H:%M:%S')
						# response_dict['notice'] = notice
						if not T.CheckExist(NOTICE_READ,{'nr_user':USERS_objs[0],'nr_notice':NOTICE_objs[0]}):
							NOTICE_READ_new = NOTICE_READ(nr_user = USERS_objs[0],nr_notice = NOTICE_objs[0])
							NOTICE_READ_new.save()
					else:
						response_dict['status'] = 0
				elif n_type == 'user':
					NOTICE_USER_objs = NOTICE_USER.objects.filter(id__exact = n_id)
					if NOTICE_USER_objs:
						response_dict['status'] = 1
						# notice = {}
						# notice['title'] = NOTICE_USER_objs[0].nu_title
						# notice['body'] = NOTICE_USER_objs[0].nu_body
						# notice['time'] = NOTICE_USER_objs[0].nu_time.strftime('%Y-%m-%d %H:%M:%S')
						# response_dict['notice'] = notice
						#标记为已经阅读
						NOTICE_USER_objs[0].nu_is_read = 1
						NOTICE_USER_objs[0].save()
					else:
						response_dict['status'] = 0
				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#获取收益列表
def GetProfits(request):
	response_dict = {}

	if request.method == 'GET':
		token = request.GET.get('token','')
		u_name = request.GET.get('u_name','')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				response_dict['status'] = 1
				profits = []
				PROFIT_objs = PROFIT.objects.filter(pr_user__exact = USERS_objs[0]).order_by('-pr_date')
				for PROFIT_obj in PROFIT_objs:
					profits_data = {}
					profits_data['pr_date'] = PROFIT_obj.pr_date.strftime('%Y-%m-%d %H:%M:%S')
					profits_data['pr_amount'] = PROFIT_obj.pr_amount
					if PROFIT_obj.pr_stock:
						profits_data['pr_stock'] = PROFIT_obj.pr_stock.st_title
						profits_data['pr_stock_id'] = PROFIT_obj.pr_stock.id
					elif PROFIT_obj.pr_bond:
						profits_data['pr_bond'] = PROFIT_obj.pr_bond.bo_title
						profits_data['pr_bond_id'] = PROFIT_obj.pr_bond.id
					profits.append(profits_data)
				response_dict['profits'] = profits
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0
	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#检查是否需要更新
def CheckUpdate(request):
	response_dict = {}

	if request.method == 'GET':
		os = request.GET.get('os','')
		version = request.GET.get('version','')

		SETTINGS_objs = SETTINGS.objects.all()
		if SETTINGS_objs:
			if os == 'android' or os == 'Android':
				if version != SETTINGS_objs[0].se_android_version:
					response_dict['status'] = 1
				else:
					response_dict['status'] = 0
			elif os == 'IOS' or os == 'ios':
				if version != SETTINGS_objs[0].se_ios_version:
					response_dict['status'] = 1
				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = 0
		else:
			response_dict['status'] = 0
	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#用户反馈
def Feedback(request):
	response_dict = {}

	if request.method == 'POST':
		token = request.POST.get('token','')
		u_name = request.POST.get('u_name','')
		mail = request.POST.get('mail','')
		content = request.POST.get('content','')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				if content:
					response_dict['status'] = 1
					FEEDBACK_new = FEEDBACK(fe_user = USERS_objs[0],fe_mail = mail,fe_time = datetime.now(),fe_content = content)
					FEEDBACK_new.save()
				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0
	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")