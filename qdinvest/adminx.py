#coding:utf-8
import xadmin
from xadmin import views
from models import *
'''
基础用户表
'''
class USERSAdmin(object):
	list_display = ['u_name','u_pwd','u_tel','u_status']
	list_filter=['u_status']	
	search_fiedls = ['u_name']
    
'''
用户账户信息
'''

class ACCOUNTAdmin(object):
	list_display = ['ac_user','ac_like','ac_support','ac_sponsor','ac_infos',
	'ac_balance','ac_frozen','ac_soon_profit','ac_actual_profit','ac_total_invest',
	'ac_total_profit']
	search_fiedls = ['ac_user']

'''
行业
'''

class INDUSTRYAdmin(object):
	list_display = ['in_name','in_sort']
	search_fiedls = ['in_name'] 

'''
地区 城市 基础信息
'''

class PROVINCEAdmin(object):
	list_display = ['pr_name']
	search_fiedls = ['pr_name'] 

'''
公司类型 
'''
class PRO_TYPEAdmin(object):
	list_display = ['pt_name']
	search_fiedls = ['pt_name'] 


'''
企业类型 
'''
class COM_TYPEAdmin(object):
	list_display = ['ct_name']
	search_fiedls = ['ct_name'] 
'''
股权众筹
'''
class STOCKAdmin(object):
	list_display = ['st_user','st_title','st_image','st_brief','st_begin_time',
	'st_end_time','st_create_time','st_scale','st_total_price','st_current_price','st_min_price','st_industry',
	'st_province','st_pro_type','st_com_type','st_like_count','st_invest_count','st_hint','st_com_brief','st_protect',
	'st_inf_expose','st_plan','st_finance','st_good_bad','st_market','st_business','st_risk','st_team','st_prospectus',
	'st_sort','st_status']
	search_fiedls = ['st_user'] 

'''
债权众筹 
'''
class BONDAdmin(object):
	list_display = ['bo_user','bo_title','bo_image','bo_com_name','bo_brief','bo_begin_time','bo_create_time','bo_end_time',
	'bo_scale','bo_province','bo_total_price','bo_current_price','bo_min_price','bo_pro_type','bo_com_type',
	'bo_goal','bo_repayment','bo_com_inf','bo_risk_inf','bo_files','bo_repay_plan','bo_finance','bo_sort',
	'bo_status']
	search_fiedls = ['bo_user'] 

'''
用户投资 股权众筹
'''
class INVEST_STOCKAdmin(object):
	list_display = ['is_user','is_stock','is_amount','is_date','is_soon_profit','is_profit_date','is_status']
	search_fiedls = ['is_user '] 


'''
用户充值
'''
class RECHARGEAdmin(object):
	list_display = ['rc_user','rc_type','rc_value','rc_date','rc_status']
	search_fiedls = ['rc_user '] 
'''
用户喜欢
'''
class USER_FOCUSAdmin(object):
	list_display = ['uf_user','uf_stock','uf_bond','uf_update_time']
	search_fiedls = ['uf_user'] 

'''
用户讨论
'''
class TALKAdmin(object):
	list_display = ['ta_user','ta_stock','ta_msg','ta_pre_id']
	search_fiedls = ['ta_user'] 

'''
系统通知表
'''
class NOTICEAdmin(object):
	list_display = ['no_title','no_body','no_time','no_type','no_sort','no_is_delete']
	search_fiedls = ['no_title'] 

'''
用户通知表
'''
class NOTICE_USERAdmin(object):
	list_display = ['nu_title','nu_body','nu_time','nu_user','nu_type','nu_is_read','nu_is_delete']
	search_fiedls = ['nu_title'] 

'''
系统通知查看
'''
class NOTICE_READAdmin(object):
	list_display = ['nr_user','nr_notice']
	search_fiedls = ['nr_user'] 

'''
用户收益表
'''
class PROFITAdmin(object):
	list_display = ['pr_user','pr_amount','pr_date','pr_title']
	search_fiedls = ['pr_user'] 


'''
验证码
'''
class RANDOMCODEAdmin(object):
	list_display = ['rc_tel','rc_code','rc_time']
	search_fiedls = ['rc_tel'] 

xadmin.site.register(USERS,USERSAdmin)
xadmin.site.register(ACCOUNT,ACCOUNTAdmin)
xadmin.site.register(INDUSTRY, INDUSTRYAdmin)
xadmin.site.register(PROVINCE, PROVINCEAdmin) 
xadmin.site.register(PRO_TYPE,PRO_TYPEAdmin)
xadmin.site.register(COM_TYPE,COM_TYPEAdmin)
xadmin.site.register(STOCK,STOCKAdmin)
xadmin.site.register(BOND,BONDAdmin)
xadmin.site.register(RECHARGE,RECHARGEAdmin)
xadmin.site.register(USER_FOCUS,USER_FOCUSAdmin)
xadmin.site.register(NOTICE,NOTICEAdmin)
xadmin.site.register(NOTICE_USER,NOTICE_USERAdmin)
xadmin.site.register(PROFIT,PROFITAdmin)
xadmin.site.register(INVEST_STOCK,INVEST_STOCKAdmin)
xadmin.site.register(TALK,TALKAdmin)
xadmin.site.register(NOTICE_READ,NOTICE_READAdmin)
xadmin.site.register(RANDOMCODE,RANDOMCODEAdmin)






