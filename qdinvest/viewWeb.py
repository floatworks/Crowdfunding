#coding:utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q


import simplejson as json
from datetime import datetime,timedelta
from  models import STOCK


def index(request):
	context = RequestContext(request)
   # context_dict = STOCK.objects.all()[0:3:1]
	context_dict = {}
	return render_to_response('qdinvest/index.html',{'context_dict':context_dict},context)

def bond(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/bond.html',context_dict,context)


def stock(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/stock.html',context_dict,context)

def transfer(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/transfer.html',context_dict,context)

def bdetail(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/bdetail.html',context_dict,context)

def sdetail(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/sdetail.html',context_dict,context)

def db(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('qdinvest/models_doc.html',context_dict,context)