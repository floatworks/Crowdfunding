#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.conf import settings
import operator
import traceback
from datetime import datetime

from models import *
import tools as T

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
				return HttpResponseRedirect('/w/login/')
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

def Index(request):
	context = RequestContext(request)
	context_dict = {}
	projects = []
	projects_commend = []

	STOCK_objs = STOCK.objects.order_by('-st_create_time')[:5]
	BOND_objs = BOND.objects.order_by('-bo_create_time')[:5]
	
	for STOCK_obj in STOCK_objs:
		stock_data = {}
		stock_data['type'] = 'stock'
		stock_data['id'] = STOCK_obj.id
		stock_data['title'] = STOCK_obj.st_title
		stock_data['image'] = str(STOCK_obj.st_image)
		stock_data['pro_type'] = STOCK_obj.st_pro_type.pt_name
		stock_data['province'] = STOCK_obj.st_province.pr_name
		stock_data['industry'] = STOCK_obj.st_industry.in_name
		stock_data['com_type'] = STOCK_obj.st_com_type.ct_name
		stock_data['view_count'] = STOCK_obj.st_view_count
		stock_data['like_count'] = STOCK_obj.st_like_count
		stock_data['invest_count'] = STOCK_obj.st_invest_count
		stock_data['current_price'] = STOCK_obj.st_current_price
		stock_data['total_price'] = STOCK_obj.st_total_price
		stock_data['min_price'] = STOCK_obj.st_min_price
		stock_data['create_time'] = STOCK_obj.st_create_time.strftime('%Y-%m-%d %H:%M:%S')
		stock_data['progress'] = T.Scale(STOCK_obj.st_current_price,STOCK_obj.st_total_price)
		projects.append(stock_data)
		if STOCK_obj.st_is_commend == 1:
			projects_commend.append(stock_data)
	for BOND_obj in BOND_objs:
		bond_data = {}
		bond_data['type'] = 'bond'
		bond_data['id'] = BOND_obj.id
		bond_data['title'] = BOND_obj.bo_title
		bond_data['image'] = str(BOND_obj.bo_image)
		bond_data['com_name'] = BOND_obj.bo_com_name
		bond_data['pro_type'] = BOND_obj.bo_pro_type.pt_name
		bond_data['brief'] = BOND_obj.bo_brief
		bond_data['scale'] = BOND_obj.bo_scale
		bond_data['total_price'] = BOND_obj.bo_total_price
		bond_data['current_price'] = BOND_obj.bo_current_price
		bond_data['min_price'] = BOND_obj.bo_min_price
		bond_data['create_time'] = BOND_obj.bo_create_time.strftime('%Y-%m-%d %H:%M:%S')
		bond_data['progress'] = T.Scale(BOND_obj.bo_current_price,BOND_obj.bo_total_price)
		projects.append(bond_data)
		if BOND_obj.bo_is_commend == 1:
			projects_commend.append(bond_data)

	STOCK_com_objs = STOCK.objects.filter(st_is_commend = 1).order_by('-st_create_time')
	BOND_com_objs = BOND.objects.filter(bo_is_commend = 1).order_by('-bo_create_time')
	for STOCK_obj in STOCK_com_objs:
		stock_data = {}
		stock_data['type'] = 'stock'
		stock_data['id'] = STOCK_obj.id
		stock_data['title'] = STOCK_obj.st_title
		stock_data['image'] = str(STOCK_obj.st_image)
		stock_data['pro_type'] = STOCK_obj.st_pro_type.pt_name
		stock_data['province'] = STOCK_obj.st_province.pr_name
		stock_data['industry'] = STOCK_obj.st_industry.in_name
		stock_data['com_type'] = STOCK_obj.st_com_type.ct_name
		stock_data['view_count'] = STOCK_obj.st_view_count
		stock_data['like_count'] = STOCK_obj.st_like_count
		stock_data['invest_count'] = STOCK_obj.st_invest_count
		stock_data['current_price'] = STOCK_obj.st_current_price
		stock_data['total_price'] = STOCK_obj.st_total_price
		stock_data['min_price'] = STOCK_obj.st_min_price
		stock_data['create_time'] = STOCK_obj.st_create_time.strftime('%Y-%m-%d %H:%M:%S')
		stock_data['progress'] = T.Scale(STOCK_obj.st_current_price,STOCK_obj.st_total_price)
		projects_commend.append(stock_data)
	for BOND_obj in BOND_com_objs:
		bond_data = {}
		bond_data['type'] = 'bond'
		bond_data['id'] = BOND_obj.id
		bond_data['title'] = BOND_obj.bo_title
		bond_data['image'] = str(BOND_obj.bo_image)
		bond_data['com_name'] = BOND_obj.bo_com_name
		bond_data['pro_type'] = BOND_obj.bo_pro_type.pt_name
		bond_data['brief'] = BOND_obj.bo_brief
		bond_data['scale'] = BOND_obj.bo_scale
		bond_data['total_price'] = BOND_obj.bo_total_price
		bond_data['current_price'] = BOND_obj.bo_current_price
		bond_data['min_price'] = BOND_obj.bo_min_price
		bond_data['create_time'] = BOND_obj.bo_create_time.strftime('%Y-%m-%d %H:%M:%S')
		bond_data['progress'] = T.Scale(BOND_obj.bo_current_price,BOND_obj.bo_total_price)
		projects_commend.append(bond_data)

	projects = sorted(projects,key = operator.itemgetter('create_time'),reverse=True)
	projects_commend = sorted(projects_commend,key = operator.itemgetter('create_time'),reverse=True)
	context_dict['projects'] = projects
	context_dict['projects_commend'] = projects_commend
	#if settings.DEBUG:
	#	print context_dict
	return render_to_response('wechat/index.html',context_dict,context)

