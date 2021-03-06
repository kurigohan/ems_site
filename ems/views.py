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
from django.db.models import Q
from ems.forms import RegistrationForm, EventCreationForm, EventEditForm, ReservationEditForm, QueryForm, SummaryReportForm, SearchForm
from ems.models import Event, Reservation, Location, Approval, Attendance, Category
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
    attend_list = Attendance.objects.filter(user=request.user)
    return render(request, template_name, {'event_list':event_list, 'attend_list':attend_list})

@login_required
def all_events(request, template_name="ajax/all_events.html"):
    """
    View all approved events/reservations
    """
    reservation_list = Reservation.objects.filter(status=status_const.APPROVED)
    search_term = ""
    if request.method == 'GET' and 'search_term' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
    else:
        form = SearchForm()
    if search_term:
        reservation_list = event_search(search_term)
    return render(request, template_name, {'reservation_list':reservation_list, 'form':form})

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
    permissions = {'creator':False, 'mod': False,  'prepay': False, 'attend':False}

    if request.user == event.creator:
        permissions['creator'] = True
    if request.user.is_staff and event.reservation.status == status_const.PENDING:
        permissions['mod'] = True
    if event.reservation.status == status_const.APPROVED:
        user_register_count = Attendance.objects.filter(user=request.user, event=event).count()
        if user_register_count == 0:
            permissions['attend'] = True
        if event.prepay:
            permissions['prepay'] = True

    return render(request, template_name, {'event':event, 'attendance_list':attendance_list, 'permissions':permissions})



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
    date = timezone.now()
    new_attendee = Attendance(user=event.creator, 
                                                event=event,
                                                prepaid=False,
                                                date_registered=date
                                                )
    new_attendee.save()

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
        form = SummaryReportForm(request.POST)
        if form.is_valid():
            week_start_datetime = form.cleaned_data['week_start_datetime']
    else:
        form = SummaryReportForm()
    week_end_datetime = week_start_datetime + timedelta(days=7)

    total_event_count = Event.objects.filter(reservation__start_datetime__gte=week_start_datetime, reservation__start_datetime__lte=week_end_datetime).count()
    approved_event_count = Event.objects.filter(reservation__status=status_const.APPROVED, reservation__start_datetime__gte=week_start_datetime, reservation__start_datetime__lte=week_end_datetime).count()
    attendance = Attendance.objects.filter(event__reservation__start_datetime__gte=week_start_datetime, event__reservation__start_datetime__lte=week_end_datetime)
    attendance_count = attendance.count()
    revenue = 0

    for currentAttendance in attendance:
        revenue = revenue + currentAttendance.event.student_fee

    categories = Category.objects.all()

    category_registration = {}
    category_prepay = {}

    for current_category in categories:
        category_registration[current_category.name] = Attendance.objects.filter(event__category=current_category, event__reservation__start_datetime__gte=week_start_datetime, event__reservation__start_datetime__lte=week_end_datetime).count()
        category_prepay[current_category.name] = Attendance.objects.filter(prepaid=True, event__category=current_category, event__reservation__start_datetime__gte=week_start_datetime, event__reservation__start_datetime__lte=week_end_datetime).count()

    category_payment_data = {}

    for current_category in category_registration:
        current_category_percent_prepay = 0
        if category_registration[current_category] != 0:
            current_category_percent_prepay = category_prepay[current_category]/float(category_registration[current_category])*100
        category_payment_data[current_category] = (category_registration[current_category], category_prepay[current_category], current_category_percent_prepay)

    return render(request, template_name, {'form':form, 'total_event_count':total_event_count, 'approved_event_count':approved_event_count, 'attendance_count':attendance_count, 'revenue':revenue, 'category_payment_data':category_payment_data})

@login_required
def attend(request, event_id):
    """
    Register to attend an event
    """
    event = get_object_or_404(Event, pk=event_id)

    user_register_count = Attendance.objects.filter(user=request.user, event=event).count()

    if user_register_count != 0:
        messages.error(request, "Error: You are already attending this event.")
        return redirect('event_details', event_id=event_id)

    timestamp = timezone.now()
    #timestamp = timestamp.replace(tzinfo=timezone.utc)

    attendance = Attendance(user=request.user,
                    event=event, 
                    prepaid=False,
                    date_registered=timestamp)
    attendance.save()
    return redirect('event_details', event_id=event_id)

@login_required
def prepay(request, event_id):
    """
    Prepay to attend an event
    """
    event = get_object_or_404(Event, pk=event_id)

    if not event.can_prepay:
        messages.error(request, "Error: Pre-payments are not accepted.")
        return redirect('event_details', event_id=event_id)

    user_register_count = Attendance.objects.filter(user=request.user, event=event).count()

    if user_register_count != 0:
        messages.error(request, "Error: User has already prepaid for this event.")
        return redirect('event_details', event_id=event_id)

    timestamp = timezone.now()
    #timestamp = timestamp.replace(tzinfo=timezone.utc)

    attendance = Attendance(user=request.user,
                    event=event, 
                    prepaid=True,
                    date_registered=timestamp)
    attendance.save()
    return redirect('event_details', event_id=event_id)



@login_required
def location_details(request, loc_id, template_name="ajax/location_details.html"):
    """
    View location details and upcoming events at that location
    """
    location = get_object_or_404(Location, pk=loc_id)
    reservation_list = Reservation.objects.filter(status=status_const.APPROVED, location=location.id)
    return render(request, template_name, {'location':location, 'reservation_list':reservation_list})






def event_search(term):
    """
    Search event names that contain the given search term
    """

    search_results = Reservation.objects.filter(Q(status=status_const.APPROVED), Q(event__name__icontains=term) | Q(event__description__icontains=term) | Q(location__name__icontains=term))
    return search_results
