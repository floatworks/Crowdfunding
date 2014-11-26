#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.conf import settings
import operator

from models import *

def Index(request):
	context = RequestContext(request)
	context_dict = {}
	projects = []
	projects_commend = []

	STOCK_objs = STOCK.objects.order_by('-st_create_time')
	BOND_objs = BOND.objects.order_by('-bo_create_time')
	
	for STOCK_obj in STOCK_objs:
		stock_data = {}
		stock_data['type'] = 'stock'
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
		projects.append(bond_data)
		if BOND_obj.bo_is_commend == 1:
			projects_commend.append(bond_data)

	projects = sorted(projects,key = operator.itemgetter('create_time'),reverse=True)
	projects_commend = sorted(projects_commend,key = operator.itemgetter('create_time'),reverse=True)
	context_dict['projects'] = projects
	context_dict['projects_commend'] = projects_commend
	if settings.DEBUG:
		print context_dict
	return render_to_response('wechat/index.html',context_dict,context)

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
def Projectdetail(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('wechat/proDetail.html',context_dict,context)
