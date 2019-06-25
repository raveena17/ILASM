from __future__ import unicode_literals
from django.db import models
import datetime
from project_management.users.models import *
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from client_visit_report.emailmanager import send
from project_management.users.models import *
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from netifaces import interfaces, ifaddresses, AF_INET
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator


class Type(models.Model):

    leave_id = models.AutoField(primary_key=True)
    leave_type = models.CharField(max_length=200, blank=False, null=False)
    no_of_days = models.IntegerField()
    current_year = models.IntegerField()
    leave_status = models.CharField(max_length=200, blank=False, null=False)
    organization = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return str(self.leave_type)

    class Meta:
        db_table = 'leave_types'
        verbose_name_plural = "Leave Type"


class LeaveRequest(models.Model):

    request_id = models.AutoField(primary_key=True)
    request_date = models.DateField(null=True, blank=True, auto_now=True)
    empid = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_empid",
        verbose_name='empid',
        null=True,
        db_column='empid')
    leave_from = models.DateField(null=True, blank=True)
    leave_to = models.DateField(null=True, blank=True)
    no_of_days = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True)
    leave_nature = models.ForeignKey(
        Type,
        related_name="%(app_label)s_%(class)s_leave_nature",
        verbose_name='leave_nature',
        null=True,
        db_column='leave_nature')
    leave_reason = models.TextField(max_length=1500, blank=True, null=True)
    approved_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_approved_by",
        verbose_name='approved_by',
        null=True,
        db_column='approved_by')
    approval_status = models.CharField(
        default="Not Yet Approved",
        max_length=200,
        blank=False,
        null=False)
    # date_of_action = models.DateTimeField(null=True, blank=True)
    reject_reason = models.TextField(max_length=1500, blank=True, null=True)
    lop = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return str(self.empid)

    class Meta:
        db_table = 'leave_requests'
        verbose_name_plural = "Leave Request "


class Status(models.Model):

    id = models.AutoField(primary_key=True)
    empid = models.CharField(max_length=200, blank=False, null=False)
    cur_year = models.IntegerField()
    leave_id = models.IntegerField()
    total_leave = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    balance_leave = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.empid)

    class Meta:
        db_table = 'leave_statuses'
        verbose_name_plural = "Leave Status"


class ShortLeaveRequest(models.Model):

    request_id = models.AutoField(primary_key=True)
    leave_date = models.DateField(null=True, blank=True)
    request_date = models.DateField(null=True, blank=True, auto_now=True)
    empid = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_employee",
        verbose_name='employee',
        null=True,
        db_column='empid')
    leave_reason = models.TextField(max_length=1500, blank=True, null=True)
    approved_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_manager",
        verbose_name='manager',
        null=True,
        db_column='approved_by')
    no_of_hours = models.IntegerField(null=True, validators=[MaxValueValidator(2), MinValueValidator(1)])
    approval_status = models.CharField(
        default="Not Yet Approved",
        max_length=200,
        blank=False,
        null=False)
    reject_reason = models.TextField(max_length=1500, blank=True, null=True)

    def __unicode__(self):
        return str(self.empid)

    class Meta:
        db_table = 'shortleave_requests'
        verbose_name_plural = "Short Leave Request "


class LeaveCredit(models.Model):

    id = models.AutoField(primary_key=True)
    empid = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_users",
        verbose_name='users',
        null=True,
        db_column='empid')
    leave_id = models.ForeignKey(
        Type,
        related_name="%(app_label)s_%(class)s_leave_type",
        verbose_name='leave_type',
        null=True,
        db_column='leave_id')
    no_of_days = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True)
    credit_date = models.DateField(null=True, blank=True, auto_now=True)
    cur_year = models.IntegerField()

    def __unicode__(self):
        return str(self.empid)

    class Meta:
        db_table = 'leave_credit'
        verbose_name_plural = "Leave Credit "


class LateAttendance(models.Model):
    empid = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_employeeID",
        null=True,
        db_column='empid')
    month_of_year = models.CharField(max_length=10)
    late_attendance_count = models.IntegerField()

    def __unicode__(self):
        return unicode(self.empid)

    class Meta:
        db_table = "late_Attendance"
        verbose_name_plural = "late_attendances"