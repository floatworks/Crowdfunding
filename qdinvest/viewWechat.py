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
	if p_type == 's':
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
	elif p_type == 'b':
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
		if USERS_objs:
			request.session['HAS_LOGIN'] = True
			request.session['USER_ID'] = USERS_objs[0].id
			request.session['USER_NAME'] = USERS_objs[0].u_name
			origin_path = request.session.get('origin_path','/w')
			if origin_path == '/w/login/' or origin_path == '/w/login':
				origin_path = '/w'
			return HttpResponseRedirect(origin_path)
		else:
			return render_to_response('wechat/login.html',context_dict,context)

#微信端个人中心
def Personal(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('wechat/personal.html',context_dict,context)

#微信端关于页面
def Setting(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('wechat/setting.html',context_dict,context)
