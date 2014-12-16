from django.conf.urls import patterns, url
import viewWeb

urlpatterns = patterns('',
	url(r'^$', viewWeb.index, name='index'),
	#url(r'^\w*/$', viewWeb.stock1, name='stock1'),
	url(r'^stock/$', viewWeb.stock, name='stock'),
	url(r'^bond/$', viewWeb.bond, name='bond'),
	
	url(r'^login/$', viewWeb.login, name='login'),
	url(r'^logout/$', viewWeb.logout, name='logout'),
	url(r'^register/$', viewWeb.register, name='register'),
	url(r'^register1/$', viewWeb.register1, name='register1'),
	url(r'^register2/$', viewWeb.register2, name='register2'),
	url(r'^test/$', viewWeb.test, name='test'),
	url(r'^test1/$', viewWeb.test1, name='test1'),
	url(r'^bdetail/(.+)$', viewWeb.bdetail, name='bdetail'),
	url(r'^sdetail/(.+)$', viewWeb.sdetail, name='sdetail'),
	url(r'^db/$', viewWeb.db, name='db'),
	url(r'^testUeditor/$', viewWeb.testUeditor, name='testUeditor'),
	url(r'^forget/$', viewWeb.forget, name='forget'),
	url(r'^forget1/$', viewWeb.forget1, name='forget1'),	
	url(r'^forget3/$', viewWeb.forget3, name='forget3'),
	url(r'^forget4/$', viewWeb.forget4, name='forget4'),
	url(r'^forget5/$', viewWeb.forget5, name='forget5'),
	
	url(r'^account_list/$', viewWeb.account_list, name='account_list'),
	url(r'^stock_list/$', viewWeb.stock_list, name='stock_list'),
	url(r'^bond_list/$', viewWeb.bond_list, name='bond_list'),
	url(r'^like_list/$', viewWeb.like_list, name='like_list'),
	url(r'^news/$', viewWeb.news, name='news'),
	url(r'^news2/$', viewWeb.news2, name='news2'),
	)