from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from project_management.leave.models import *
from project_management.leave.forms import *
from django.views.generic import RedirectView
from django.views.generic import ListView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from project_management.users.models import *
from django.contrib.auth.models import User, Group
from project_management.users.models import UserProfile, userType
from project_management.users.forms import UserProfileForm, UserForm, MyProfileForm
from datetime import date, timedelta
from project_management.alert.models import *
from django.views.decorators.http import require_http_methods
from django.template import Context
from django.db.models import Sum
from decimal import *
from django.core.mail import EmailMessage
from .utils import get_report_data, make_mail_content
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import settings
from project_management.leave.utils import *
import json
import calendar
import dateutil.relativedelta
from collections import OrderedDict
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from mysql.connector import MySQLConnection, Error



CURRENT_YEAR = settings.CURRENT_YEAR
OTHER_LEAVE_TYPE = settings.OTHER_LEAVE_TYPE


CREATED = 'Leave request submitted successfully.'
SHORT_LEAVE_CREATED = 'Short leave request submitted successfully.'
CANCELLED = 'Leave request cancelled'
SHORT_CANCELLED = 'Short leave request cancelled'
APPROVED = 'Leave request approved.'
REJECTED = 'Leave request rejected.'
SHORT_LEAVE = settings.SHORT_LEAVE_DAYS
SHORT_LEAVE_ALERT = "You have already availed the maximum allowed short leave."
LEAVE_CREDIT = "Leave Credit successfully"
MSG = 'Leave apply valid for current year only'
today = datetime.date.today()


