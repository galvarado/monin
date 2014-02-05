from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import re

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^home/?$', 'home', name='home'),
    url(r'^our/?$', 'our', name='our'),
    url(r'^access/?$', 'access', name='access'),
    url(r'^products/?$', 'products', name='products'),
    url(r'^clients/?$', 'clients', name='clients'),
    url(r'^contact/?$', 'contact', name='contact'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

# Static files serve
urlpatterns += patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.contrib.staticfiles.views.serve', kwargs={'insecure':True}),
) 
