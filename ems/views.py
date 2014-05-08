from datetime import datetime, timedelta
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError, connection
from django.contrib import messages

from ems.forms import RegistrationForm, EventCreationForm, EventEditForm, ReservationEditForm, QueryForm, SummaryReportForm
from ems.models import Event, Reservation, Location, Approval, Attendance
from ems import status_const # constants for reservation status

@login_required
def dashboard(request, template_name='base.html'):
    """
    Displays dashboard
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
            prepay = form.cleaned_data['prepay']

            try:
                with transaction.atomic():
                    event = Event(creator=creator,
                                        name=name, 
                                        category=category,
                                        description=description,
                                        is_public=is_public,
                                        student_fee=student_fee,
                                        staff_fee=staff_fee,
                                        public_fee=public_fee,
                                        prepay=prepay)
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
    attendance_list = Attendance.objects.filter(event_id=event.id)
    return render(request, template_name, {'event':event, 'attendance_list':attendance_list})



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
    Delete an event and its reservation
    """
    event = get_object_or_404(Event, pk=event_id)
    reservation = event.reservation
    if request.user == event.creator:
        with transaction.atomic():
            reservation.delete()
            event.delete()
    return redirect('my_events')



# Mod powers 

@login_required
def pending_events(request, template_name="ajax/pending_events.html"):
    """
    View all events that need approval/denial
    """
    if not request.user.is_staff:
        raise Http404
    pending_list = Event.objects.filter(reservation__status=status_const.PENDING)
    return render(request, template_name, {'pending_list': pending_list})


@login_required
def approve_event(request, event_id):
    """
    Set the status of an event reservation to 'approved' and redirect to pending events page
    """
    if not request.user.is_staff:
        raise Http404
    event = get_object_or_404(Event, pk=event_id)
    event.reservation.status = status_const.APPROVED
    event.reservation.save()
    return redirect('pending_events') 


@login_required
def deny_event(request, event_id):
    """
    Set the status of an event reservation to 'denied' and redirect to pending events page
    """
    if not request.user.is_staff:
        raise Http404
    event = get_object_or_404(Event, pk=event_id)
    event.reservation.status = status_const.DENIED
    event.reservation.save()
    return redirect('pending_events')


@login_required
def summary_report(request, template_name="ajax/summary_report.html"):
    """
    View summary report of events
    """
    if not request.user.is_staff:
        raise Http404

    week_start_datetime = datetime.now()
    week_start_datetime = week_start_datetime.replace(tzinfo=timezone.utc)

    if request.method == 'POST':
        submitted_form = SummaryReportForm(request.POST)
        if submitted_form.is_valid():
            week_start_datetime = submitted_form.cleaned_data['week_start_datetime']

    week_end_datetime = week_start_datetime + timedelta(days=7)

    event_count = Event.objects.filter(reservation__status=status_const.APPROVED, reservation__start_datetime__gte=week_start_datetime, reservation__start_datetime__lte=week_end_datetime).count()
    attendance = Attendance.objects.filter(event__reservation__start_datetime__gte=week_start_datetime, event__reservation__start_datetime__lte=week_end_datetime).count()

    form = SummaryReportForm()
    return render(request, template_name, {'form':form, 'event_count':event_count, 'attendance':attendance})


@login_required
def location_details(request, loc_id, template_name="ajax/location_details.html"):
    """
    View location details and upcoming events at that location
    """
    location = get_object_or_404(Location, pk=loc_id)
    reservation_list = Reservation.objects.filter(status=status_const.APPROVED, location=location.id)
    return render(request, template_name, {'location':location, 'reservation_list':reservation_list})

