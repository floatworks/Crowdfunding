#coding:utf-8
import xadmin
from xadmin import views
from models import *
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from xadmin.views import BaseAdminPlugin, ModelFormAdminView, DetailAdminView
from django.conf import settings
from django.db.models import TextField


class GlobalSetting(object):
	#设置base_site.html的Title
	site_title = '清大众筹后台管理系统'

	def get_site_menu(self):

		return (
            {'title': '用户管理','menus':(
                {'title': '用户管理', 'icon': 'fa fa-user', 'url': self.get_model_url(USERS, 'changelist')},
                {'title': '账户管理', 'icon': 'fa fa-file', 'url': self.get_model_url(ACCOUNT, 'changelist')},
                {'title': '收益管理', 'icon': 'fa fa-cny', 'url': self.get_model_url(PROFIT, 'changelist')},
                {'title': '定金管理', 'icon': 'fa fa-usd', 'url': self.get_model_url(PAYMENT, 'changelist')},
            )},
            {'title':'众筹管理','menus':(
            	{'title':'股权众筹','icon': 'fa fa-line-chart','url':self.get_model_url(STOCK,'changelist')},
            	{'title':'债权众筹','icon': 'fa fa-money','url':self.get_model_url(BOND,'changelist')},	
            )},
            {'title': '认购管理','menus':(
                {'title': '股权认购', 'icon': 'fa fa-bar-chart-o', 'url': self.get_model_url(INVEST_STOCK, 'changelist')},
                {'title': '债权认购', 'icon': 'fa fa-bank', 'url': self.get_model_url(INVEST_BOND, 'changelist')},
            )},
            {'title':'基础数据维护','menus':(
            	{'title':'行业方向','icon': 'fa fa-location-arrow','url':self.get_model_url(INDUSTRY,'changelist')},
            	{'title':'辐射区域','icon': 'fa fa-globe','url':self.get_model_url(PROVINCE,'changelist')},
            	{'title':'项目属性','icon': 'fa fa-briefcase','url':self.get_model_url(PRO_TYPE,'changelist')},
            	{'title':'企业类型','icon': 'fa fa-credit-card','url':self.get_model_url(COM_TYPE,'changelist')},
            )},
            {'title':'通知管理','menus':(
            	{'title':'系统通知','icon': 'fa fa-envelope','url':self.get_model_url(NOTICE,'changelist')},
            	{'title':'用户通知','icon': 'fa fa-envelope-o','url':self.get_model_url(NOTICE_USER,'changelist')},	
            )},
            {'title':'其他','menus':(
            	{'title':'用户反馈','icon': 'fa fa-comment','url':self.get_model_url(FEEDBACK,'changelist')},
            	{'title':'系统参数','icon': 'fa fa-gear','url':self.get_model_url(SETTINGS,'changelist')},	
            )},
        )

xadmin.site.register(views.CommAdminView, GlobalSetting)

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
	list_display = ['ac_user',
	'ac_stock_invest','ac_bond_invest','ac_total_invest','ac_stock_profit','ac_bond_profit',
	'ac_total_profit','ac_subscription','ac_total_subscription','ac_like','ac_support','ac_infos']
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
项目属性
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
	list_display = ['st_title','st_user','st_brief','st_is_commend','st_begin_time',
	'st_end_time','st_create_time','st_scale','st_total_price','st_current_price','st_min_price','st_industry',
	'st_province','st_pro_type','st_com_type','st_like_count','st_view_count','st_invest_count',
	'st_sort','st_status']
	list_filter = ('st_begin_time','st_end_time','st_create_time')
	search_fiedls = ['st_user']
	style_fields = {'st_hint':'ueditor','st_com_brief':'ueditor','st_protect':'ueditor','st_inf_expose':'ueditor',
					'st_plan':'ueditor','st_finance':'ueditor','st_good_bad':'ueditor','st_market':'ueditor',
					'st_business':'ueditor','st_risk':'ueditor','st_team':'ueditor','st_prospectus':'ueditor',
					'st_manage':'ueditor',}
	list_editable = ['st_is_commend']

