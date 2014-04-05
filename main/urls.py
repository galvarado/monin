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
     url(r'^admin/config/?$', 'admin_config', name='admin_config'),
    url(r'^admin/clients/?$', 'admin', name='admin'),
    url(r'^admin/clients/add/?$', 'admin_client_add', name='admin_client_add'),
    url(r'^admin/clients/password/(?P<pk>\d+)/?$', 'admin_client_password', name='admin_client_password'),
    url(r'^admin/clients/deactivate/?$', 'admin_client_deactivate', name='admin_client_deactivate'),
    url(r'^admin/clients/delete/(?P<pk>\d+)/?$', 'admin_client_delete', name='admin_client_delete'),
    url(r'^admin/categories/?$', 'admin_categories', name='admin_categories'),
    url(r'^admin/categories/all/?$', 'admin_categories_all', name='admin_categories_all'),
    url(r'^admin/category/add/?$', 'admin_category_add', name='admin_category_add'),
    url(r'^admin/category/deactivate/?$', 'admin_category_deactivate', name='admin_category_deactivate'),
    url(r'^admin/category/delete/(?P<pk>\d+)/?$', 'admin_category_delete', name='admin_category_delete'),
    url(r'^admin/categories/sample/?$', 'admin_categories_sample', name='admin_categories_sample'),
    url(r'^admin/categories/sample/all/?$', 'admin_categories_sample_all', name='admin_categories_sample_all'),
    url(r'^admin/category/sample/add/?$', 'admin_category_sample_add', name='admin_category_sample_add'),
    url(r'^admin/category/sample/deactivate/?$', 'admin_category_sample_deactivate', name='admin_category_sample_deactivate'),
    url(r'^admin/category/sample/delete/(?P<pk>\d+)/?$', 'admin_category_sample_delete', name='admin_category_sample_delete'),
    url(r'^admin/products/sample/?$', 'admin_products_sample', name='admin_products_sample'),
    url(r'^admin/products/sample/all/?$', 'admin_products_sample_all', name='admin_products_all'),
    url(r'^admin/product/sample/add/?$', 'admin_product_sample_add', name='admin_product_sample_add'),
    url(r'^admin/product/sample/deactivate/?$', 'admin_product_sample_deactivate', name='admin_product_sample_deactivate'),
    url(r'^admin/product/sample/delete/(?P<pk>\d+)/?$', 'admin_product_sample_delete', name='admin_product_sample_delete'),
    url(r'^admin/products/?$', 'admin_products', name='admin_products'),
    url(r'^admin/products/all/?$', 'admin_products_all', name='admin_products_all'),
    url(r'^admin/product/add/?$', 'admin_product_add', name='admin_product_add'),
    url(r'^admin/product/deactivate/?$', 'admin_product_deactivate', name='admin_product_deactivate'),
    url(r'^admin/product/delete/(?P<pk>\d+)/?$', 'admin_product_delete', name='admin_product_delete'),
    url(r'^admin/sliders/?$', 'admin_sliders', name='admin_sliders'),
    url(r'^admin/sliders/all/?$', 'admin_sliders_all', name='admin_sliders_all'),
    url(r'^admin/slider/add/?$', 'admin_slider_add', name='admin_slider_add'),
    url(r'^admin/slider/deactivate/?$', 'admin_slider_deactivate', name='admin_slider_deactivate'),
    url(r'^admin/slider/delete/(?P<pk>\d+)/?$', 'admin_slider_delete', name='admin_slider_delete'),
    # Translations Urls
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

# Static files serve
urlpatterns += patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.contrib.staticfiles.views.serve', kwargs={'insecure':True}),
) 
