from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
         (r'^$', 'almostmyigoogle.index.index'),
	 (r'^openid/', include('django_openid_auth.urls')),
	 (r'^lookup/$', 'almostmyigoogle.service.lookup_item'),
	 (r'^visited/$', 'almostmyigoogle.service.visited'),
    # Examples:
    # url(r'^$', 'almostmyigoogle.views.home', name='home'),
    # url(r'^almostmyigoogle/', include('almostmyigoogle.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
) 
urlpatterns += staticfiles_urlpatterns()
