from django.conf.urls import patterns, url
import viewApp

urlpatterns = patterns('',
	url(r'^reg/$', viewApp.Register, name='Register'),
	url(r'^code/$', viewApp.GetRandomCode, name='GetRandomCode'),
	url(r'^login/$', viewApp.Login, name='Login'),
	url(r'^pwd/$', viewApp.RePassWord, name='RePassWord'),
	url(r'^forget/$', viewApp.Forget, name='Forget'),
	)