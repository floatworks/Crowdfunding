#coding:utf8
from django import forms
from models import *

class USERSForm(forms.ModelForm):

	class Meta:
		model = USERS