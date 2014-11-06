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
				if T.SendRandomCode(u_tel):
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

