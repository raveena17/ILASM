from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

class Announcement(models.Model):
    announcement_ID = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 120)
    content = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(null = True,  blank = True,
                                                default=datetime.now)
    approved_by = models.ForeignKey(User, 
        related_name = '%s(class)s_approved_by', null = True )
    is_approved = models.BooleanField(default = False)
    requested_by = models.ForeignKey(User,
        related_name = '%s(class)s_requested_by', null = True)

    def __unicode__(self):
        return self.title


