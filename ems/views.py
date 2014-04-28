from django.shortcuts import render, redirect,get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def test_view(request, template_name='base.html'):
    return render(request, template_name)


def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return redirect('test')