#微信端ajax加载更多数据
def GetProList(request,count):
	context = RequestContext(request)
	response_dict = {}
	projects = []

	count = int(count)

	STOCK_objs = STOCK.objects.order_by('-st_create_time')[count*5:count*5+5]
	BOND_objs = BOND.objects.order_by('-bo_create_time')[count*5:count*5+5]

	for STOCK_obj in STOCK_objs:
		stock_data = {}
		stock_data['type'] = 'stock'
		stock_data['id'] = STOCK_obj.id
		stock_data['title'] = STOCK_obj.st_title
		stock_data['image'] = str(STOCK_obj.st_image)
		stock_data['pro_type'] = STOCK_obj.st_pro_type.pt_name
		stock_data['province'] = STOCK_obj.st_province.pr_name
		stock_data['industry'] = STOCK_obj.st_industry.in_name
		stock_data['com_type'] = STOCK_obj.st_com_type.ct_name
		stock_data['view_count'] = STOCK_obj.st_view_count
		stock_data['like_count'] = STOCK_obj.st_like_count
		stock_data['invest_count'] = STOCK_obj.st_invest_count
		stock_data['current_price'] = STOCK_obj.st_current_price
		stock_data['total_price'] = STOCK_obj.st_total_price
		stock_data['min_price'] = STOCK_obj.st_min_price
		stock_data['create_time'] = STOCK_obj.st_create_time.strftime('%Y-%m-%d %H:%M:%S')
		stock_data['progress'] = T.Scale(STOCK_obj.st_current_price,STOCK_obj.st_total_price)
		projects.append(stock_data)
		#if STOCK_obj.st_is_commend == 1:
		#	projects_commend.append(stock_data)
	for BOND_obj in BOND_objs:
		bond_data = {}
		bond_data['type'] = 'bond'
		bond_data['id'] = BOND_obj.id
		bond_data['title'] = BOND_obj.bo_title
		bond_data['image'] = str(BOND_obj.bo_image)
		bond_data['com_name'] = BOND_obj.bo_com_name
		bond_data['pro_type'] = BOND_obj.bo_pro_type.pt_name
		bond_data['brief'] = BOND_obj.bo_brief
		bond_data['scale'] = BOND_obj.bo_scale
		bond_data['total_price'] = BOND_obj.bo_total_price
		bond_data['current_price'] = BOND_obj.bo_current_price
		bond_data['min_price'] = BOND_obj.bo_min_price
		bond_data['create_time'] = BOND_obj.bo_create_time.strftime('%Y-%m-%d %H:%M:%S')
		bond_data['progress'] = T.Scale(BOND_obj.bo_current_price,BOND_obj.bo_total_price)
		projects.append(bond_data)
		#if BOND_obj.bo_is_commend == 1:
		#	projects_commend.append(bond_data)

	projects = sorted(projects,key = operator.itemgetter('create_time'),reverse=True)

	if STOCK_objs or BOND_objs:
		response_dict['projects'] = projects
		response_dict['status'] = 1
	else:
		response_dict['status'] = 0
	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

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

