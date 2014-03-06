from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # main urls
    url(r'^', include('main.urls')),
    # Serving media
    url(r'^main/', include('main.urls')),
    # django admin urls
    url(r'^manager/', include(admin.site.urls)),
    #django-registration
    url(r'^accounts/', include('registration.backends.default.urls')),

)
