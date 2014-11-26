#coding:utf-8
from models import *
from django.contrib.contenttypes.models import ContentType  
from django.contrib.contenttypes import generic  
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.db.models import Sum

'''
定义各类触发函数
'''
'''
股权认购触发函数
'''
def invest_stock_callback(sender, instance, signal, *args, **kwargs):
	post_data = instance
	ACCOUNT_obj = ACCOUNT.objects.get(ac_user__exact = post_data.is_user)
	#重新计算该账户总的认购金额
	ac_total_stock =  SUMModel(INVEST_STOCK,{'is_user':post_data.is_user},'is_amount')
	ac_total_bond =  SUMModel(INVEST_BOND,{'ib_user':post_data.is_user},'ib_amount')
	ACCOUNT_obj.ac_total_subscription = str(ac_total_stock+ac_total_bond)
	invest_stock = SUMModel(INVEST_STOCK,{'is_user':post_data.is_user,'is_status__id':2},'is_amount')
	invest_stock_3 = SUMModel(INVEST_STOCK,{'is_user':post_data.is_user,'is_status__id':3},'is_amount')
	invest_bond = SUMModel(INVEST_BOND,{'ib_user':post_data.is_user,'ib_status__id':2},'ib_amount')
	invest_bond_3 = SUMModel(INVEST_BOND,{'ib_user':post_data.is_user,'ib_status__id':3},'ib_amount')
	ACCOUNT_obj.ac_stock_invest = str(invest_stock+invest_stock_3)
	ACCOUNT_obj.ac_bond_invest = str(invest_bond+invest_bond_3)
	ACCOUNT_obj.ac_total_invest = str(invest_stock+invest_stock_3+invest_bond+invest_bond_3)
	ACCOUNT_obj.save()

'''
债权认购触发函数
'''
def invest_bond_callback(sender, instance, signal, *args, **kwargs):
	post_data = instance
	ACCOUNT_obj = ACCOUNT.objects.get(ac_user__exact = post_data.ib_user)
	#重新计算该账户总的认购金额
	ac_total_stock =  SUMModel(INVEST_STOCK,{'is_user':post_data.ib_user},'is_amount')
	ac_total_bond =  SUMModel(INVEST_BOND,{'ib_user':post_data.ib_user},'ib_amount')
	ACCOUNT_obj.ac_total_subscription = str(ac_total_stock+ac_total_bond)
	invest_stock = SUMModel(INVEST_STOCK,{'is_user':post_data.ib_user,'is_status__id':2},'is_amount')
	invest_stock_3 = SUMModel(INVEST_STOCK,{'is_user':post_data.ib_user,'is_status__id':3},'is_amount')
	invest_bond = SUMModel(INVEST_BOND,{'ib_user':post_data.ib_user,'ib_status__id':2},'ib_amount')
	invest_bond_3 = SUMModel(INVEST_BOND,{'ib_user':post_data.ib_user,'ib_status__id':3},'ib_amount')
	ACCOUNT_obj.ac_stock_invest = str(invest_stock+invest_stock_3)
	ACCOUNT_obj.ac_bond_invest = str(invest_bond+invest_bond_3)
	ACCOUNT_obj.ac_total_invest = str(invest_stock+invest_stock_3+invest_bond+invest_bond_3)
	ACCOUNT_obj.save()

'''
收益更改触发函数
'''
def profit_callback(sender, instance, signal, *args, **kwargs):
	post_data = instance
	ACCOUNT_obj = ACCOUNT.objects.get(ac_user__exact = post_data.pr_user)
	#计算收益
	ac_stock_profit = SUMModel(PROFIT,{'pr_user':post_data.pr_user,'pr_bond':None},'pr_amount')
	ac_total_profit = SUMModel(PROFIT,{'pr_user':post_data.pr_user},'pr_amount')
	ACCOUNT_obj.ac_stock_profit = str(ac_stock_profit)
	ACCOUNT_obj.ac_bond_profit = str(ac_total_profit - ac_stock_profit)
	ACCOUNT_obj.ac_total_profit = str(ac_total_profit)
	ACCOUNT_obj.save()

'''
定金更改触发函数
'''
def payment_callback(sender, instance, signal, *args, **kwargs):
	post_data = instance
	ACCOUNT_obj = ACCOUNT.objects.get(ac_user__exact = post_data.pa_user)
	ac_subscription = SUMModel(PAYMENT,{'pa_user':post_data.pa_user,'pa_status':0},'pa_amount')
	ACCOUNT_obj.ac_subscription = str(ac_subscription)
	ACCOUNT_obj.save()

#功能类，返回某一张表某个参数的SUM
#kwargs 条件
#object SUM对象
def SUMModel(model,kwargs,object):
	modelSUM =  model.objects.filter(**kwargs).aggregate(Sum(object))[object+'__sum']
	if modelSUM:
		return float(modelSUM)
	else:
		return 0