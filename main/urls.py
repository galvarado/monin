from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import re

urlpatterns = patterns('main.views',
    # App Urls
    url(r'^$', 'index', name='index'),
    url(r'^logout/?$', 'logout', name='logout'),
    url(r'^home/?$', 'home', name='home'),
    url(r'^our/?$', 'our', name='our'),
    url(r'^access/?$', 'access', name='access'),
    url(r'^products/?$', 'products', name='products'),
    url(r'^products/all/?$', 'products_all', name='products_all'),
    url(r'^orders/all/?$', 'orders_all', name='orders_all'),
    url(r'^order/delete/?$', 'order_delete', name='order_delete'),
    url(r'^order/do/?$', 'order_do', name='order_do'),
    url(r'^clients/?$', 'clients', name='clients'),
    url(r'^clients/all/?$', 'clients_all', name='clients_all'),
    url(r'^order/?$', 'order', name='order'),
    url(r'^order/product/(?P<pk>\d+)/?$', 'order_product', name='order_product'),
    url(r'^contact/?$', 'contact', name='contact'),
    # Mobile Urls
    url(r'^mobile/?$', 'mobile', name='mobile'),
    url(r'^mobile_order/?$', 'mobile_order', name='mobile_order'),
    # Admin Urls
    url(r'^admin/?$', 'admin_login', name='admin_login'),
    url(r'^admin/clients/?$', 'admin', name='admin'),
    url(r'^admin/clients/add/?$', 'admin_client_add', name='admin_client_add'),
    url(r'^admin/clients/password/(?P<pk>\d+)/?$', 'admin_client_password', name='admin_client_password'),
    url(r'^admin/clients/deactivate/?$', 'admin_client_deactivate', name='admin_client_deactivate'),
    url(r'^admin/clients/delete/(?P<pk>\d+)/?$', 'admin_client_delete', name='admin_client_delete'),

    # Translations Urls
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

# Static files serve
urlpatterns += patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.contrib.staticfiles.views.serve', kwargs={'insecure':True}),
) 
