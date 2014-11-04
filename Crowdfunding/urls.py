from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
import xadmin
xadmin.autodiscover()
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Crowdfunding.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('qdinvest.urls')),
    url(r'^c/', include('qdinvest.urls')),
    url(r'^app/', include('qdinvest.urlsapp')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'admin/', include(xadmin.site.urls)),
)


if settings.DEBUG:
	urlpatterns += patterns(
		'django.views.static',
		(r'media/(?P<path>.*)',
		'serve',
		{'document_root': settings.MEDIA_ROOT}),)