from django.conf.urls import patterns, url
import viewWechat

urlpatterns = patterns('',
	url(r'^$', viewWechat.Index, name='Index'),
	url(r'^index/$', viewWechat.Index, name='Index'),
	)