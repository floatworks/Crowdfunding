from django.conf.urls import patterns, url
import viewWeb

urlpatterns = patterns('',
	url(r'^$', viewWeb.index, name='index'),
	#url(r'^\w*/$', viewWeb.stock1, name='stock1'),
	url(r'^stock/$', viewWeb.stock, name='stock'),
	url(r'^bond/$', viewWeb.bond, name='bond'),
	url(r'^account/$', viewWeb.account, name='account'),
	url(r'^login/$', viewWeb.login, name='login'),
	url(r'^bdetail/(.+)$', viewWeb.bdetail, name='bdetail'),
	url(r'^sdetail/(.+)$', viewWeb.sdetail, name='sdetail'),
	url(r'^db/$', viewWeb.db, name='db'),
	url(r'^testUeditor/$', viewWeb.testUeditor, name='testUeditor'),
	)