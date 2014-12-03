#coding:utf8
from django import forms
from models import *

class USERSFORM(forms.ModelForm):
	# u_name = forms.CharField(label='姓名')
	# u_pwd = forms.CharField(label='密码')
	# u_tel = forms.CharField(label='电话')
	# u_status = forms.IntegerField(label='用户状态') 
	class Meta:
		model = USERS
		# fields = ['u_name','u_pwd','u_tel','u_status']

class PROFITFORM(forms.ModelForm):

	class Meta:
		model = PROFIT

	def __init__(self,*args,**kwargs):
		super(PROFITFORM,self).__init__(*args,**kwargs)
		print kwargs
		inst = kwargs.get('initial')
		print inst
		if inst:
			self.fields['pr_stock'].queryset = STOCK.objects.filter(st_user = inst['pr_user'])