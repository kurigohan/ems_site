from django.shortcuts import render, redirect,get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from ems.forms import RegistrationForm

@login_required
def home(request, template_name='base.html'):
    return render(request, template_name)


def logout(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return redirect('login')


def register_user(request):
    """
    Create a user
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        original = request.POST.get('username')
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            test = {'username':username, 'email':email, 'original':original}
            User.objects.create_user(username, email, password)
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/registration_form.html', {'form':form})
