from django.conf.urls import patterns, url
import viewWeb

urlpatterns = patterns('',
	url(r'^$', viewWeb.index, name='index'),
	)