class SubListView(ListView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(SubListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


@require_http_methods(["GET"])
def get_holiday(request):
    today = datetime.date.today()
    user_id = request.user.id
    bucode = UserProfile.objects.get(user_id=user_id).business_unit_code_id
    holydays = Holiday.objects.filter(
        holdate__year=today.year, organization=bucode).values_list('holdate', flat=True)
    print holydays
    return JsonResponse([date.date() for date in holydays], safe=False)


@require_http_methods(["GET"])
def get_previous_leave_balance(request):
    empid = request.GET['empid']
    username = User.objects.get(id=empid)
    leave_type = request.GET['leave_type']
    try:
        _status = Status.objects.get(leave_id=leave_type, empid=username)
        balance = _status.balance_leave
    except Exception as e:
        balance = 0
    return JsonResponse({'leave_bal': balance}, safe=True)


@login_required
def manage_leave(request, id=None, RedirectView=leave_list):
    today = datetime.date.today()
    user = UserProfile.objects.filter(
        user__username=request.user.username,
        user__is_active=True)[0]
    print user
    reporting_senior = user.reporting_senior
    leave = None
    data_set = get_current_status_for_user(request)
    if id:
        leave = get_object_or_404(LeaveRequest, pk=id)
    if request.method == 'POST':
        LeaveForm = LeaveReportForm(request.user, request.POST, instance=leave)
        if LeaveForm.is_valid():
            leave = LeaveForm.save()
            datas = get_report_data(request.user, leave)
            approver = leave.approved_by
            if (leave.leave_from).year == today.year and (leave.leave_to).year == today.year:
                from_date = (leave.leave_from).strftime("%d-%b-%Y")
                to_date = (leave.leave_to).strftime("%d-%b-%Y")
                reason = leave.leave_reason
                no_of_days = leave.no_of_days
                make_mail_content(
                    request.user, leave.leave_nature, from_date, to_date, no_of_days, reason, datas, approver)
                messages.success(request, (CREATED))
            else:
                messages.error(request, (MSG))

        return HttpResponseRedirect(reverse(RedirectView))
    else:
        LeaveForm = LeaveReportForm(request.user, instance=leave)
    return render(request, 'Leave_form.html', {
                  'form': LeaveForm, 'data_set': data_set, 'current_year': settings.CURRENT_YEAR})


@login_required
def manage_shortleave(request, id=None, RedirectView=leave_list):
    shortleave = None
    if id:
        shortleave = get_object_or_404(ShortLeaveRequest, pk=id)
    today = datetime.date.today()
    leave = ShortLeaveRequest.objects.filter(
        empid=request.user,
        request_date__month=today.month,
        request_date__year=today.year).exclude(approval_status="Cancelled").exclude(approval_status="Rejected")

    if request.method == 'POST':
        ShortLeaveForm = ShortLeaveRequestForm(
            request.user, request.POST, instance=shortleave)
        if ShortLeaveForm.is_valid():
            ShortLeaveForm.request_date = datetime.date.today().strftime("%d-%b-%Y")
            leave = ShortLeaveForm.save()
            approver = leave.approved_by
            if (leave.leave_date).year == today.year:
                from_date = (leave.leave_date).strftime("%d-%b-%Y")
                reason = leave.leave_reason
                no_of_days = leave.no_of_hours
                subject = "{0} has applied ShortLeave" .format(
                    request.user.first_name)
                body = "Hello {0},\n\n\nI have applied for {1} leave on {2} (Total hours: {3}).\n\nReason: {4}\n\n\nI kindly request you to approve the same.\n\n\nRegrads,\n{5}\n{6} " .format(
                    approver.first_name + ' ' + approver.last_name, "Short", from_date, no_of_days, reason, request.user.first_name, ShortLeaveForm.request_date)
                email = EmailMessage(
                    subject, body, request.user.email, to=[approver.email])
                email.send()
                messages.success(request, (SHORT_LEAVE_CREATED))
            else:
                messages.error(request, (MSG))
        return HttpResponseRedirect(reverse(RedirectView))
    else:
        if not id:
            if leave:
                count_shortleave_list = leave.count()
                if SHORT_LEAVE <= int(count_shortleave_list):
                    messages.error(request, (SHORT_LEAVE_ALERT))
                    return HttpResponseRedirect(reverse(RedirectView))

            ShortLeaveForm = ShortLeaveRequestForm(
                request.user, instance=shortleave)
        ShortLeaveForm = ShortLeaveRequestForm(
            request.user, instance=shortleave)
    return render(request, 'Short_leave_form.html', {
        'short_leave_form': ShortLeaveForm, 'current_year': settings.CURRENT_YEAR})


@require_http_methods(["GET"])
def get_lop(request):
    applied = 0
    _type = Type.objects.get(leave_id=request.GET["leave_nature"])
    if _type.leave_type == "LOP":
        return JsonResponse({'lop': request.GET["no_of_days"]}, safe=True)
    else:
        status = Status.objects.get(
            leave_id=request.GET["leave_nature"],
            empid=request.user)
        leave = LeaveRequest.objects.filter(
            leave_nature__leave_id=status.leave_id,
            empid=request.user,
            request_date__year=today.year,
            approval_status="Not Yet Approved"
        )
        if leave:
            applied = leave.aggregate(Sum('no_of_days'))['no_of_days__sum']
        lop = 0
        if status.balance_leave > applied:
            lop = (status.balance_leave - applied) - \
                Decimal(request.GET["no_of_days"])
        else:
            lop = -Decimal(request.GET["no_of_days"])
        if lop < 0:
            return JsonResponse({'lop': abs(lop)}, safe=True)
        else:
            return JsonResponse({'lop': 0}, safe=True)


@login_required
def cancel_leave(request):
    """Cancelled - Changed by status and return added your leave"""
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        try:
            leave_ids = request.POST.getlist('leave_pk')
            leave_request = LeaveRequest.objects.filter(pk__in=leave_ids)[0]
            if leave_request.approval_status == "Not Yet Approved":
                _leave_type = leave_request.leave_nature

                _type_id = Type.objects.get(
                    current_year=today.year,
                    leave_type=_leave_type).leave_type
                if _type_id == 'LOP' or 'Compoff' or 'Maternity':
                    leave_request.approval_status = "Cancelled"
                    leave_request.save()
                    messages.success(request, (CANCELLED))
                else:
                    _type_id = Type.objects.get(
                        current_year=today.year,
                        leave_type=_leave_type).leave_id
                    _status = Status.objects.get(
                        empid=request.user,
                        cur_year=today.year,
                        leave_id=_type_id)

                    if leave_request.lop == 0:
                        leave_request.no_of_days = leave_request.no_of_days
                    else:
                        if leave_request.no_of_days == leave_request.lop:
                            lop = 0
                        else:
                            _lop = abs(leave_request.lop)
                            lop = _lop
                    leave_request.no_of_days = abs(leave_request.no_of_days)
                    leave_request.lop = 0
                    leave_request.approval_status = "Cancelled"
                    leave_request.save()
                    messages.success(request, (CANCELLED))
            elif leave_request.approval_status == "Approved":
                messages.error(request, ("Approved record can't be cancelled"))
            elif leave_request.approval_status == "Rejected":
                messages.error(request, ("Rejected record can't be cancelled"))
        except Exception as e:
            return HttpResponseRedirect(reverse(leave_list))
    return HttpResponseRedirect(reverse(leave_list))


def leave_approval_status(request, id, status):
    try:
        if id:
            leave = get_object_or_404(LeaveRequest, pk=id)
    except LeaveRequest.DoesNotExist:
        return HttpResponse('Not Found', status=404)

    user1 = User.objects.get(username=leave.empid)
    userid = user1.id
    bucode = UserProfile.objects.get(user_id=userid).business_unit_code
    bu_id = bu_id=BusinessUnit.objects.get(name=bucode).id
    now = datetime.datetime.now()
    
    if request.method == 'GET':
        if status == 'approve':
            # Reduce the leave
            if leave.approval_status == "Not Yet Approved":
                _leave_type = leave.leave_nature
                leave_no_of_days = leave.no_of_days

                type = Type.objects.get(
                    current_year=today.year,
                    leave_type=_leave_type,organization=bu_id).leave_type

                if type in OTHER_LEAVE_TYPE:
                    leave.approval_status = "Approved"
                else:
                    _type_id = Type.objects.get(
                        current_year=today.year, leave_type=_leave_type,organization=bu_id).leave_id
                    _status = Status.objects.get(
                        empid=leave.empid, cur_year=today.year, leave_id=_type_id)

                    _no_of_days = leave_no_of_days - leave.lop
                    no_of_days = abs(_no_of_days)
                    balance_leave = _status.balance_leave - no_of_days
                    _status.balance_leave = balance_leave
                    leave.approval_status = "Approved"
                    _status.save()

                leave.save(
                    update_fields=[
                        'approval_status'])
                subject = 'Leave Approved'
                message = "Dear {0},\n\nLeave from {1} to {2} ('{3}' days) has been approved on {4} .\n\nBest Regrads,\n{5}" .format(
                    user1.first_name,
                    leave.leave_from.strftime("%d-%b-%Y"),
                    leave.leave_to.strftime("%d-%b-%Y"),
                    leave.no_of_days,
                    now.strftime("%d-%b-%Y"),
                    leave.approved_by.first_name)

            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [
                    user1.email], fail_silently=False)
            messages.success(request, (APPROVED))
        return HttpResponseRedirect(reverse(get_leave_approval_list))



def leave_reject_status(request, id, status):
    try:
        if id:
            leave = get_object_or_404(LeaveRequest, pk=id)
    except LeaveRequest.DoesNotExist:
        return HttpResponse('Not Found', status=404)

    user1 = User.objects.get(username=leave.empid)
    userid = user1.id
    bucode = UserProfile.objects.get(user_id=userid).business_unit_code
    bu_id = bu_id=BusinessUnit.objects.get(name=bucode).id
    now = datetime.datetime.now()

    if request.method == 'POST':
        if status == 'reject':
            if leave.approval_status == "Not Yet Approved":
                _leave_type = leave.leave_nature
                _type_id = Type.objects.get(
                    current_year=today.year,
                    leave_type=_leave_type,organization=bu_id).leave_id
                _status = Status.objects.get(
                    empid=user1,
                    cur_year=today.year,
                    leave_id=_type_id)

                if leave.lop == 0:
                    leave.no_of_days = leave.no_of_days
                else:
                    if leave.no_of_days == leave.lop:
                        lop = 0
                    else:
                        _lop = abs(leave.lop)
                        lop = _lop

                leave.no_of_days = abs(leave.no_of_days)
                leave.lop = 0
                leave.approval_status = 'Rejected'
                leave.reject_reason = request.POST.get('reason')
                leave.save(
                    update_fields=[
                        'approval_status',
                        'reject_reason'])

            subject = 'Approve Rejected to leave'
            message = "Dear {0},\n\nLeave from {1} to {2} ('{3}' days) has been rejected on {4}.\n\nReason : {5}.\n\n\nRegrads,\n{6}" .format(
                user1.first_name,
                leave.leave_from.strftime("%d-%b-%Y"),
                leave.leave_to.strftime("%d-%b-%Y"),
                leave.no_of_days,
                now.strftime("%d-%b-%Y"),
                leave.reject_reason,
                leave.approved_by.first_name)
            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [
                    user1.email], fail_silently=False)
            messages.success(request, (REJECTED))
            return JsonResponse("Rejected", safe=False)


