#coding:utf8
from django import forms
from models import *

class USERSFORM(forms.ModelForm):

	class Meta:
		model = USERS