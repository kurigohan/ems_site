from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError, connection
from django.contrib import messages

from ems.forms import RegistrationForm, EventCreationForm
from ems.models import Event, Reservation, Location, Approval, Attendance


@login_required
def dashboard(request, template_name='base.html'):
    """
    Displays dashboard
    """
    return render(request, template_name, {'user':request.user})

@login_required
def home(request, template_name='ajax/home.html'):
    """
    Displays AJAX home page
    """
    return render(request, template_name, {'user':request.user})



# --------------------- User Login/Registration ---------------------------
@login_required
def logout(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return redirect('login')


def register_user(request, template_name= 'registration/registration_form.html'):
    """
    Create a user
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        original = request.POST.get('username')
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            test = {'username':username, 'email':email, 'original':original}
            User.objects.create_user(username=username, email=email, password=password,
                        first_name=first_name, last_name=last_name)
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request, template_name, {'form':form})



 # --------------- Events ---------------------   

@login_required
def my_events(request, template_name="ajax/my_events.html"):
    """
    View all events created by the user
    """
    event_list = Event.objects.filter(creator=request.user)
    return render(request, template_name, {'event_list':event_list})


@login_required
def create_event(request, template_name="ajax/create_event.html"):
    """
    Create an event and reservation
    """
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            creator = request.user
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']
            is_public = form.cleaned_data['is_public']
            start_datetime = form.cleaned_data['start_datetime']
            end_datetime = form.cleaned_data['end_datetime']
            try:
                with transaction.atomic():
                    event = Event(creator=creator,
                                        name=name, 
                                        category=category,
                                        description=description,
                                        is_public=is_public,)
                    event.save()
                    reservation = Reservation(event=event,
                                                location=location,
                                                start_datetime=start_datetime,
                                                end_datetime=end_datetime)
                    reservation.save()
            except IntegrityError: pass
                #messages.error(request, "An error occured during event creation")

            return redirect("my_events")
    else:
        form = EventCreationForm()
    return render(request, template_name, {'form':form})


@login_required
def event_details(request, event_id, template_name="ajax/event_details.html"):
    """
    View event and reservation details
    """
    event = get_object_or_404(Event, pk=event_id)
    event.start 
    return render(request, template_name, {'event':event})


@login_required
def browse_events(request, template_name="event/browse_events.html"):
    """
    View all approved events/reservations
    """
    reservation_list = Reservation.objects.filter(is_approved=True)

    return render(request, template_name, {'reservation_list':reservation_list})




@login_required
def location_details(request, loc_id, template_name="location/location_details.html"):
    """
    View location details
    """
    location = get_object_or_404(Event, pk=loc_id)

    return render(request, template_name, {'location':location})