@login_required
def cancel_shortleave(request):
    """Cancelled - Changed by status and return added your shortleave"""
    if request.method == 'POST':
        try:
            leave_ids = request.POST.getlist('shortleave_pk')
            shortleave_request = ShortLeaveRequest.objects.filter(pk__in=leave_ids)[
                0]
            if shortleave_request.approval_status == "Not Yet Approved":
                shortleave_request.approval_status = "Cancelled"
                shortleave_request.save()
                messages.success(request, (SHORT_CANCELLED))
            elif shortleave_request.approval_status == "Approved":
                messages.error(request, ("Approved record can't be cancelled"))
            elif shortleave_request.approval_status == "Rejected":
                messages.error(request, ("Rejected record can't be cancelled"))
        except Exception as e:
            return HttpResponseRedirect(reverse(leave_list))
    return HttpResponseRedirect(reverse(leave_list))

# short leave approve and reject action


def shortleave_approval_status(request, id, status):
    try:
        if id:
            leave = get_object_or_404(ShortLeaveRequest, pk=id)
    except ShortLeaveRequest.DoesNotExist:
        return HttpResponse('Not Found', status=404)

    user1 = User.objects.get(username=leave.empid)
    now = datetime.datetime.now()
    if request.method == 'GET':
        if status == 'approve':
            if leave.approval_status == "Not Yet Approved":
                leave.approval_status = "Approved"
                leave.save(
                    update_fields=[
                        'approval_status'])
                subject = 'ShortLeave Approved'
                message = "Dear {0},\n\nShortLeave from {1} ('{2}' hours) has been approved on {3} .\n\nBest Regards,\n{4}" .format(
                    user1.first_name,
                    leave.leave_date.strftime("%d-%b-%Y"),
                    leave.no_of_hours,
                    now.strftime("%d-%b-%Y"),
                    leave.approved_by.first_name)

            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [
                    user1.email], fail_silently=False)
            messages.success(request, ("Short" + APPROVED))
            return HttpResponseRedirect(reverse(get_leave_approval_list))

    else:
        if request.method == 'POST':
            if status == 'reject':
                if leave.approval_status == "Not Yet Approved":
                    leave.approval_status = 'Rejected'
                    leave.reject_reason = request.POST.get('reason')
                    leave.save(
                        update_fields=[
                            'approval_status',
                            'reject_reason'])

                subject = 'Approve Rejected to ShortLeave'
                message = "Dear {0},\n\nShortLeave from {1} ('{2}' hours) has been rejected on {3}.\n\nReason : {4}.\n\n\nRegards,\n{5}" .format(
                    user1.first_name,
                    leave.leave_date.strftime("%d-%b-%Y"),
                    leave.no_of_hours,
                    now.strftime("%d-%b-%Y"),
                    leave.reject_reason,
                    leave.approved_by.first_name)
                send_mail(
                    subject, message, settings.EMAIL_HOST_USER, [
                        user1.email], fail_silently=False)
                messages.success(request, ("Short" + REJECTED))
                return JsonResponse("Rejected", safe=False)


