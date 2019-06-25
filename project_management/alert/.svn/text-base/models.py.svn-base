from django.db import models
from django.contrib.auth.models import User

from project_management.fields import UUIDField

ALERT_TYPE_CHOICES = (('Event', 'Event'), ('Time', 'Time'))
ACTION = (('Create', 'Create'), ('Update', 'Update'), ('Approve', 'Approve'), ('Delete', 'Delete'))


class AlertDataConfiguration(models.Model):
    id = UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    alert_type = models.CharField(max_length=5, choices=ALERT_TYPE_CHOICES)
    action = models.CharField(max_length=10, choices=ACTION)
    days = models.IntegerField(default=0)
    frequency = models.IntegerField(default=1)    
    subject_fields = models.TextField()
    body_fields = models.TextField()
    toemail = models.ManyToManyField(User, related_name='%s(class)alert_email')
    cc = models.ManyToManyField(User, related_name='%s(class)alert_cc')
    bcc = models.ManyToManyField(User, related_name='%s(class)alert_bcc')
    subject = models.TextField()
    body = models.TextField()
    is_email = models.BooleanField(blank=True)
    is_screen = models.BooleanField(blank=True)
    is_active = models.BooleanField(blank=True)
    is_lock = models.BooleanField(blank=True)

    ###audit fields
    created_by = models.ForeignKey(User, null=True, related_name='%s(class)alert_created')
    created_on = models.DateField(blank=True, null=True)
    modified_by = models.ForeignKey(User, null=True, related_name='%s(class)alert_updated')
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'AlertDataConfiguration'

    def __unicode__(self):
        return u'%s:%s' % (self.name, self.alert_type)

    def get_absolute_url(self):
        return "/alert/edit/%s" % self.id


class AlertDataTransaction(models.Model):
    id = UUIDField(primary_key=True)
    alert = models.ForeignKey(AlertDataConfiguration)
    record_id = models.CharField(max_length=255)
    to_id = models.TextField()
    cc_id = models.TextField()
    body = models.TextField()
    subject = models.TextField()
    raised_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(blank=True, default=1)

    class Meta:
        db_table = 'AlertDataTransaction'

    def _unicode_(self):
        return u'%s' % (self.id)


class AlertRaisedTime(models.Model):
    id = UUIDField(primary_key=True)
    alert = models.ForeignKey(AlertDataConfiguration)
    record_id = models.CharField(max_length=255)
    raised_on = models.DateField()

    class Meta:
        db_table = 'AlertRaisedTime'

    def _unicode_(self):
        return u'%s' % (self.id)
    
class Holiday(models.Model):
    id = models.IntegerField(primary_key=True)
    holdate = models.DateTimeField()
    occasion = models.TextField()
    organization = models.TextField()
    
    class Meta:
        db_table = 'holiday'
        
class LeaveRequests(models.Model):
    request_id = models.IntegerField(primary_key=True)
    request_date = models.DateTimeField(null=True, blank=True)
    empid = models.CharField(max_length=90, blank=True)
    leave_from = models.DateTimeField(null=True, blank=True)
    leave_to = models.DateTimeField(null=True, blank=True)
    no_of_days = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    leave_nature = models.IntegerField(null=True, blank=True)
    leave_reason = models.CharField(max_length=600, blank=True)
    approved_by = models.CharField(max_length=150, blank=True)
    approval_status = models.CharField(max_length=150, blank=True)
    reject_reason = models.CharField(max_length=600, blank=True)
    lop = models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)
    class Meta:
        db_table = u'leave_requests'

class Emailomission(models.Model):
    adsslogin = models.CharField(max_length=90, blank=True)
    class Meta:
        db_table = u'emailomission'
