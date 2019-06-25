from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from project_management.projects.models import Project
#from project_management.users.models import FiveGUser


class Event(models.Model):
    name = models.CharField(_('name'), max_length = 120)
    type = models.CharField(_('event type'), max_length = 120,
                                    null = True, blank = True)
    date = models.DateField(_('date'))
    start_time = models.TimeField(_('start Time'))
    end_time = models.TimeField(_('end Time'))
    venue = models.CharField(_('venue'), max_length = 120,
                                    null = True, blank = True)

    location = models.CharField(_('location'), max_length = 120,
                                    null = True, blank = True)
    project = models.ForeignKey(Project,
                verbose_name=_('project'), null=True, blank=True)
    attendees = models.ManyToManyField(User, verbose_name = _('attendees'))
    description = models.TextField(_('description'), null = True, blank = True)
    creator = models.ForeignKey(User, verbose_name = _('creator'),
        related_name='%s(class)s_development_process')
    cancel = models.BooleanField(_('cancel'), default = False)

    def __unicode__(self):
        return self.name

#class NotificationModule (models.Model):
#	notificationModuleID = models.AutoField(primary_key = True)
#	name = models.CharField(max_length = 250, null = True, blank = True)
#
#	def __unicode__(self):
#		return self.name
#
#class NotificationConfig (models.Model):
#    notificationModule = models.ForeignKey(NotificationModule)
#    program = models.ForeignKey(Project)
#    message = models.TextField (null = True, blank = True)
#    email = models.NullBooleanField(default = 'False', null = True)
#    SMS = models.NullBooleanField(default = 'False', null = True)
#
#    def __unicode__(self):
#        return self.notificationModule.name


#class EventAttendee (models.Model):
#    event = models.ForeignKey(Event)
#    user = models.ForeignKey(User)
#
#    def __unicode__(self):
#        return self.event.name

#class EventOtherAttendee (models.Model):
#    event = models.ForeignKey(Event)
#    otheruser = models.CharField(max_length = 120)
#
#    def __unicode__(self):
#        return self.otheruser
