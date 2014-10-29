from django.conf.urls import patterns, url
import viewWeb

urlpatterns = patterns('',
	url(r'^$', viewWeb.index, name='index'),
	url(r'^stock/$', viewWeb.stock, name='stock'),
	url(r'^bond/$', viewWeb.bond, name='bond'),
	url(r'^transfer/$', viewWeb.transfer, name='transfer'),
	url(r'^bdetail/$', viewWeb.bdetail, name='bdetail'),
	url(r'^sdetail/$', viewWeb.sdetail, name='sdetail'),
	)