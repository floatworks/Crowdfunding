#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q
from django.conf import settings

from models import *
from forms import *
import tools as T

import requests
import simplejson as json
from datetime import datetime,timedelta
from xml.etree import ElementTree

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
				response_dict['status'] = 1
			else:
				response_dict['status'] = 0
				if settings.DEBUG:
					response_dict['error'] = userForm.errors
					print userForm.errors
	
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
					stocks_data.append(stocks_per)
				response_dict['stocks'] = stocks_data
				bonds_data = []
				BOND_objs = BOND.objects.order_by('-bo_create_time')[num*20:(num+1)*20]
				for BOND_obj in BOND_objs:
					bonds_per = {}
					bonds_per['bo_title'] = BOND_obj.bo_title
					bonds_per['bo_image'] = str(BOND_obj.bo_image)
					bonds_per['bo_com_name'] = BOND_obj.bo_com_name
					bonds_per['bo_pro_type'] = BOND_obj.bo_pro_type.pt_name
					bonds_per['bo_brief'] = BOND_obj.bo_brief
					bonds_per['bo_scale'] = BOND_obj.bo_scale
					bonds_per['bo_total_price'] = BOND_obj.bo_total_price
					bonds_per['bo_current_price'] = BOND_obj.bo_current_price
					bonds_per['bo_min_price'] = BOND_obj.bo_min_price
					bonds_data.append(bonds_per)
				response_dict['bonds'] = bonds_data
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
					stocks_data.append(stocks_per)
				response_dict['stocks'] = stocks_data
				bonds_data = []
				BOND_objs = BOND.objects.order_by('bo_sort')[num*20:(num+1)*20]
				for BOND_obj in BOND_objs:
					bonds_per = {}
					bonds_per['bo_title'] = BOND_obj.bo_title
					bonds_per['bo_image'] = str(BOND_obj.bo_image)
					bonds_per['bo_com_name'] = BOND_obj.bo_com_name
					bonds_per['bo_pro_type'] = BOND_obj.bo_pro_type.pt_name
					bonds_per['bo_brief'] = BOND_obj.bo_brief
					bonds_per['bo_scale'] = BOND_obj.bo_scale
					bonds_per['bo_total_price'] = BOND_obj.bo_total_price
					bonds_per['bo_current_price'] = BOND_obj.bo_current_price
					bonds_per['bo_min_price'] = BOND_obj.bo_min_price
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
					stocks_data.append(stocks_per)
				response_dict['stocks'] = stocks_data
				bonds_data = []
				BOND_objs = BOND.objects.filter(bo_title__contains = keyword).order_by('bo_sort')[num*20:(num+1)*20]
				for BOND_obj in BOND_objs:
					bonds_per = {}
					bonds_per['bo_title'] = BOND_obj.bo_title
					bonds_per['bo_image'] = str(BOND_obj.bo_image)
					bonds_per['bo_com_name'] = BOND_obj.bo_com_name
					bonds_per['bo_pro_type'] = BOND_obj.bo_pro_type.pt_name
					bonds_per['bo_brief'] = BOND_obj.bo_brief
					bonds_per['bo_scale'] = BOND_obj.bo_scale
					bonds_per['bo_total_price'] = BOND_obj.bo_total_price
					bonds_per['bo_current_price'] = BOND_obj.bo_current_price
					bonds_per['bo_min_price'] = BOND_obj.bo_min_price
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
		p_id = request.GET.get('id','')

		USERS_objs = USERS.objects.filter(u_name__exact = u_name)
		if USERS_objs:
			if T.CheckToken(USERS_objs[0],token,0):
				if p_type == 'stock':

				elif p_type == 'bond':

				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = -1
		else:
			response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")