#手机短获取通知详细信息
def NoticeDetail(request,n_type,n_id):
	context = RequestContext(request)
	context_dict = {}
	if n_type == 'sys':
		try:
			NOTICE_obj = NOTICE.objects.get(id__exact = n_id)
			context_dict['notice'] = NOTICE_obj
			return render_to_response('wechat/pro-details.html',context_dict,context)
		except NOTICE.DoesNotExist:
			raise Http404
	elif n_type == 'user':
		try:
			NOTICE_USER_obj = NOTICE_USER.objects.get(id__exact = n_id)
			context_dict['notice'] = NOTICE_USER_obj
			return render_to_response('wechat/pro-details.html',context_dict,context)
		except NOTICE_USER.DoesNotExist:
			raise Http404
	else:
		raise Http404

#手机短获取投后管理界面
def ProManage(request,p_type,p_id):
	context = RequestContext(request)
	context_dict = {}
	if p_type == 's':
		try:
			STOCK_obj = STOCK.objects.get(id__exact = p_id)
			context_dict['promanage'] = STOCK_obj.st_manage
			return render_to_response('wechat/pro-details.html',context_dict,context)
		except STOCK.DoesNotExist:
			raise Http404
	elif p_type == 'b':
		try:
			BOND_obj = BOND.objects.get(id__exact = p_id)
			context_dict['promanage'] = BOND_obj.bo_manage
			return render_to_response('wechat/pro-details.html',context_dict,context)
		except BOND.DoesNotExist:
			raise Http404
	else:
		raise Http404


