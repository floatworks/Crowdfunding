from django.conf.urls import patterns, url
import viewApp

urlpatterns = patterns('',
	url(r'^reg/$', viewApp.Register, name='Register'),
	url(r'^code/$', viewApp.GetRandomCode, name='GetRandomCode'),
	url(r'^login/$', viewApp.Login, name='Login'),
	url(r'^pwd/$', viewApp.RePassWord, name='RePassWord'),
	url(r'^forget/$', viewApp.Forget, name='Forget'),
	url(r'^projects/$', viewApp.GetProjects, name='GetProjects'),
	url(r'^recompro/$', viewApp.GetProjectsSort, name='GetProjectsSort'),
	url(r'^searchpro/$', viewApp.SearchProject, name='SearchProject'),
	url(r'^probase/$', viewApp.ProjectBase, name='ProjectBase'),
	url(r'^like/$', viewApp.ProLike, name='ProLike'),
	)