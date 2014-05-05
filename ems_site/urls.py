from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from ems import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ems_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^home/$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',  name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/login/'}, name='logout'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^my_events/$', views.my_events, name='my_events'),
    url(r'^all_events/$', views.all_events, name='all_events'),
    url(r'^create_event/$', views.create_event, name='create_event'),
    url(r'^event/(?P<event_id>\w+)/$', views.event_details, name='event_details'),
    url(r'^location/(?P<loc_id>\w+)/$', views.location_details, name='location_details'),
    url(r'^query/$', views.query, name='query'),
)
