#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect

def Index(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('wechat/index.html',context_dict,context)