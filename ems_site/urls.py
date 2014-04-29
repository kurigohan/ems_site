from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from ems import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ems_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',  name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/login/'}, name='logout'),
    url(r'^register/$', views.register_user, name='register'),

)
