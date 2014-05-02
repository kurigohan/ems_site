from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.shortcuts import render
from ems.models import Event, Location, Reservation, Attendance, Approval
from ems.forms import QueryForm
from django.http import Http404
from django.contrib import messages

from django.db import connection
def db_explorer(request, template_name="admin/ems/db_explorer.html"):
    """
    Query the database with select statements
    """
    if not request.user.is_superuser:
        raise Http404

    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            try:
                cursor = connection.cursor()
                cursor.execute(form.cleaned_data['query'])
                result_set = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                return render(request, template_name, {'form':form, 'columns':columns, 'result_set':result_set})
            except: 
                messages.error(request, "Error: Could not execute query.")

    else:
        form = QueryForm()
    return render(request, template_name, {'form':form})


def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
                url(r'^db_explorer/$', admin.site.admin_view(db_explorer))
            )
        return my_urls + urls
    return get_urls


admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Reservation)
admin.site.register(Attendance)
admin.site.register(Approval)


admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls