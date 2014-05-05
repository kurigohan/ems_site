from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError, connection
from django.contrib import messages

from ems.forms import RegistrationForm, EventCreationForm, EventEditForm, ReservationEditForm, QueryForm
from ems.models import Event, Reservation, Location, Approval, Attendance
from ems import status_const # constants for reservation status

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
def all_events(request, template_name="ajax/all_events.html"):
    """
    View all approved events/reservations
    """
    reservation_list = Reservation.objects.filter(status=status_const.APPROVED)
    return render(request, template_name, {'reservation_list':reservation_list})

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
            student_fee = form.cleaned_data['student_fee']
            staff_fee = form.cleaned_data['staff_fee']
            public_fee = form.cleaned_data['public_fee']

            try:
                with transaction.atomic():
                    event = Event(creator=creator,
                                        name=name, 
                                        category=category,
                                        description=description,
                                        is_public=is_public,
                                        student_fee=student_fee,
                                        staff_fee=staff_fee,
                                        public_fee=public_fee)
                    event.save()
                    reservation = Reservation(event=event,
                                                location=location,
                                                start_datetime=start_datetime,
                                                end_datetime=end_datetime)
                    reservation.save()
                    return redirect("my_events")
            except Exception as e: 
                messages.error(request, "%s: Event could not be created" % e)
    else:
        form = EventCreationForm()
    return render(request, template_name, {'form':form, 'redirect_url':reverse('my_events')})



@login_required
def event_details(request, event_id, template_name="ajax/event_details.html"):
    """
    View event and reservation details
    """
    event = get_object_or_404(Event, pk=event_id)
    return render(request, template_name, {'event':event})



@login_required
def edit_event(request, event_id, template_name="ajax/edit_event.html"):
    """
    Edit existing event
    """
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form1 = EventEditForm(request.POST, instance=event)
        form2 = ReservationEditForm(request.POST, instance=event.reservation)
        if form1.is_valid() and form2.is_valid():
            try:
                with transaction.atomic():
                    form2.save()
                    form1.save()
                return redirect('my_events')
            except Exception as e:
                messages.error(request, "%s: Event could not be edited" % e)

    else:
        form1= EventEditForm(instance=event)
        form2 = ReservationEditForm(instance=event.reservation)
    return render(request, template_name, {'event_form':form1, 'reservation_form':form2, 'event_id':event.id, 'redirect_url':reverse('my_events')})


@login_required
def delete_event(request, event_id):
    """
    Delete an event
    """
    event = get_object_or_404(Event, pk=event_id)
    reservation = event.reservation
    if request.user == event.creator:
        with transaction.atomic():
            reservation.delete()
            event.delete()
    return redirect('my_events')

#--------------------NOT IMPLEMENTED---------------------------


# Mod powers 

@login_required
def pending_events(request, template_name=""):
    """
    View all events that need approval/denial
    """
    return

@login_required
def approve_event(request, event_id):
    return #should redirect 


@login_required
def deny_event(request, event_id):
    return #should redirect 


# For extra 4 queries given by professor
@login_required
def summary_report(request, template_name=""):
    return

#--------------------------------------------------------------------------


@login_required
def location_details(request, loc_id, template_name="ajax/location_details.html"):
    """
    View location details and upcoming events at that location
    """
    location = get_object_or_404(Location, pk=loc_id)
    reservation_list = Reservation.objects.filter(status=status_const.APPROVED, location=location.id)
    return render(request, template_name, {'location':location, 'reservation_list':reservation_list})


@login_required
def query(request, template_name="ajax/query.html"):
    """
    Query the database
    """
    form = QueryForm()
    return render(request, template_name, {'form':form})