'''
债权众筹 
'''
class BONDAdmin(object):
	list_display = ['bo_title','bo_user','bo_com_name','bo_brief','bo_is_commend','bo_begin_time','bo_create_time','bo_end_time',
	'bo_scale','bo_province','bo_total_price','bo_current_price','bo_min_price','bo_pro_type','bo_com_type','bo_like_count',
	'bo_view_count','bo_sort','bo_status']
	list_filter = ('bo_begin_time','bo_create_time','bo_end_time')
	search_fiedls = ['bo_user'] 
	style_fields = {'bo_com_inf':'ueditor','bo_risk_inf':'ueditor','bo_files':'ueditor','bo_repay_plan':'ueditor','bo_finance':'ueditor','bo_manage':'ueditor'}
   	list_editable = ['bo_is_commend']

'''
用户投资 股权众筹
'''
class INVEST_STOCKAdmin(object):
	list_display = ['is_user','is_stock','is_amount','is_status','is_date','is_soon_profit','is_profit_date']
	search_fiedls = ['is_user ']
	list_editable = ['is_status']

'''
用户投资 债权众筹 
'''
class INVEST_BONDAdmin(object):
	list_display = ['ib_user','ib_bond','ib_amount','ib_status','ib_date','ib_soon_profit','ib_profit_date']
	search_fields = ['ib_user']
	list_editable = ['ib_status']
	
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
	list_display = ['no_title','no_brief','no_time','no_type','no_sort','no_is_delete']
	search_fiedls = ['no_title'] 
	style_fields  = {'no_body':'ueditor'}
	list_editable = ['no_is_delete','no_sort','no_type']

'''
用户通知表
'''
class NOTICE_USERAdmin(object):
	list_display = ['nu_title','nu_brief','nu_time','nu_user','nu_type','nu_is_read','nu_is_delete']
	search_fiedls = ['nu_title'] 
	style_fields  = {'nu_body':'ueditor'}
	list_editable = ['nu_is_delete','nu_sort','nu_type']

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
	#def formfield_for_foreignkey(self, db_field, request, **kwargs):
	#	if db_field.name == "pr_user":
	#		kwargs["queryset"] = USERS.objects.filter(u_status=3)
	#	return super(PROFITAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	list_display = ['pr_user','pr_amount','pr_date','pr_stock','pr_bond']
	search_fiedls = ['pr_user']



class PAYMENTAdmin(object):
	list_display = ['pa_user','pa_amount','pa_date','pa_stock','pa_bond','pa_status']
	search_fiedls = ['pa_user']
	list_editable = ['pa_status']


'''
验证码
'''
class RANDOMCODEAdmin(object):
	list_display = ['rc_tel','rc_code','rc_time']
	search_fiedls = ['rc_tel'] 

'''
系统设置
'''
class SETTINGSAdmin(object):
	list_display = ['se_android_version','se_ios_version']

'''
'''
class FEEDBACKAdmin(object):
	list_display = ['fe_user','fe_mail','fe_time','fe_content']

class XadminUEditorWidget(UEditorWidget):
	def __init__(self,**kwargs):
		self.ueditor_options=kwargs
		self.Media.js = None
		super(XadminUEditorWidget,self).__init__(kwargs)

class UeditorPlugin(BaseAdminPlugin):
	def get_field_style(self, attrs, db_field, style, **kwargs):
		if style == 'ueditor':
			if isinstance(db_field, UEditorField):
				widget = db_field.formfield().widget
				param = {}
				param.update(widget.ueditor_settings)
				param.update(widget.attrs)
				return {'widget': XadminUEditorWidget(**param)}
			if isinstance(db_field, TextField):
				return {'widget': XadminUEditorWidget}
		return attrs
	def block_extrahead(self, context, nodes):
		js = '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "ueditor/ueditor.config.js")
		js += '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "ueditor/ueditor.all.min.js")
		nodes.append(js)

xadmin.site.register_plugin(UeditorPlugin,DetailAdminView)
xadmin.site.register_plugin(UeditorPlugin,ModelFormAdminView)

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
xadmin.site.register(INVEST_BOND,INVEST_BONDAdmin)
xadmin.site.register(TALK,TALKAdmin)
xadmin.site.register(NOTICE_READ,NOTICE_READAdmin)
xadmin.site.register(RANDOMCODE,RANDOMCODEAdmin)
xadmin.site.register(SETTINGS,SETTINGSAdmin)
xadmin.site.register(FEEDBACK,FEEDBACKAdmin)
xadmin.site.register(PAYMENT,PAYMENTAdmin)