#微信端获取项目详细页面
def ProjectDetail(request,p_type,p_id):
	context = RequestContext(request)
	context_dict = {}
	print p_type,p_id
	if p_type == 's' or p_type == 'stock':
		try:
			STOCK_obj = STOCK.objects.get(id__exact = p_id)
			context_dict['p_type'] = 'stock'
			context_dict['id'] = STOCK_obj.id
			context_dict['title'] = STOCK_obj.st_title
			context_dict['image'] = STOCK_obj.st_image
			#获取用户是否已经关注
			if request.session.get('HAS_LOGIN',False):
				USERS_obj = USERS.objects.get(id__exact = request.session['USER_ID'])
				if T.CheckExist(USER_FOCUS,{'uf_user':USERS_obj,'uf_stock':STOCK_obj}):
					context_dict['if_like'] = 1
				else:
					context_dict['if_like'] = 0
			else:
				context_dict['if_like'] = 0
			context_dict['view_count'] = STOCK_obj.st_view_count
			context_dict['like_count'] = STOCK_obj.st_like_count
			context_dict['invest_count'] = STOCK_obj.st_invest_count
			context_dict['progress'] = T.Scale(STOCK_obj.st_current_price,STOCK_obj.st_total_price)
			context_dict['province'] = STOCK_obj.st_province.pr_name
			context_dict['st_industry'] = STOCK_obj.st_industry.in_name
			context_dict['st_com_type'] = STOCK_obj.st_com_type.ct_name
			context_dict['st_pro_type'] = STOCK_obj.st_pro_type.pt_name
			context_dict['end_time'] = STOCK_obj.st_end_time
			context_dict['current_price'] = STOCK_obj.st_current_price
			context_dict['total_price'] = STOCK_obj.st_total_price
			context_dict['min_price'] = STOCK_obj.st_min_price
			invests = []
			INVEST_STOCK_objs = INVEST_STOCK.objects.filter(is_stock = STOCK_obj)
			for INVEST_STOCK_obj in INVEST_STOCK_objs:
				invests.append({'date':INVEST_STOCK_obj.is_date,'user':INVEST_STOCK_obj.is_user.u_name,'price':INVEST_STOCK_obj.is_amount})
			context_dict['invests'] = invests
			context_dict['stock'] = STOCK_obj
			context_dict['promanage'] = STOCK_obj.st_manage

			return render_to_response('wechat/proDetail.html',context_dict,context)
		except STOCK.DoesNotExist:
			raise Http404
	elif p_type == 'b' or p_type == 'bond':
		try:
			BOND_obj = BOND.objects.get(id__exact = p_id)
			context_dict['p_type'] = 'bond'
			context_dict['id'] = BOND_obj.id
			context_dict['title'] = BOND_obj.bo_title
			context_dict['image'] = BOND_obj.bo_image
			#获取用户是否已经关注
			if request.session.get('HAS_LOGIN',False):
				USERS_obj = USERS.objects.get(id__exact = request.session['USER_ID'])
				if T.CheckExist(USER_FOCUS,{'uf_user':USERS_obj,'uf_bond':BOND_obj}):
					context_dict['if_like'] = 1
				else:
					context_dict['if_like'] = 0
			else:
				context_dict['if_like'] = 0
			context_dict['view_count'] = BOND_obj.bo_view_count
			context_dict['like_count'] = BOND_obj.bo_like_count
			context_dict['invest_count'] = BOND_obj.bo_invest_count
			context_dict['progress'] = T.Scale(BOND_obj.bo_current_price,BOND_obj.bo_total_price)
			context_dict['province'] = BOND_obj.bo_province.pr_name
			context_dict['st_industry'] = BOND_obj.bo_industry.in_name
			context_dict['st_com_type'] = BOND_obj.bo_com_type.ct_name
			context_dict['st_pro_type'] = BOND_obj.bo_pro_type.pt_name
			context_dict['end_time'] = BOND_obj.bo_end_time
			context_dict['current_price'] = BOND_obj.bo_current_price
			context_dict['total_price'] = BOND_obj.bo_total_price
			context_dict['min_price'] = BOND_obj.bo_min_price
			context_dict['scale'] = BOND_obj.bo_scale
			invests = []
			INVEST_BOND_objs = INVEST_BOND.objects.filter(ib_bond = BOND_obj)
			for INVEST_BOND_obj in INVEST_BOND_objs:
				invests.append({'date':INVEST_BOND_obj.ib_date,'user':INVEST_BOND_obj.ib_user.u_name,'price':INVEST_BOND_obj.ib_amount})
			context_dict['invests'] = invests
			context_dict['bond'] = BOND_obj
			context_dict['promanage'] = BOND_obj.bo_manage

			return render_to_response('wechat/proDetail.html',context_dict,context)
		except BOND.DoesNotExist:
			raise Http404
	else:
		raise Http404

