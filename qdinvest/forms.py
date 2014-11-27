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