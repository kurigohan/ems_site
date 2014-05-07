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
    url(r'^event/create/$', views.create_event, name='create_event'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.edit_event, name='edit_event'),
    url(r'^event/delete/(?P<event_id>\d+)/$', views.delete_event, name='delete_event'),
    url(r'^event/details/(?P<event_id>\d+)/$', views.event_details, name='event_details'),
    url(r'^location/(?P<loc_id>\d+)/$', views.location_details, name='location_details'),
    url(r'^pending_events/$', views.pending_events, name='pending_events'),
    url(r'^event/approve/(?P<event_id>\d+)/$', views.approve_event, name="approve_event"),
    url(r'^event/deny/(?P<event_id>\d+)/$', views.deny_event, name="deny_event"),
    url(r'^summary_report/$', views.summary_report, name='summary_report'),
)