#微信端用户喜欢界面
def ProLike(request):
	response_dict = {}
	if not T.CheckIsLogin(request):
		response_dict['status'] = -1
	else:
		if request.method == 'POST':
			p_type = request.POST.get('type','')
			p_id = request.POST.get('id','-1')
			focus = request.POST.get('focus','')
			p_id = int(p_id)
			print p_type,p_id,focus

			USERS_obj = USERS.objects.get(id__exact = request.session['USER_ID'])
			if focus == 'like':
				if p_type == 'stock':
					STOCK_objs = STOCK.objects.filter(id__exact = p_id)
					if STOCK_objs:
						if T.CheckExist(USER_FOCUS,{'uf_user':USERS_obj,'uf_stock':STOCK_objs[0]}):
							response_dict['status'] = 2
						else:
							USER_FOCUS_new = USER_FOCUS(uf_user = USERS_obj,uf_stock = STOCK_objs[0],uf_update_time = datetime.now())
							USER_FOCUS_new.save()
							ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__exact = USERS_obj)
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
						if T.CheckExist(USER_FOCUS,{'uf_user':USERS_obj,'uf_bond':BOND_objs[0]}):
							response_dict['status'] = 2
						else:
							USER_FOCUS_new = USER_FOCUS(uf_user = USERS_obj,uf_bond = BOND_objs[0],uf_update_time = datetime.now())
							USER_FOCUS_new.save()
							ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__exact = USERS_obj)
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
						USER_FOCUS_objs = USER_FOCUS.objects.filter(uf_user = USERS_obj,uf_stock = STOCK_objs[0])
						if USER_FOCUS_objs:
							USER_FOCUS_objs[0].delete()
							ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__exact = USERS_obj)
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
						USER_FOCUS_objs = USER_FOCUS.objects.filter(uf_user = USERS_obj,uf_bond = BOND_objs[0])
						if USER_FOCUS_objs:
							USER_FOCUS_objs[0].delete()
							ACCOUNT_objs = ACCOUNT.objects.filter(ac_user__exact = USERS_obj)
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
	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")
	

