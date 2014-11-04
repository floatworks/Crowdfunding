#coding:utf-8
from django.contrib import admin
from models import *

# Register your models here.
'''
基础用户表
'''

class USERSAdmin(admin.ModelAdmin):
	list_display = ['u_name','u_pwd','u_tel','u_status']
	list_filter = ['u_status',]
	search_fiedls = ['u_name']
   
admin.site.register(USERS,USERSAdmin) 



'''
用户账户信息
'''

class ACCOUNTAdmin(admin.ModelAdmin):
	list_display = ['ac_user','ac_like','ac_support','ac_sponsor','ac_infos',
	'ac_balance','ac_frozen','ac_soon_profit','ac_actual_profit','ac_total_invest',
	'ac_total_profit']
	search_fiedls = ['ac_user']

admin.site.register(ACCOUNT,ACCOUNTAdmin)


'''
行业
'''

class INDUSTRYAdmin(admin.ModelAdmin):
	list_display = ['in_name','in_sort']
	search_fiedls = ['in_name'] 

admin.site.register(INDUSTRY, INDUSTRYAdmin) 


'''
地区 城市 基础信息
'''

class PROVINCEAdmin(admin.ModelAdmin):
	list_display = ['pr_name']
	search_fiedls = ['pr_name'] 
admin.site.register(PROVINCE, PROVINCEAdmin) 