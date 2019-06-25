from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

class EquipmentsRequired(models.Model):      
    list_name = models.CharField(max_length = 40)
    
    def __unicode__(self):
        """
            returns model data stored in your database as unicode.
        """
        return self.list_name
    
class ConferenceRoom(models.Model):
    """
        Creating new Conference Room
    """
    name = models.CharField(max_length = 120)
    location = models.CharField(max_length = 40)
    no_of_seats = models.IntegerField(_('No of seats'),
        null=True, blank = True)
    equipments_required = models.ManyToManyField(EquipmentsRequired, verbose_name = _('Equipments'),
                                                 null = True, blank = True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']            

class BookConference(models.Model):
    """
        Creating new Conference Room
    """
    MEETING_TYPES = (('M', _('Meeting')), ('T', _('Training')),
                        ('CM', _('Client Meeting')))
    
    CLIENT_PROVISION = (('S', _('Snacks')), ('B', _('Breakfast')),
                        ('L', _('Lunch')), ('D', _('Dinner')))
    APPROVE_OR_NOT = (('Approve', 'Approve'), ('Reject', 'Reject'))
    
    name_of_meeting = models.CharField(_('Meeting About'), max_length = 100 , null = True, blank = True)
    requested_by = models.ForeignKey(User, verbose_name = _('Requested By'),
        related_name = '%s(class)s_requested_by', null = True)
    requesting_date = models.DateField(_('Requesting Date'),
        null=True, blank = True)
    conference_room = models.ForeignKey(ConferenceRoom, null=True, blank = True,
        verbose_name = _('Conference Room'), related_name = '%s(class)s_conference_room')
    reason_for_room = models.CharField(_('Reason for room'), choices = MEETING_TYPES,
                        max_length = 15)
    meeting_date = models.DateField(_('Meeting Date'))
    from_time = models.TimeField(_('Meeting Start Time'), null=True, blank = True)
    to_time = models.TimeField(_('Meeting End Time'), null=True, blank = True)
    no_of_persons = models.IntegerField(_('No of Persons'),
        null=True, blank = True)
    equipments_required = models.ManyToManyField(EquipmentsRequired, verbose_name = _('Equipments'),
                                                 null = True, blank = True)
    client_food_arrangement = models.CharField(_('Food Needed'), choices = CLIENT_PROVISION,
                        max_length = 15,null = True, blank = True)
    
    approved_by = models.ForeignKey(User, verbose_name = _('Request To'),
        related_name = '%s(class)s_approved_by', null = True )
    approved_date = models.DateField(_('Approved Date'),
        null=True, blank = True)
    attendence_needed = models.BooleanField(_('Attendance'), default = False)
    is_approved = models.BooleanField(_('is_approved'),default = False)
    is_approvedby = models.CharField(_('Approval Type'),
                        max_length = 20, choices = APPROVE_OR_NOT)
    
    
    def __unicode__(self):
        return self.requested_by.username

    class Meta:
        """
            Defines metadata for the model.
        """
        verbose_name = _('Conference Room Booking')
        verbose_name_plural = _('Conference Rooms Booking')
        
class MeetingAttendees(models.Model):
    
    
    conference_name = models.CharField(max_length='20')
    attendees = models.ForeignKey(User, null = True, blank = True)
    
   

    class Meta:
        """
            Defines metadata for the model.
        """
        verbose_name = _('Conference Room Booking')
        verbose_name_plural = _('Conference Rooms Booking')