#微信端登录
def Login(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method == 'POST':
		username = request.POST.get('user','')
		password = request.POST.get('pwd','')

		USERS_objs = USERS.objects.filter(u_name = username,u_pwd = password)
		print USERS_objs
		if USERS_objs:
			request.session['HAS_LOGIN'] = True
			request.session['USER_ID'] = USERS_objs[0].id
			request.session['USER_NAME'] = USERS_objs[0].u_name
			origin_path = request.session.get('origin_path','/w')
			print origin_path
			if origin_path.endswith('/w/login/') or origin_path.endswith('/w/login') or not origin_path:
				origin_path = '/w'
			return HttpResponseRedirect(origin_path)
		else:
			return render_to_response('wechat/login.html',context_dict,context)
	else:
		return render_to_response('wechat/login.html',context_dict,context)

#微信端个人中心
def Personal(request):
	context = RequestContext(request)
	context_dict = {}

	if not T.CheckIsLogin(request):
		return	HttpResponseRedirect('/w/login/')
	else:
		#USERS_obj = USERS.objects.get(id__exact = request.session['USER_ID'])
		ACCOUNT_obj = ACCOUNT.objects.get(ac_user__id = request.session['USER_ID'])
		context_dict['account'] = ACCOUNT_obj

		PROFIT_objs = PROFIT.objects.filter(pr_user__id = request.session['USER_ID']).order_by('-pr_date')
		profits = []
		for PROFIT_obj in PROFIT_objs:
			profits_data = {}
			profits_data['date'] = PROFIT_obj.pr_date.strftime('%Y-%m-%d')
			profits_data['amount'] = PROFIT_obj.pr_amount
			if PROFIT_obj.pr_stock:
				profits_data['title'] = PROFIT_obj.pr_stock.st_title
				profits_data['id'] = PROFIT_obj.pr_stock.id
				profits_data['type'] = 'stock'
			elif PROFIT_obj.pr_bond:
				profits_data['title'] = PROFIT_obj.pr_bond.bo_title
				profits_data['id'] = PROFIT_obj.pr_bond.id
				profits_data['type'] = 'bond'
			profits.append(profits_data)
		context_dict['profits'] = profits

	return render_to_response('wechat/personal.html',context_dict,context)

#微信端设置页面
def Setting(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('wechat/setting.html',context_dict,context)

#微信端我的项目页面
def GetMyProList(request):
	context = RequestContext(request)
	context_dict = {}
	if not T.CheckIsLogin(request):
		return	HttpResponseRedirect('/w/login/')
	else:
		USERS_obj = USERS.objects.get(id__exact = request.session['USER_ID'])
		projects_s1 = []
		projects_s2 = []
		projects_s3 = []

		STOCK_ids = INVEST_STOCK.objects.filter(is_user__exact = USERS_obj).values('is_stock').distinct()
		for STOCK_id in STOCK_ids:
			STOCK_obj = STOCK.objects.get(id__exact = STOCK_id['is_stock'])
			stocks_per = {}
			stocks_per['id'] = STOCK_obj.id
			stocks_per['type'] = 'stock'
			stocks_per['title'] = STOCK_obj.st_title
			stocks_per['image'] = str(STOCK_obj.st_image)
			stocks_per['total_price'] = STOCK_obj.st_total_price
			stocks_per['brief'] = STOCK_obj.st_brief 
			#stocks_per['is_amount'] = INVEST_STOCK_obj.is_amount
			INVEST_STOCK_objs = INVEST_STOCK.objects.filter(is_user__exact = USERS_obj,is_stock__exact = STOCK_obj,is_status__id = 1).order_by('-is_date')
			if INVEST_STOCK_objs:
				stocks_per['date'] = INVEST_STOCK_objs[0].is_date.strftime('%Y-%m-%d %H:%M:%S')
				projects_s1.append(stocks_per)
			INVEST_STOCK_objs = INVEST_STOCK.objects.filter(is_user__exact = USERS_obj,is_stock__exact = STOCK_obj,is_status__id = 2).order_by('-is_date')
			if INVEST_STOCK_objs:
				stocks_per['date'] = INVEST_STOCK_objs[0].is_date.strftime('%Y-%m-%d %H:%M:%S')
				projects_s2.append(stocks_per)
			INVEST_STOCK_objs = INVEST_STOCK.objects.filter(is_user__exact = USERS_obj,is_stock__exact = STOCK_obj,is_status__id = 3).order_by('-is_date')
			if INVEST_STOCK_objs:
				stocks_per['date'] = INVEST_STOCK_objs[0].is_date.strftime('%Y-%m-%d %H:%M:%S')
				projects_s3.append(stocks_per)
		BOND_ids = INVEST_BOND.objects.filter(ib_user__exact = USERS_obj).values('ib_bond').distinct()
		for BOND_id in BOND_ids:
			BOND_obj = BOND.objects.get(id__exact = BOND_id['ib_bond'])
			bonds_per = {}
			bonds_per['id'] = BOND_obj.id
			bonds_per['type'] = 'bond'
			bonds_per['title'] = BOND_obj.bo_title
			bonds_per['image'] = str(BOND_obj.bo_image)
			bonds_per['total_price'] = BOND_obj.bo_total_price
			bonds_per['brief'] = BOND_obj.bo_brief
			INVEST_BOND_objs = INVEST_BOND.objects.filter(ib_user__exact = USERS_obj,ib_bond__exact = BOND_obj,ib_status__id = 1).order_by('-ib_date')
			if INVEST_BOND_objs:
				bonds_per['date'] = INVEST_BOND_objs[0].ib_date.strftime('%Y-%m-%d %H:%M:%S')
				projects_s1.append(bonds_per)
			INVEST_BOND_objs = INVEST_BOND.objects.filter(ib_user__exact = USERS_obj,ib_bond__exact = BOND_obj,ib_status__id = 2).order_by('-ib_date')
			if INVEST_BOND_objs:
				bonds_per['date'] = INVEST_BOND_objs[0].ib_date.strftime('%Y-%m-%d %H:%M:%S')
				projects_s2.append(bonds_per)
			INVEST_BOND_objs = INVEST_BOND.objects.filter(ib_user__exact = USERS_obj,ib_bond__exact = BOND_obj,ib_status__id = 3).order_by('-ib_date')
			if INVEST_BOND_objs:
				bonds_per['date'] = INVEST_BOND_objs[0].ib_date.strftime('%Y-%m-%d %H:%M:%S')
				projects_s3.append(bonds_per)
		projects_s1 = sorted(projects_s1,key = operator.itemgetter('date'),reverse=True)
		projects_s2 = sorted(projects_s2,key = operator.itemgetter('date'),reverse=True)
		projects_s3 = sorted(projects_s3,key = operator.itemgetter('date'),reverse=True)
		context_dict['projects_s1'] = projects_s1
		context_dict['projects_s2'] = projects_s2
		context_dict['projects_s3'] = projects_s3
	#if settings.DEBUG:
	#	print context_dict
	return render_to_response('wechat/myproject.html',context_dict,context)

#获取我的项目的认购信息
def GetMyProInvest(request,p_type,p_id):
	context = RequestContext(request)
	response_dict = {}
	if not T.CheckIsLogin(request):
		return	HttpResponseRedirect('/w/login/')
	else:
		USERS_obj = USERS.objects.get(id__exact = request.session['USER_ID'])
		if p_type == 'stock':
			if T.CheckExist(STOCK,{'id':p_id}):
				STOCK_obj = STOCK.objects.get(id__exact = p_id)
				project = {}
				project['id'] = STOCK_obj.id
				project['type'] = 'stock'
				project['title'] = STOCK_obj.st_title
				project['image'] = str(STOCK_obj.st_image)
				project['brief'] = STOCK_obj.st_brief
				project['total_price'] = STOCK_obj.st_total_price
				project['current_price'] = STOCK_obj.st_current_price
				invests = []
				st_invest_price = 0
				INVEST_STOCK_objs = INVEST_STOCK.objects.filter(is_user = USERS_obj,is_stock = STOCK_obj)
				for INVEST_STOCK_obj in INVEST_STOCK_objs:
					invests.append({'amount':INVEST_STOCK_obj.is_amount,'date':INVEST_STOCK_obj.is_date.strftime('%Y-%m-%d'),'status':INVEST_STOCK_obj.is_status.id})
					st_invest_price += INVEST_STOCK_obj.is_amount
				#判断是否已经交定金
				if T.CheckExist(PAYMENT,{'pa_user':USERS_obj,'pa_stock':STOCK_obj,'pa_status':0}):
					project['is_payment'] = 1
				else:
					project['is_payment'] = 0
				project['invest_price'] = st_invest_price
				response_dict['project'] = project
				response_dict['invests'] = invests
			else:
				response_dict['status'] = 0
		elif p_type == 'bond':
			if T.CheckExist(BOND,{'id':p_id}):
				BOND_obj = BOND.objects.get(id__exact = p_id)
				project = {}
				project['id'] = BOND_obj.id
				project['type'] = 'bond'
				project['title'] = BOND_obj.bo_title
				project['image'] = str(BOND_obj.bo_image)
				project['brief'] = BOND_obj.bo_brief
				project['total_price'] = BOND_obj.bo_total_price
				project['current_price'] = BOND_obj.bo_current_price
				invests = []
				bo_invest_price = 0
				INVEST_BOND_objs = INVEST_BOND.objects.filter(ib_user = USERS_obj,ib_bond = BOND_obj)
				for INVEST_BOND_obj in INVEST_BOND_objs:
					invests.append({'amount':INVEST_BOND_obj.ib_amount,'date':INVEST_BOND_obj.ib_date.strftime('%Y-%m-%d'),'status':INVEST_BOND_obj.ib_status.id})
					bo_invest_price += INVEST_BOND_obj.ib_amount
				#判断是否已经交定金
				if T.CheckExist(PAYMENT,{'pa_user':USERS_obj,'pa_bond':BOND_obj,'pa_status':0}):
					project['is_payment'] = 1
				else:
					project['is_payment'] = 0
				project['invest_price'] = bo_invest_price
				response_dict['project'] = project
				response_dict['invests'] = invests

	if settings.DEBUG:
		print response_dict
	return render_to_response('wechat/myproinvest.html',response_dict,context)


#用户认购
def Invest(request):
	response_dict = {}

	if not T.CheckIsLogin(request):
		response_dict['status'] = -1
	else:
		if request.method == 'POST':
			p_type = request.POST.get('type','')
			p_id = request.POST.get('id','-1')
			price = request.POST.get('price','0')

			USERS_obj = USERS.objects.get(id__exact = request.session['USER_ID'])
			if float(price) > 0:
				if p_type == 'stock':
					STOCK_objs = STOCK.objects.filter(id__exact = p_id)
					if STOCK_objs:
						if not T.CheckExist(INVEST_STOCK,{'is_user':USERS_obj,'is_stock':STOCK_objs[0]}):
							ACCOUNT_obj = ACCOUNT.objects.get(ac_user = USERS_obj)
							ACCOUNT_obj.ac_support += 1
							ACCOUNT_obj.save()
						response_dict['status'] = 1
						INVEST_STATUS_obj = INVEST_STATUS.objects.get(id__exact = 1)
						INVEST_STOCK_new = INVEST_STOCK(is_user = USERS_obj,is_stock = STOCK_objs[0],is_amount = str(price),is_date = datetime.now(),is_status = INVEST_STATUS_obj)
						INVEST_STOCK_new.save()

						STOCK_objs[0].st_invest_count += 1
						STOCK_objs[0].save()
					else:
						response_dict['status'] = 0
				elif p_type == 'bond':
					BOND_objs = BOND.objects.filter(id__exact = p_id)
					if BOND_objs:
						if not T.CheckExist(INVEST_BOND,{'ib_user':USERS_obj,'ib_bond':BOND_objs[0]}):
							ACCOUNT_obj = ACCOUNT.objects.get(ac_user = USERS_obj)
							ACCOUNT_obj.ac_support += 1
							ACCOUNT_obj.save()
						response_dict['status'] = 1
						INVEST_STATUS_obj = INVEST_STATUS.objects.get(id__exact = 1)
						INVEST_BOND_new = INVEST_BOND(ib_user = USERS_obj,ib_bond = BOND_objs[0],ib_amount = str(price),ib_date = datetime.now(),ib_status = INVEST_STATUS_obj)
						INVEST_BOND_new.save()

						BOND_objs[0].bo_invest_count += 1
						BOND_objs[0].save()
					else:
						response_dict['status'] = 0
				else:
					response_dict['status'] = 0
			else:
				response_dict['status'] = 2

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")

#用户反馈
def Feedback(request):
	response_dict = {}

	if not T.CheckIsLogin(request):
		response_dict['status'] = -1
	else:
		if request.method == 'POST':
			mail = request.POST.get('mail','')
			content = request.POST.get('content','')

			USERS_obj = USERS.objects.get(id__exact = request.session['USER_ID'])
			if content:
				response_dict['status'] = 1
				FEEDBACK_new = FEEDBACK(fe_user = USERS_obj,fe_mail = mail,fe_time = datetime.now(),fe_content = content)
				FEEDBACK_new.save()
			else:
				response_dict['status'] = 0

	if settings.DEBUG:
		print response_dict
	return HttpResponse(json.dumps(response_dict),content_type="application/json")


#微信端弹出页面
def Pop(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('wechat/popup.html',context_dict,context)
