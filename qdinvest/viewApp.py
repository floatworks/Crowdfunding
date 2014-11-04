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
		#elif not CheckRandomCode(u_tel,code):
		#	response_dict['status'] = 4
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
		if T.CheckExist(USERS,{'u_tel':u_tel}):
			response_dict['status'] = 2
		elif u_tel:
			url = 'http://www.duanxin10086.com/sms.aspx'
			code = T.RandCode()
			content = '【清大众筹】您的验证码为'+code+'。工作人员不会向您索要，请勿向任何人泄漏。'
			payload = {'userid':'7685','account':'tb2014','password':'123456','mobile':u_tel,
						'content':content,'sendTime':'','action':'send','checkcontent':0,
						'taskName':'','countnumber':1,'mobilenumber':1,'telephonenumber':0}
			r = requests.post(url,data=payload)
			xml = ElementTree.fromstring(r.content)
			returnstatus = xml.find("returnstatus").text
			#验证码获取成功
			if returnstatus == 'Success':
				response_dict['status'] = 1
				if T.CheckExist(RANDOMCODE,{'rc_tel':u_tel}):
					randomCode_obj = RANDOMCODE.objects.get(rc_tel__exact = u_tel)
					randomCode_obj.rc_code = code
					randomCode_obj.rc_time = datetime.now()
					randomCode_obj.save()
				else:
					randomCode_obj = RANDOMCODE(rc_tel = u_tel,rc_code = code,rc_time = datetime.now())
					randomCode_obj.save()
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