def leave_credit(request, id=None, RedirectView=leave_credit_list):
    leave_credit = None
    if id:
        leave_credit = get_object_or_404(LeaveCredit, pk=id)

    if request.method == 'POST':
        CreditForm = LeaveCreditForm(
            request.user, request.POST, instance=leave_credit)
        if CreditForm.is_valid():
            leave_credit = CreditForm.save()
            empid = leave_credit.empid
            leave_id = leave_credit.leave_id.leave_id
            cur_year = leave_credit.cur_year
            username = UserProfile.objects.get(user_id=empid)
            leave_status = Status.objects.get(
                empid=username, cur_year=cur_year, leave_id=leave_id)
            current_balance = leave_status.balance_leave
            balance_leave = current_balance + leave_credit.no_of_days
            leave_status.balance_leave = balance_leave
            leave_status.save()
            messages.success(request, (LEAVE_CREDIT))
        return HttpResponseRedirect(reverse(RedirectView))
    else:
        CreditForm = LeaveCreditForm(request.user, instance=leave_credit)
    return render(request, 'Leave_credit.html', {
        'credit_form': CreditForm})


def generate_leave(request):

    report_form = ReportForm()
    return render(request, 'generate_leave.html', {'report_form': report_form})




class LateListView(ListView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(LateListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


def fetch_lateAttendanceCount_sp(employee):
    """Get datas in mysql store procedure"""

    
    host = settings.DATABASES['default']['HOST']
    database = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    try:
        mySQL_conn = mysql.connector.connect(host=host,database=database,user=user,password=password)
        # mySQL_conn = mysql.connector.connect(host='192.168.1.72',database='mindshare_test',user='mind',password='p@ssw0rd')
        cursor = mySQL_conn.cursor()
        args = (employee)
        cursor.callproc('GetLateAttendance', [args])

        for result in cursor.stored_results():
            column_names_list = [x[0] for x in result.description]
            result_dicts = [dict(zip(column_names_list, row))
                            for row in result.fetchall()]
        return result_dicts

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

    finally:
        if (mySQL_conn.is_connected()):
            cursor.close()
            mySQL_conn.close()
            print("connection is closed")



def get_employees(request,status=None, id=None):
    current_month = get_current_month(request)

    if status and id != None:
        month = status+" "+id
        print month
    else:
        month = current_month


    if request.method == "POST":
        emp_datas = request.POST
        month_year = request.POST['monthList']

        previous_record = LateAttendance.objects.filter(month_of_year = month_year)
        previous_record.delete()
        for user_id, late_count in emp_datas.iteritems():
            if user_id not in ['save','monthList','csrfmiddlewaretoken']:
                emp_id = User.objects.get(id=user_id)
                late_form = LateAttendance.objects.create(
                empid=emp_id,
                late_attendance_count = late_count,
                month_of_year = month_year)  
                late_form.save()
                if month_year == month:
                    employee_list= fetch_lateAttendanceCount_sp(month)
                else:
                    employee_list= fetch_lateAttendanceCount_sp(month_year)

    else:
        employee_list = fetch_lateAttendanceCount_sp(month)
    return render(request,'late_list.html', {'employee_list' : employee_list, 'Selectedmonth':month, 'currentMonth':current_month})


def get_current_month(request):
    today = datetime.datetime.today()
    year = str(today.year)
    month = today.month
    month_name = calendar.month_abbr[month]
    month_str = str(month_name)
    month_yr = month_str+' '+year
    return month_yr