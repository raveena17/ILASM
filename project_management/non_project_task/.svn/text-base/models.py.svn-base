"""
    Non project task models.
"""

from django.db import models
from django.contrib.auth.models import User

from project_management.tasks.models import Type
from django.utils.translation import ugettext_lazy as _
#from project_management.users.models import FiveGUser


class NonProjectTask(models.Model):
    non_project_taskID = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 120)
    plannedStartDate = models.DateField(null = True,  blank = True)
    plannedEndDate = models.DateField(null = True,  blank = True)
    notes = models.TextField(null = True, blank = True)
    owner = models.ForeignKey(User)
    cancel = models.BooleanField(default = 'False')
    taskType = models.ForeignKey(Type)

    def __unicode__(self):
        return self.name

    def get_program(self):
        """
            This type of task has no project. Always return None.
        """
        return None

class NonProjectTaskAssignees(models.Model):
    non_project_taskID = models.ForeignKey(NonProjectTask)
    actualstartDate = models.DateField(null = True,  blank = True)
    actualendDate = models.DateField(null = True,  blank = True)
    user = models.ForeignKey(User)
    status = models.CharField(max_length = 50, default = 'Incomplete')

    def __unicode__(self):
        return self.non_project_taskID.name

    class Meta:
        verbose_name = _('Non project Task Assignee')
        verbose_name_plural = _('Non Project Task Assignees')

