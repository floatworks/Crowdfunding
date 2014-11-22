from django.conf.urls import patterns, url
import viewWechat

urlpatterns = patterns('',
	url(r'^$', viewWechat.Index, name='Index'),
	url(r'^index/(.+)$', viewWechat.Index, name='Index'),
	url(r'^pro_detail/(.+)$', viewWechat.Pro_detail, name='Pro_detail'),
	)