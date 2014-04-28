from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from ems import views as EMSView
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ems_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^test/$', EMSView.test_view, name='test'),
)
