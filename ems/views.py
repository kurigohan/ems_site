from django.shortcuts import render, redirect,get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def test_view(request, template_name='base.html'):
    return render(request, template_name)
