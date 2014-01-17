from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import re

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^zohoverify/verifyforzoho.html$', 'zohoverify', name='zohoverify'),
)

# Static files serve
urlpatterns += patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.contrib.staticfiles.views.serve', kwargs={'insecure':True}),
) 
