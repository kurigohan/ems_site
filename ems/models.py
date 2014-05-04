from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime

class Event(models.Model):
    creator = models.OneToOneField(User)
    category = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True)
    is_active = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    student_fee = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    staff_fee = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    public_fee = models.DecimalField(max_digits=4, decimal_places=2, default=0)


    def start(self):
        return self.reservation.start_datetime

    def end(self):
        return self.reservation.end_datetime

    def location(self):
        return self.reservation.location

    def is_free(self):
        if self.student_fee == 0 and self.staff_fee == 0 and self.public_fee == 0:
            return True
        return False

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event_details', args=[str(self.id)])

class Location(models.Model):
    name = models.CharField(max_length=255)
    building = models.CharField(max_length=50, blank=True)
    room = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=500, blank=True)
    capacity = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('location_details', args=[str(self.id)])

class Reservation(models.Model):
    event = models.ForeignKey(Event)
    location = models.ForeignKey(Location)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    is_approved = models.BooleanField(default=False)

class Approval(models.Model):
    approver = models.ForeignKey(User)
    reservation = models.OneToOneField(Reservation)
    date = models.DateTimeField()

class Attendance(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)


