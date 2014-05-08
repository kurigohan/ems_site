from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime
from ems import status_const

class Category(models.Model):
	name = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "categories"

class Event(models.Model):
    creator = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True)
    is_active = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    student_fee = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    staff_fee = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    public_fee = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    prepay = models.BooleanField(default=False)

    def start(self):
        return self.reservation.start_datetime

    def end(self):
        return self.reservation.end_datetime

    def location(self):
        return self.reservation.location

    def status(self):
        return self.reservation.status

    def description_short(self):
        short_descrip = self.description
        if len(short_descrip) > 30:
            short_descrip = '%s...' % short_descrip[:27]
        return short_descrip

    def is_free(self):
        if self.student_fee == 0 and self.staff_fee == 0 and self.public_fee == 0:
            return True
        return False
    def can_prepay(self):
        if self.prepay:
            return "Yes"
        return "No"
    def access(self):
        if self.is_public:
            return "Public"
        return "Private"

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
    event = models.OneToOneField(Event)
    location = models.ForeignKey(Location)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=30, default=status_const.PENDING)

    def __unicode__(self):
        return self.event.name

class Approval(models.Model):
    approver = models.ForeignKey(User)
    reservation = models.OneToOneField(Reservation)
    date = models.DateTimeField()

    def __unicode__(self):
        return '%s - %s - %s' % (self.approver.username, self.event, self.date)

class Attendance(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    prepaid = models.BooleanField(default=False)
    date_registered = models.DateTimeField()

    def is_prepaid(self):
        if self.prepaid:
            return "Yes"
        return "No"
        
    def __unicode__(self):
        return '%s - %s - %s' % (self.user.username, self.event, self.date_registered)