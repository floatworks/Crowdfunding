from django.conf.urls import patterns, url
import viewWechat

urlpatterns = patterns('',
	url(r'^$', viewWechat.Index, name='Index'),
	url(r'^index/$', viewWechat.Index, name='Index'),
	url(r'^prolist/(\d+)$', viewWechat.GetProList, name='GetProList'),
	url(r'^prodetail/t(\w)d(\d+)$', viewWechat.ProDetail, name='ProDetail'),
	url(r'^nodetail/t(\w+)d(\d+)$', viewWechat.NoticeDetail, name='NoticeDetail'),
	url(r'^promanage/t(\w+)d(\d+)$', viewWechat.ProManage, name='ProManage'),

	url(r'^projectdetail', viewWechat.Projectdetail, name='Projectdetail'),
	)