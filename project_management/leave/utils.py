import datetime
from django.core.mail import send_mail
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.db.models import Sum
from .models import *
from .views import *
import settings
from project_management.leave.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import RedirectView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import itertools

# from mysql.connector import MySQLConnection, Error, errorcode
# from python_mysql_dbconfig import read_db_config

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import settings
from mysql.connector import MySQLConnection, Error

# import mysql.connector
# from mysql.connector import Error
# from mysql.connector import errorcode
# import settings


HRDESK = settings.REMINDER_FOR_HRDESK
today = datetime.date.today()


class SubListView(ListView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(SubListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


def get_current_status_for_user(request, _apply=None):
    list_data = []
    status_list = Status.objects.filter(
        empid=request.user, cur_year=today.year)
    for status in status_list:
        _type = Type.objects.get(
            current_year=today.year,
            leave_id=status.leave_id)
        leave = LeaveRequest.objects.filter(
            leave_nature__leave_id=status.leave_id,
            empid=request.user,
            request_date__year=today.year,
            approval_status="Not Yet Approved"
        )
        if leave:
            no_of_days = leave.aggregate(Sum('no_of_days'))['no_of_days__sum']
            balance = status.balance_leave
            if _apply is None:
                balance = status.balance_leave - no_of_days
            else:
                balance = status.balance_leave - (no_of_days + _apply)
            list_data.append({
                'leave_type': _type.leave_type,
                'current_balence': status.balance_leave,
                'appied_for': no_of_days,
                'balence_after_approval': balance if balance > 0 else 0,
                'lop': 0 if balance > 0 else abs(balance)
            })
        else:
            balance = 0
            list_data.append({
                'leave_type': _type.leave_type,
                'current_balence': status.balance_leave,
                'appied_for': balance,
                'balence_after_approval': status.balance_leave,
                'lop': balance
            })
    return list_data


def get_role(user):
    try:
        role = User.objects.get(id=user.id).groups.all()
        return role
    except Exception as e:
        role = None
        return role


@login_required
def leave_list(request, page=1):
    requestlist = LeaveRequest.objects.filter(
        empid=request.user, request_date__year=today.year).order_by('-request_id').exclude(approval_status="Cancelled")
    short_leave_requestlist = ShortLeaveRequest.objects.filter(
        empid=request.user,
        request_date__year=today.year).order_by('-request_id').exclude(approval_status="Cancelled")
    requestlist = Paginator(
        requestlist,
        10).page(
        request.GET.get(
            'request_page',
            1))
    short_leave_requestlist = Paginator(
        short_leave_requestlist,
        10).page(
        request.GET.get(
            'short_leave_request_page',
            1))
    data_set = get_current_status_for_user(request)
    return render(request, 'Leave_list.html', {
                  'requestlist': requestlist, 'short_leave_requestlist': short_leave_requestlist, 'data_set': data_set})


def leave_record_list(request, page=1):
    role = get_role(request.user)
    if 'Corporate Admin' in role.values_list('name', flat=True):
        requestlist = LeaveRequest.objects.filter(
            request_date__year=today.year).order_by('-request_id')
        short_leave_requestlist = ShortLeaveRequest.objects.filter(
            request_date__year=today.year).order_by('-request_id')

    requestlist = Paginator(
        requestlist,
        20).page(
        request.GET.get(
            'request_page',
            1))
    short_leave_requestlist = Paginator(
        short_leave_requestlist, 20).page(
        request.GET.get(
            'short_leave_requestlist_page', 1))
    return render(request, 'leave_record.html', {
                  'requestlist': requestlist, 'short_leave_requestlist': short_leave_requestlist})


def leave_credit_list(request, page=1):
    creditlist = LeaveCredit.objects.all().order_by('-id')
    creditlist = Paginator(
        creditlist,
        20).page(
        request.GET.get(
            'credit_page',
            1))
    return render(request, 'Leave_credit_list.html',
                  {'creditlist': creditlist})


def get_leave_approval_list(request, page=1):
    approvallist = LeaveRequest.objects.filter(
        approved_by=request.user,
        request_date__year=today.year,
        approval_status="Not Yet Approved").order_by('-request_id')
    short_leave_approvallist = ShortLeaveRequest.objects.filter(
        approved_by=request.user,
        request_date__year=today.year,
        approval_status="Not Yet Approved").order_by('-request_id')

    approvallist = Paginator(
        approvallist,
        10).page(
        request.GET.get(
            'approve_page',
            1))
    short_leave_approvallist = Paginator(
        short_leave_approvallist,
        10).page(
        request.GET.get(
            'short_leave_approve_page',
            1))
    data_set = get_current_status_for_user(request)
    return render(request, 'Leave_request_list.html', {
                  'approvallist': approvallist, 'short_leave_approvallist': short_leave_approvallist})


def get_report_data(user, _leave):
    datas = []
    today = datetime.date.today()
    user_status_list = Status.objects.filter(
        empid=user.username, cur_year=today.year)
    for status in user_status_list:
        data = {}
        _type = Type.objects.get(
            current_year=today.year,
            leave_id=status.leave_id)
        no_of_days = 0
        leave = LeaveRequest.objects.filter(
            leave_nature__leave_id=status.leave_id,
            empid=user,
            request_date__year=today.year,
            approval_status="Not Yet Approved"
        )
        if leave:
            no_of_days = leave.aggregate(Sum('no_of_days'))['no_of_days__sum']
        if _type == _leave.leave_nature:
            data = {
                'leave_type': _leave.leave_nature.leave_type,
                'current_balence': status.balance_leave,
                'appied_for': _leave.no_of_days,
                'balence_after_approval': status.balance_leave - _leave.no_of_days
            }
            if _leave.leave_nature.leave_type == "LOP":
                data["lop"] = _leave.no_of_days
                data["balence_after_approval"] = 0
        else:
            data = {
                'leave_type': _type.leave_type,
                'current_balence': status.balance_leave,
                'appied_for': 0,
                'balence_after_approval': 0,
            }
        datas.append(data)
    return datas


@require_http_methods(["GET"])
def get_reports(request):
    page = request.GET.get('page', 1)
    if request.GET['employee'] == 'all':
        if request.GET['status'] == "Pending":
            leave_requests = LeaveRequest.objects.filter(
                leave_from__year=request.GET['year'],
                leave_from__month=request.GET['month'],
                approval_status="Not Yet Approved")
            json_res = convert_json(leave_requests)

        else:
            leave_requests = LeaveRequest.objects.filter(
                leave_from__year=request.GET['year'],
                leave_from__month=request.GET['month'],
                approval_status=request.GET['status'])
            json_res = convert_json(leave_requests)
    else:
        if request.GET['status'] == "Pending":
            leave_requests = LeaveRequest.objects.filter(
                leave_from__year=request.GET['year'],
                leave_from__month=request.GET['month'],
                approval_status="Not Yet Approved",
                empid=User.objects.get(
                    id=int(
                        request.GET['employee'])))
            json_res = convert_json(leave_requests)
        else:
            leave_requests = LeaveRequest.objects.filter(
                leave_from__year=request.GET['year'],
                leave_from__month=request.GET['month'],
                approval_status=request.GET['status'],
                empid=User.objects.get(
                    id=int(
                        request.GET['employee'])))
            json_res = convert_json(leave_requests)
    return HttpResponse(json.dumps(json_res), content_type='application/json')


@require_http_methods(["GET"])
def get_short_leave_reports(request):

    if request.GET['employee'] == 'all':
        if request.GET['status'] == "Pending":
            leave_requests = ShortLeaveRequest.objects.filter(
                leave_date__year=request.GET['year'],
                leave_date__month=request.GET['month'],
                approval_status="Not Yet Approved")
            json_res = convert_short_leave_to_json(leave_requests)

        else:
            leave_requests = ShortLeaveRequest.objects.filter(
                leave_date__year=request.GET['year'],
                leave_date__month=request.GET['month'],
                approval_status=request.GET['status'])
            json_res = convert_short_leave_to_json(leave_requests)
    else:
        if request.GET['status'] == "Pending":
            leave_requests = ShortLeaveRequest.objects.filter(
                leave_date__year=request.GET['year'],
                leave_date__month=request.GET['month'],
                approval_status="Not Yet Approved",
                empid=User.objects.get(
                    id=int(
                        request.GET['employee'])))
            json_res = convert_short_leave_to_json(leave_requests)
        else:
            leave_requests = ShortLeaveRequest.objects.filter(
                leave_date__year=request.GET['year'],
                leave_date__month=request.GET['month'],
                approval_status=request.GET['status'],
                empid=User.objects.get(
                    id=int(
                        request.GET['employee'])))
            json_res = convert_short_leave_to_json(leave_requests)
    return HttpResponse(json.dumps(json_res), content_type='application/json')


def convert_json(leave_requests):
    json_res = []
    for record in leave_requests:
        json_obj = dict(
            employee=record.empid.username,
            from_date=record.leave_from.strftime('%d-%b-%Y'),
            to_date=record.leave_to.strftime('%d-%b-%Y'),
            type=record.leave_nature.leave_type,
            no_of_days=int(record.no_of_days),
            lop=int(record.lop),
            status=record.approval_status
        )
        json_res.append(json_obj)
    return json_res


def convert_short_leave_to_json(leave_requests):
    json_res = []
    for record in leave_requests:
        json_obj = dict(
            employee=record.empid.username,
            from_date=record.leave_date.strftime('%d-%b-%Y'),
            no_of_hours=int(record.no_of_hours),
            status=record.approval_status
        )
        json_res.append(json_obj)
    return json_res


def paginate_leave_requests(leave_requests, page):
    paginator = Paginator(leave_requests, 10)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
    return requests


def make_mail_content(user, select_leave, from_date,
                      to_date, no_of_days, reason, datas, approver):
    now = datetime.datetime.now().strftime("%d-%b-%Y")
    sender = user.email
    recipient = [approver.email]
    template_name = 'Leave_Reminder.html'
    subject = user.first_name + ' ' + 'has applied leave'
    content = make_html_content(template_name, {
        'reporting_senior': approver.first_name + ' ' + approver.last_name,
        'from_date': from_date,
        'type': select_leave,
        'to_date': to_date,
        'no_of_days': no_of_days,
        'reason': reason,
        'datas': datas,
        'user': user.first_name,
        'now': now
    })
    email = EmailMultiAlternatives(
        subject, content, sender, recipient, cc=HRDESK)
    email.attach_alternative(content, "text/html")
    email.send()


def make_html_content(template_name, context):
    template = get_template(template_name)
    html_content = template.render(context)
    return html_content


@login_required
def leave_consolidated(request, page=1):
    active_user = User.objects.filter(is_active=1)
    consolidated_list = []
    for user in active_user:
        emp_list = Status.objects.filter(cur_year=today.year, empid=user)
        adict_list = {}
        data_list = []
        for emp in emp_list:
            adict = {}
            list = []
            leavetype = Type.objects.filter(
                leave_id=emp.leave_id, current_year=today.year)
            leavetype = leavetype[0].leave_type
            if leavetype == 'Earned':
                username = emp.empid
                adict.update(
                    {'username': username, 'earned': emp.balance_leave})
            elif leavetype == 'Personal':
                adict.update({'personal': emp.balance_leave})
            elif leavetype == 'Sick':
                adict.update({'sick': emp.balance_leave})
            else:
                balance_leave = 0
            data_list.append(adict)

        for dictionary in data_list:
            for key in dictionary:
                adict_list[key] = dictionary[key]

        if adict_list != {}:
            consolidated_list.append(adict_list)

    consolidated_list = Paginator(
        consolidated_list, 25).page(
        request.GET.get(
            'consolidate_page', 1))
    return render(request, 'Leave_consolidated.html', {
                  'consolidated_list': consolidated_list})


def fetch_reconciliation_sp(request, employee):
    """Get datas in mysql store procedure"""

    
    host = settings.DATABASES['default']['HOST']
    database = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    try:
        mySQL_conn = mysql.connector.connect(host=host,database=database,user=user,password=password)
        # mySQL_conn = mysql.connector.connect(host='192.168.1.72',database='mindshare_test',user='mind',password='p@ssw0rd')
        cursor = mySQL_conn.cursor()
        args = [settings.CURRENT_YEAR, employee]
        cursor.callproc('LeaveReconciliation_SP', args)

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


# def fetch_reconciliation_sp(request, employee):
#     """Get datas in mysql store procedure"""

#     # host = settings.DATABASES['default']['HOST']
#     # database = settings.DATABASES['default']['NAME']
#     # user = settings.DATABASES['default']['USER']
#     # password = settings.DATABASES['default']['PASSWORD']

#     host = settings.DATABASES['default']['HOST']
#     database = settings.DATABASES['default']['NAME']
#     user = settings.DATABASES['default']['USER']
#     password = settings.DATABASES['default']['PASSWORD']

#     import pdb;pdb.set_trace()
#     conn = MySQLConnection(host=host,
#          database=database,
#          user=user,
#          password=password)
#     try:
        
#         cursor = conn.cursor()
#         args = [settings.CURRENT_YEAR, employee]
#         cursor.callproc('LeaveReconciliation_SP', args)
        
#         for result in cursor.stored_results():
#             column_names_list = [x[0] for x in result.description]
#             result_dicts = [dict(zip(column_names_list, row))
#             for row in result.fetchall()]
#         return result_dicts

#     except Error as e:
#         print("Failed to execute stored procedure: {}".format(error))

#     finally:
#         cursor.close()
#         conn.close()

def leave_reconciliation(request):

    if request.method == 'GET':
        reconciliation_form = ReconciliationForm()
    else:
        user_id = request.POST['username']
        employee = User.objects.get(id=user_id).username
        fetch_reconciliation = fetch_reconciliation_sp(request, employee)

        fetch_reconciliation = Paginator(
            fetch_reconciliation, 50).page(
            request.GET.get(
                'reconciliation_page', 1))
        print fetch_reconciliation
        return render(request, 'Leave_reconciliation.html', {
                      'reconciliation_data': fetch_reconciliation})

    return render(request, 'Leave_reconciliation.html', {
                  'reconciliation_form': reconciliation_form})






# def leave_reconciliation(request):

#     # import pdb;pdb.set_trace()
#     # if request.method == 'GET':
#     reconciliation_form = ReconciliationForm()
#     # else:
#         # user_id = request.POST['username']
#         # employee = User.objects.get(id=user_id).username
#         # fetch_reconciliation = fetch_reconciliation_sp(request, employee)

#         # fetch_reconciliation = Paginator(
#         #     fetch_reconciliation, 50).page(
#         #     request.GET.get(
#         #         'reconciliation_page', 1))
#         # print fetch_reconciliation
#         # return render(request, 'Leave_reconciliation.html', {
#         #               'reconciliation_data': fetch_reconciliation})

#     return render(request, 'Leave_reconciliation.html', {
#                   'reconciliation_form': reconciliation_form})


# def get_reconciliation_data(request):
#     # if request.method == 'GET':
#     import pdb;pdb.set_trace()
#     user_id = request.POST['username']
#     employee = User.objects.get(id=user_id).username
#     fetch_reconciliation = fetch_reconciliation_sp(request, employee)

#     fetch_reconciliation = Paginator(
#         fetch_reconciliation, 50).page(
#         request.GET.get(
#             'reconciliation_page', 1))
#     print fetch_reconciliation
#     return render(request, 'Leave_reconciliation.html', {
#                   'reconciliation_data': fetch_reconciliation})












































# def fetch_reconciliation_sp(request, employee):

#     """Get datas in mysql store procedure"""

#     host = settings.DATABASES['default']['HOST']
#     database = settings.DATABASES['default']['NAME']
#     user = settings.DATABASES['default']['USER']
#     password = settings.DATABASES['default']['PASSWORD']
#     try:
#         mySQL_conn = mysql.connector.connect(host=host,
#                                        database=database,
#                                        user=user,
#                                        password=password)
#         cursor = mySQL_conn.cursor()
#         args =[settings.CURRENT_YEAR, employee]

#         cursor.callproc('LeaveReconciliation_SP', args)
#         for result in cursor.stored_results():
#             value_list = result.fetchall()
#         return values_list

#     except mysql.connector.Error as error:
#         print("Failed to execute stored procedure: {}".format(error))

#     finally:
#         if (mySQL_conn.is_connected()):
#             cursor.close()
#             mySQL_conn.close()
#             print("connection is closed")


# def leave_reconciliation(request):
#     leave_data=[]
#     if request.method == 'GET':
#         reconciliation_form = ReconciliationForm()
#     else:
#         user_id = request.POST['username']
#         user = User.objects.get(id=user_id).username
#         leave_list = LeaveRequest.objects.filter(empid=user_id,request_date__year=today.year,approval_status='Approved')
#         credit_list = LeaveCredit.objects.filter(empid=user_id, cur_year = today.year)

#         for leave in leave_list:
#             leave_dict ={
#                         'username':user,
#                         'from_date': leave.leave_from.strftime('%d-%m-%Y'),
#                         'to_date': leave.leave_to.strftime('%d-%m-%Y'),
#                         'approval_status': leave.approval_status
#                         }

#             leave_type = leave.leave_nature
#             leave_days = leave.no_of_days
#             user_leave = get_user_leave(user)
#             print user_leave

#             leave_bal = get_applied_leave_balance(leave_type, leave_days, leave_dict, user_leave)
#             print leave_bal


#             leave_data.append(leave_bal)

#         return render(request, 'Leave_reconciliation.html',{'reconciliation_data':leave_data})
# return render(request,
# 'Leave_reconciliation.html',{'reconciliation_form':reconciliation_form})


# def get_user_leave(user):
#     user_dict ={}
#     emp_list = Status.objects.filter(cur_year=today.year, empid=user)
#     data_list = []
#     for emp in emp_list:
#         adict={}
#         list = []
#         leavetype = Type.objects.filter(leave_id=emp.leave_id, current_year=today.year)
#         leavetype = leavetype[0].leave_type
#         if leavetype == 'Earned':
#             username = emp.empid
#             adict.update({'cearned':emp.total_leave})
#         elif leavetype == 'Personal':
#             adict.update({'cpersonal':emp.total_leave})
#         elif leavetype == 'Sick':
#             adict.update({'csick':emp.total_leave})
#         else:
#             total_leave = 0
#         print adict
#         data_list.append(adict)

#     return data_list


# def get_applied_leave_balance(leave_type, leave_days, leave_dict,
# user_leave):

#     import pdb;pdb.set_trace()

#     leave_type = leave_type.leave_type
#     days = '0.00'
#     print user_leave

#     leavelist = []
#     for leave in user_leave:
#         for key in leave:
#             if key == 'csick':
#                 csick = leave[key]
#                 print csick
#             elif key == 'cpersonal':
#                 cpersonal = leave[key]
#             else:
#                 cearned = leave[key]

#     import pdb;pdb.set_trace()


#     if leave_type == 'Sick':
#         bal_days = csick-leave_days
#         leave_dict.update({'sick':leave_days})
#         leave_dict.update({'asick':bal_days})
#         csick = bal_days

#     else:
#         leave_dict.update({'sick':days})
#         leave_dict.update({'csick':csick})


#     if leave_type == 'Personal':
#         bal_days = cpersonal-leave_days
#         leave_dict.update({'personal':leave_days})
#         leave_dict.update({'cpersonal':bal_days})
#     else:
#         leave_dict.update({'personal':days})
#         leave_dict.update({'cpersonal':cpersonal})


#     if leave_type == 'Earned':
#         bal_days = cearned-leave_days
#         leave_dict.update({'earned':leave_days})
#         leave_dict.update({'cearned':bal_days})
#     else:
#         leave_dict.update({'earned':days})
#         leave_dict.update({'cearned':cearned})


#     if leave_type == 'Compoff':
#         leave_dict.update({'compoff':leave_days})
#     else:
#         leave_dict.update({'compoff':days})

#     if leave_type == 'LOP':
#         leave_dict.update({'lop':leave_days})
#     else:
#         leave_dict.update({'lop':days})

#     return leave_dict
