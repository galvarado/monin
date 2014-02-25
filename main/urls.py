from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import re

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^logout/?$', 'logout', name='logout'),
    url(r'^home/?$', 'home', name='home'),
    url(r'^our/?$', 'our', name='our'),
    url(r'^access/?$', 'access', name='access'),
    url(r'^products/?$', 'products', name='products'),
    url(r'^products/all/?$', 'products_all', name='products_all'),
    url(r'^orders/all/?$', 'orders_all', name='orders_all'),
    url(r'^order/delete/?$', 'order_delete', name='order_delete'),
    url(r'^clients/?$', 'clients', name='clients'),
    url(r'^order/?$', 'order', name='order'),
    url(r'^order/product/(?P<pk>\d+)/?$', 'order_product', name='order_product'),
    url(r'^contact/?$', 'contact', name='contact'),
    url(r'^mobile/?$', 'mobile', name='mobile'),
    url(r'^mobile_order/?$', 'mobile_order', name='mobile_order'),
    url(r'^admin/?$', 'admin', name='admin'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

# Static files serve
urlpatterns += patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.contrib.staticfiles.views.serve', kwargs={'insecure':True}),
) 
