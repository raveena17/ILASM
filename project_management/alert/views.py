import sys
import datetime
import csv
import os
import xlwt
import csv

from django.conf import settings
#from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db.models import Q
from functools import reduce
# from django.utils import simplejson
try:
    import django.utils.simplejson
except BaseException:
    import json as simplejson

from dateutil.relativedelta import *
from dateutil.rrule import rrule, DAILY
from django.db.models import Sum
from xlwt import Workbook, easyxf
from django.contrib.auth.decorators import login_required
try:
    from django.core.servers.basehttp import FileWrapper
except BaseException:
    from wsgiref.util import FileWrapper

from django.contrib.auth.models import User
from project_management.alert.models import *
from project_management.projects.models import *
from project_management.announcements.models import *
from project_management.reimbursement.models import *
from project_management.projectbudget.models import *
from project_management.users.models import *
from project_management.timesheet.models import *
from project_management.Utility import EmailWithCC
from django.contrib.auth.models import User
from django.shortcuts import render


MODULE = 'Alert'
ERROR_MESSAGE = 'ERROR : %s \nLINE NUMBER : %s'


def get_perms(request):

    alert_owners = User.objects.filter(
        groups__name__icontains='Alertmail_permission',
        is_active=True).values('id')
    return alert_owners


def alert_generate(
        request,
        module_name,
        alert_id,
        record_id,
        to_id=[],
        cc_id=[],
        comments=''):
    '''
    Event alerts
    '''
    try:
        total_to_email_list = []
        total_cc_email_list = []
        to_id_list = []
        subject_fields_lsit = []
        body_fields_list = []
        alert_configuration = AlertDataConfiguration.objects.get(pk=alert_id)
        if(alert_configuration.is_lock == False):
            return "Inactive"
        model_object = eval(module_name).objects.get(pk=record_id)

        subject_fields = alert_configuration.subject_fields.split(',')
        if str(alert_configuration.subject_fields).strip() != '':
            for each_subfield in subject_fields:
                subject_fields_lsit.append(
                    eval('model_object.' + str(each_subfield)))
        body_fields = alert_configuration.body_fields.split(',')

        if str(alert_configuration.body_fields).strip() != '':
            for each_bodyfield in body_fields:
                body_fields_list.append(
                    eval('model_object.' + str(each_bodyfield)))
        subject_content = alert_configuration.subject % tuple(
            subject_fields_lsit)
        alert_body = alert_configuration.body
        #body_fields_list.append(request.user.first_name+' '+request.user.last_name)

        body_content = alert_body % tuple(body_fields_list)
        if alert_id == 'alertdataconfig18' or alert_id == 'alertdataconfig19' or alert_id == 'alertdataconfig20' or alert_id == 'alertdataconfig26' or alert_id == 'alertdataconfig27':
            expend_tbl = Expenditure_Reimburs.objects.filter(
                reimbursement__id=record_id)
            reimbus = Reimbursement.objects.filter(id=record_id)[0]
            body_content += '<table border="1"><th> Expenditure</th><th>Amount</th>'
            for expend in expend_tbl:
                body_content += '<tr><td>' + expend.expenditure_name + '</td>'
                body_content += '<td>' + str(expend.amount) + '</td></tr>'
            body_content += '</table><br>'
            body_content += 'Total Amount:' + \
                str(reimbus.total_expenditure) + '<br><br>'
            body_content += 'Best Regards,<br>Admin<br><br>'
            body_content += 'This is a system generated alert. We request you not to reply to this message.'
        if alert_id == 'alertdataconfig22' or alert_id == 'alertdataconfig23' or alert_id == 'alertdataconfig24' or alert_id == 'alertdataconfig28' or alert_id == 'alertdataconfig29':
            expend_tbl = Expenditure.objects.filter(travel__id=record_id)
            travel = Travel.objects.filter(id=record_id)[0]
            body_content += '<table border="1"><th> Expenditure Date </th><th>Client Name</th><th>Destination</th><th>KM</th>'
            for expend in expend_tbl:
                body_content += '<tr><td>' + str(expend.expend_date) + '</td>'
                body_content += '<td>' + str(expend.client_name) + '</td>'
                body_content += '<td>' + str(expend.destination) + '</td>'
                body_content += '<td>' + str(expend.km) + '</td></tr>'
            body_content += '</table><br>'
            body_content += 'Total KM:' + str(travel.total_km) + '<br>'
            body_content += 'Total Amount:' + str(travel.total_rs) + '<br><br>'
            body_content += 'Best Regards,<br>Admin<br><br>'
            body_content += 'This is a system generated alert. We request you not to reply to this message.'
        if(comments != ''):
            body_content += comments
        to_email = alert_configuration.toemail.values()
        for each_email in to_email:
            total_to_email_list.append(each_email.get('email'))

        to_cc = alert_configuration.cc.values()
        for each_cc in to_cc:
            total_cc_email_list.append(each_cc.get('email'))

        to_bcc = alert_configuration.bcc.values()
        for each_bcc in to_bcc:
            total_cc_email_list.append(each_bcc.get('email'))
        if(len(to_id) > 0):
            total_to_email_list = total_to_email_list + to_id
        if(len(cc_id) > 0):
            total_cc_email_list = total_cc_email_list + cc_id
        total_to_email_list = filter(None, total_to_email_list)
        total_cc_email_list = filter(None, total_cc_email_list)
        if len(total_to_email_list) > 0:
            total_to_email_list = reduce(lambda x,
                                         y: x + y if y[0] not in x else x,
                                         map(lambda x: [x],
                                             total_to_email_list))
        if len(total_cc_email_list) > 0:
            total_cc_email_list = reduce(lambda x,
                                         y: x + y if y[0] not in x else x,
                                         map(lambda x: [x],
                                             total_cc_email_list))
        send_mail_flag = True
        if(send_mail_flag):
            alert_transaction = AlertDataTransaction(
                alert_id=alert_id,
                record_id=record_id,
                to_id=total_to_email_list,
                cc_id=total_cc_email_list,
                body=body_content,
                subject=subject_content)
            alert_transaction.save()
            if(alert_configuration.is_email):
                total_to_email_list = total_to_email_list + total_cc_email_list
                EmailWithCC().send_email(
                    subject_content,
                    body_content,
                    total_to_email_list,
                    settings.EMAIL_CONTENT_TYPE)
    except BaseException:
        errMessage = ERROR_MESSAGE % (
            sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
        '''
        file= open(settings.MAIL_LOG_FILE,'a')
        file.write(errMessage)
        file.close()'''


def alert_generate_timesheet(request, alert_id, user_list=[], attach='',
                             comments=''):
    '''
    Time Sheet Alerts
    '''
    try:
        total_to_email_list = []
        total_cc_email_list = []
        today_date = datetime.now().date().strftime('%m/%d/%Y')
        alert_configuration = AlertDataConfiguration.objects.get(pk=alert_id)
        if(alert_configuration.is_active == 0):
            return "Inactive"
        subject_content = alert_configuration.subject
        subject_content = subject_content % str(today_date)
        if(comments != ''):
            body_content += comments
        to_email = alert_configuration.toemail.values()
        for each_email in to_email:
            total_to_email_list.append(each_email.get('username'))
#        total_to_email_list = total_to_email_list + to_id
        if alert_id != 'alertdataconfig10':
            user_list.extend(total_to_email_list)
        for usr in user_list:
            record = User.objects.filter(username=usr)
            alert_body = alert_configuration.body
            if attach == '':
                body_content = alert_body % (str(record[0].first_name))
            else:
                body_content = alert_body
            mail_id = str(record[0].email)
            alert_transaction = AlertDataTransaction(alert_id=alert_id, record_id=str(
                record[0].id), to_id=mail_id, body=body_content, subject=subject_content)
            alert_transaction.save()
            EmailWithCC().send_email(subject_content, body_content,
                                     [mail_id],
                                     settings.EMAIL_CONTENT_TYPE,
                                     attach, '', total_cc_email_list)
    except BaseException:
        errMessage = ERROR_MESSAGE % (
            sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
        print 'errMessage', errMessage


@login_required
def list(request):
    '''
    List Of Alerts
    '''
    query = Q()
    msg = request.GET.get('msg')
    searchtext = request.GET.get('search', '')
    if request.session.get('show_inactive', '') == '':
        request.session['show_inactive'] = 1
    if str(request.session['show_inactive']) == '0' and searchtext != '':
        show_inactive = 0
    else:
        show_inactive = request.POST.get('is_active', '1')
    request.session['show_inactive'] = show_inactive
    alertlist = AlertDataConfiguration.objects.filter(
        is_active=int(show_inactive))
    if searchtext:
        for term in searchtext.split():
            q = Q(name__icontains=term)
        query = query & q
        alertlist = alertlist.filter(query)
    return render(request, 'alertlist.html', {'alertlist':
                                              alertlist, 'msg':
                                              msg, 'show_inactive':
                                              show_inactive},
                  )


@login_required
def edit(request, id):
    '''
    Alerts Edit Methods
    '''
    pagedata = {}
    alert = AlertDataConfiguration.objects.get(pk=id)
    user = User.objects.filter(is_active=1).order_by('first_name')
    pagedata.update({'alert': alert, 'user': user})
    return render(request, 'alertconfig.html',
                  {'pagedata': pagedata},
                  )


@login_required
def save(request):
    '''
    Alerts save method
    '''
    predata_dict = {}
    pagedata = {}
    record_status = request.GET.get('record_status', '')
    is_save = request.GET.get('is_save', '')
    if request.method == 'POST':
        alert_dict = {'id': request.POST.get('hdn_id', ''),
                      'name': request.POST.get('alert_name', ''),
                      'alert_type': request.POST.get('alert_type', ''),
                      'days': request.POST.get('days', '0'),
                      'frequency': request.POST.get('frequency', '0'),
                      'subject': request.POST.get('subject', ''),
                      'body': request.POST.get('body', ''),
                      'subject_fields': request.POST.get('subject_fields', ''),
                      'body_fields': request.POST.get('body_fields', ''),
                      'modified_by_id': request.user.id,
                      'is_email': 1,
                      'is_active': 1,
                      'is_screen': 1,
                      'is_lock': 1
                      }
    alert = AlertDataConfiguration(**alert_dict)
    postdata_dict = save_data(request, alert)
    alert.save()
    msg = "Alert configuration successfully saved"
    return HttpResponseRedirect(('/alert/list/') +
                                "?msg=Alert Configuration Saved Successfully ")


def save_data(request, alert):
    alert.toemail.clear()
    alert.cc.clear()
    toemail = request.POST.get('hdn_toemail', '').split(',')
    if toemail.__contains__(''):
        toemail.remove('')
    for each_mail in toemail:
        alert.toemail.add(each_mail)
    cc = request.POST.get('hdn_cc', '').split(',')
    if cc.__contains__(''):
        cc.remove('')
    for each_cc in cc:
        alert.cc.add(each_cc)


def alert_preview(module_name, alert_id,
                  record_id, to_id=[], cc_id=[], comments=''):
    '''
    Event alerts
    '''
    total_to_email_list = []
    total_cc_email_list = []
    to_id_list = []
    subject_fields_lsit = []
    body_fields_list = []
    page_data = {}
    alert_configuration = AlertDataConfiguration.objects.get(pk=alert_id)
    model_object = eval(module_name).objects.get(pk=record_id)
    subject_fields = alert_configuration.subject_fields.split(',')
    for each_subfield in subject_fields:
        subject_fields_lsit.append(
            eval('model_object.' + str(each_subfield)))
    body_fields = alert_configuration.body_fields.split(',')
    for each_bodyfield in body_fields:
        body_fields_list.append(
            eval('model_object.' + str(each_bodyfield)))
    subject_content = alert_configuration.subject % tuple(subject_fields_lsit)
    alert_body = alert_configuration.body
    # body_fields_list.append(request.user.first_name+'
    # '+request.user.last_name)
    body_content = alert_body % tuple(body_fields_list)
    if(comments != ''):
        body_content += comments
    to_email = alert_configuration.toemail.values()
    for each_email in to_email:
        total_to_email_list.append(each_email.get('email'))

    to_cc = alert_configuration.cc.values()
    for each_cc in to_cc:
        total_cc_email_list.append(each_cc.get('email'))

    to_bcc = alert_configuration.bcc.values()
    for each_bcc in to_bcc:
        total_cc_email_list.append(each_bcc.get('email'))
    if(len(to_id) > 0):
        total_to_email_list = total_to_email_list + to_id
    if(len(cc_id) > 0):
        total_cc_email_list = total_cc_email_list + cc_id
    total_to_email_list = filter(None, total_to_email_list)
    total_cc_email_list = filter(None, total_cc_email_list)
    if len(total_to_email_list) > 0:
        total_to_email_list = reduce(lambda x, y: x + y if y[
            0] not in x else x, map(lambda x: [x], total_to_email_list))
    if len(total_cc_email_list) > 0:
        total_cc_email_list = reduce(lambda x, y: x + y if y[
            0] not in x else x, map(lambda x: [x], total_cc_email_list))

    page_data = {'subject_content': subject_content,
                 'body_content': body_content,
                 'total_to_email_list': total_to_email_list}
    return page_data


@login_required
def preview(request):
    '''
    Alert configuration preview
    '''

    alert_id = request.POST.get('alert_id')
    pjtbudget = ProjectBudget.objects.all()[0].id
    preview_data = alert_preview('ProjectBudget', alert_id,
                                 '1e7884ee-07ba-11e2-8d48-00167692f6f2',
                                 ['test@5gindia.net'])
    # preview_data = alert_preview('ProjectBudget', alert_id,
    #                              '1e7884ee-07ba-11e2-8d48-00167692f6f2',
    #                              ['raveenapriya17@gmail.com'])
    json = simplejson.dumps(preview_data)
    return HttpResponse(json, mimetype='application/javascript')


def alert_status(request, status=None):
    '''
    Activate/Deactivate the alert
    '''
    if request.method == 'POST':
        alert_id = request.POST.getlist('alert_id')
    for alert in alert_id:
        alert_data = AlertDataConfiguration.objects.get(id=alert)
        alert_data.is_active = status
        alert_data.save()
    if status:
        msg = 'Alert Configuration Activated Successfully'
    else:
        msg = 'Alert Configuration Deactivated Successfully'
    return HttpResponseRedirect('/alert/list/' +
                                "?msg=%s " % msg)


def _append_list(date_check, user_data):
    vorg = ['5GI', '5GE']
    return_data = ['HOLIDAY', 'LEAVE', 'N/A', '']

    if Holiday.objects.filter(Q(holdate=date_check) &
                              Q(organization__in=vorg)):
        return return_data[0]

    if LeaveRequests.objects.filter(Q(leave_from__lte=date_check,
                                      leave_to__gte=date_check)
                                    & Q(empid=str(
            user_data.username).lower().strip())).exclude(
            approval_status='Cancelled'):
        return return_data[1]

    if TaskTracking.objects.filter(Q(start_time__startswith=date_check)
                                   & Q(user__exact=user_data.id)):

        return return_data[3]
    else:
        return return_data[2]


@login_required
def pay_it_status(request):
    return render(request, 'pay_it_status.html',
                  {'title': 'Timesheet Report'},
                  )


@login_required
def pay_it_status_days_genrte(request):
    '''
    Generate the xl sheet fromDate to toDate
    '''
    if request.method == 'POST':
        fromDate = request.POST.get('fromDate', '')
        toDate = request.POST.get('toDate', '')
        fromDate = datetime.strptime(fromDate, '%m-%d-%Y')
        toDate = datetime.strptime(toDate, '%m-%d-%Y')
        date_s = datetime.strftime(fromDate, '%Y-%m-%d')
        date_e = datetime.strftime(toDate, '%Y-%m-%d')
        _pay_it_status_convrsn(date_s, date_e, request.user.first_name)
        filename = 'PayITStatus_' + str(date_s) + '_to_' + str(date_e) + '.xls'
        FILE_attach = settings.PAY_IT_STATUS_PATH
        filepath = FILE_attach
        wrapper = FileWrapper(file(filepath))
        response = HttpResponse(
            wrapper, content_type='application/vnd.ms-excel')
        response[
            'Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


@login_required
def pay_it_status_hours_genrte(request):
    '''
    Generate the xl sheet with hours data
    '''
    header = []
    pjtid_list = []
    sum_of_pjt = {}
    sum_of_person = {}
    pjt_n = ''
    list_data = []
    user_data = []
    user_list = []
    flag = False
    list_data = _set_header_space()
    if request.method == 'POST':
        fromDate = request.POST.get('fromDate', '')
        toDate = request.POST.get('toDate', '')
        fromDate = datetime.strptime(fromDate, '%m-%d-%Y')
        toDate = datetime.strptime(toDate, '%m-%d-%Y') + relativedelta(days=+1)
        date_s = datetime.strftime(fromDate, '%Y-%m-%d')
        date_e = datetime.strftime(toDate, '%Y-%m-%d')
        pjtid_list = TaskTracking.objects.filter(
            start_time__range=[date_s, date_e])
        pjtid = pjtid_list.distinct().values('program')
        pjt = [each['program'] for each in pjtid]
        header = ['Projects', 'Hours']
        list_data.append(header)
        for data in pjt:
            if data is None:
                pjt_n = u'Non Project Task'
                sum_of_pjt[pjt_n] = pjtid_list.filter(
                    program=data).aggregate(
                    total_pjt=Sum('time_spent'))
                sum_of_person[pjt_n] = pjtid_list.filter(program=data).values(
                    'user__username').order_by('user').annotate(total=Sum('time_spent'))
            else:
                pjt_n = Project.objects.filter(id=data)[0].name
                sum_of_pjt[pjt_n] = pjtid_list.filter(
                    program=data).aggregate(
                    total_pjt=Sum('time_spent'))
                sum_of_person[pjt_n] = pjtid_list.filter(program=data).values(
                    'user__username').order_by('user').annotate(total=Sum('time_spent'))

        for key, values in sum_of_pjt.iteritems():
            data = []
            data = [key, values['total_pjt']]
            list_data.append(data)
            for keys, val in sum_of_person.iteritems():
                if key == keys:
                    for lt in val:
                        datas = []
                        datas = [lt['user__username'], lt['total']]
                        list_data.append(datas)
        user = User.objects.filter(is_active=True)
        data = ['User', 'Hours']
        user_data.append(data)
        for usr in user:
            flag = True
            for keys, val in sum_of_person.iteritems():
                for lt in val:
                    if usr.username == lt['user__username']:
                        if flag:
                            user_name = []
                            total = pjtid_list.filter(
                                user__username=usr.username).aggregate(
                                total_prsn=Sum('time_spent'))
                            user_name = [str(usr.username),
                                         total['total_prsn']]
                            user_data.append(user_name)
                            user_list.append(usr.username)
                            flag = False
                        data = []
                        data = [keys, lt['total']]
                        user_data.append(data)

        total_sum = pjtid_list.aggregate(total_pjt=Sum('time_spent'))
        data = ['Total', total_sum['total_pjt']]
        list_data.append(data)
        filename = 'PayITStatus_Hours_' + \
            str(date_s) + '_to_' + str(date_e) + '.xls'
        folder = 'PayITStatus_xl'
        currentdir = settings.MEDIA_ROOT
        currentosdir = currentdir + '/' + folder
        currentdir = os.listdir(currentdir)
        check = 0
        for each in currentdir:
            if each == folder:
                check = 1
        if(check != 1):
            os.mkdir(currentosdir)
        wb = xlwt.Workbook()
        ws = wb.add_sheet("Hours")
        userbook = wb.add_sheet("Person")
        #_set_header(ws, "", header, request.user.first_name, fromDate, toDate)
        now = datetime.now()
        TITLE = easyxf(
            'font: color black,bold on, height 420; align:horiz center')
        ws.write_merge(0, 1, 0, len(header) -
                       1, "Project-Wise Person Report", TITLE)

        ws.write(2, 0, "Report By:" + request.user.first_name)
        ws.write(2, 1, "From Date:" + str(fromDate))
        ws.write(3, 0, "Date & Time:" + now.strftime('%Y/%m/%d %H:%M:%S'))
        ws.write(3, 1, "To Date:" + str(toDate))

        HEADER = easyxf(
            'font: color black, bold on,height 220 ; align: '
            'horiz left;pattern: pattern solid, fore_colour gray25, back_colour gray25')
        SUBHEADER = easyxf(
            'font: color black, bold on,height 220 ; align: '
            'horiz left;pattern: pattern solid, fore_colour yellow, back_colour yellow')
        BODY = easyxf('font: color black,height 210;')
        for i, row in enumerate(list_data):
            for j, col in enumerate(row):
                if col in header:
                    ws.write(i, j, col, HEADER)
                elif col in sum_of_pjt:
                    ws.write(i, j, col, SUBHEADER)
                else:
                    ws.write(i, j, col, BODY)
        ws.col(0).width = 256 * (50)
        for i, row in enumerate(user_data):
            for j, col in enumerate(row):
                if col in user_list:
                    userbook.write(i, j, col, HEADER)
                else:
                    userbook.write(i, j, col, BODY)
        userbook.col(0).width = 256 * (50)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        wb.save(response)
        return response


def _pay_it_status_convrsn(start_date, end_date, requested_by):
    '''
    Conversion of daily task into spread sheet

    '''
    now = datetime.now()
    list_date = []
    date_header = ['Emp_id', 'Emp Name']
    list_data = []

    date_s = datetime.strptime(start_date, "%Y-%m-%d")
    date_e = datetime.strptime(end_date, "%Y-%m-%d")
    emailomission = Emailomission.objects.all()
    for dt in rrule(DAILY, dtstart=date_s, until=date_e):
        if dt.strftime("%A") != 'Sunday' and dt.strftime("%A") != 'Saturday':
            list_date.append(dt.strftime("%Y-%m-%d"))
            date_header.append(dt.strftime("%d-%m-%Y"))
    user_list = User.objects.filter(is_active=True).exclude(
        username__in=emailomission.values('adsslogin'))
    list_data = _set_header_space()
    list_data.append(date_header)
    for user in user_list:
        user_code_list = UserProfile.objects.filter(user=user.id)
        if user_code_list.count() != 0:
            user_code = user_code_list[0].code
            data = []
            data = [user_code, user.first_name]
            for date_item in list_date:
                data.append(_append_list(date_item, user))
            list_data.append("")
        list_data.append(data)
    filename = 'PayITStatus.xls'
    folder = 'PayITStatus_xl'
    currentdir = settings.MEDIA_ROOT
    currentosdir = currentdir + '/' + folder
    currentdir = os.listdir(currentdir)
    check = 0
    for each in currentdir:
        if each == folder:
            check = 1
    if(check != 1):
        os.mkdir(currentosdir)
    wb = xlwt.Workbook()
    ws = wb.add_sheet("My Sheet")
    _set_header(
        ws,
        "PM Report Sheet",
        date_header,
        requested_by,
        start_date,
        end_date)
    HEADER = easyxf(
        'font: color black, bold on,height 220 ; align: '
        'horiz left;pattern: pattern solid, fore_colour gray25, back_colour gray25')
    BODY = easyxf('font: color black,height 210;')
    for i, row in enumerate(list_data):
        for j, col in enumerate(row):
            if col in date_header:
                ws.write(i, j, col, HEADER)
            else:
                ws.write(i, j, col, BODY)
    wb.save('%s/%s' % (currentosdir, filename))


def timesheet_alert(request):
    '''
    Time Sheet Alert
    '''
    email_to_list = []
    start_date = ''
    end_date = ''
    vorg = ['5GI', '5GE','1']
    today_date = datetime.now().date()
    if not Holiday.objects.filter(Q(holdate=today_date) &
                                  Q(organization__in=vorg)):
        emp_in_leave =[]
        emp_list = LeaveRequests.objects.filter(Q(leave_from__lte=today_date,leave_to__gte=today_date)).exclude(approval_status='Cancelled').values_list('empid', flat=True)
        user_name = User.objects.filter(id__in=emp_list)
        for name in user_name:
            emp_in_leave.append(name.username)

        emailomission = Emailomission.objects.all().values('adsslogin')
        user = User.objects.filter(is_active=True).exclude(
            username__in=emp_in_leave).exclude(username__in=emailomission)
        # print user
        for userdata in user:
            if not TaskTracking.objects.filter(
                    Q(start_time__startswith=today_date) &
                    Q(user__exact=userdata.id)):
                email_to_list.append(userdata.username)

        alert_generate_timesheet(request, 'alertdataconfig10', email_to_list)


def pm_status_report_mail(request):
    '''
    PayIt status report for   project manager
    '''
    email_pmto_list = []
    start_date = ''
    end_date = ''
    today_day = datetime.now().strftime("%A")
    if (today_day == 'Monday'):
        tod_date = datetime.now()
        tod_date = datetime.now()
        end_date = tod_date + relativedelta(days=-3)
        start_date = end_date + relativedelta(days=-4)
        date_s = start_date.date()
        date_e = end_date.date()
        _pay_it_status_convrsn(str(date_s), str(date_e))
        FILE_attach = settings.PAY_IT_STATUS_PATH
        alert_owners = User.objects.filter(
            groups__name__icontains='Alertmail_permission',
            is_active=True).values('username')
        email_pmto_list = [each['username'] for each in alert_owners]
        alert_generate_timesheet(
            request, 'alertdataconfig11', email_pmto_list, FILE_attach)


def task_report(request):
    '''
    To generate report based on person,project,time spent
    '''
    report_list = []
    if request.method == 'POST':
        filename = 'task_report.xls'
        work_book = xlwt.Workbook()
        userbook = work_book.add_sheet("Task Report")
        fromDate = request.POST.get('fromDate', '')
        toDate = request.POST.get('toDate', '')
        fromDate = datetime.strptime(fromDate, '%m-%d-%Y')
        toDate = datetime.strptime(toDate, '%m-%d-%Y') + relativedelta(days=+1)
        date_s = datetime.strftime(fromDate, '%Y-%m-%d')
        date_e = datetime.strftime(toDate, '%Y-%m-%d')
        timesheet_list = TaskTracking.objects.filter(
            start_time__range=[date_s, date_e])
        task_list = dict(
            Task.objects.filter(
                id__in=[
                    a[0] for a in timesheet_list.values_list('task')]).values_list(
                'id',
                'name'))
        #task_dict = task_name
        project_list = dict(
            Project.objects.filter(
                id__in=[
                    a[0] for a in timesheet_list.values_list('program')]).values_list(
                'id',
                'name'))
        header_list = [
            'UserName',
            'ProjectName',
            'Tasks',
            'StartTime',
            'TimeSpent']
        for j, col in enumerate(header_list):
            userbook.write(0, j, col)
        for i, task in enumerate(timesheet_list):
            #import pdb;pdb.set_trace()
            result_list = []
            task_name = task_list[long(float(task.task))]
            if task.program is not None:
                project_name = project_list[long(float(task.program))]
            else:
                project_name = "Non-Project Task"
            result_list = [
                task.user.username,
                project_name,
                task_name,
                datetime.strftime(
                    task.start_time,
                    '%Y-%m-%d %H:%M:%S'),
                task.time_spent]
            for j, col in enumerate(result_list):
                userbook.write(i + 1, j, col)
        userbook.col(1).width = 256 * (25)
        userbook.col(2).width = 256 * (50)
        userbook.col(3).width = 256 * (25)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        work_book.save(response)
        return response


def _get_users():
    return User.objects.filter(is_active=True).exclude(
        username__in=Emailomission.objects.all().values('adsslogin'))


def _get_projects(tasks):
    project_list = []
    for task_obj in tasks:
        project_name = task_obj.get_projectname(task_obj.task)
        seen = set(project_list)
        if project_name not in seen:
            seen.add(project_name)
            project_list.append(project_name)
    return project_list


def _append_detail(list_data, users, date_s, date_e, list_date):
    vorg = ['5GI', '5GE']
    for user in users:
        # user_code = UserProfile.objects.filter(user=user.id)[0].code
        user_code = UserProfile.objects.filter(user=user.id)
        if user_code.count() != 0:
            user_code = user_code[0].code

    # for user in user_list:
    #     user_code_list = UserProfile.objects.filter(user=user.id)
    #     if user_code_list.count() != 0:
    #         user_code = user_code_list[0].code

            data = [user_code, user.first_name, '']
            time_spent = []
            tasks = TaskTracking.objects.filter(Q(user=user.id) & Q(
                start_time__range=[date_s, date_e + timedelta(1)]))
            projects = _get_projects(tasks)
            hours_count = 0
            missed_entry_count = 0
            leave_count = 0
            for date in list_date:
                time = tasks.filter(
                    start_time__startswith=date).aggregate(
                    Sum('time_spent')).values()
                if time[0] is not None:
                    data.append(float(time[0]))
                    hours_count += float(time[0])
                else:
                    if Holiday.objects.filter(Q(holdate=date) &
                                              Q(organization__in=vorg)):
                        data.append('Holid')
                    elif LeaveRequests.objects.filter(Q(leave_from__lte=date,
                                                        leave_to__gte=date)
                                                      & Q(empid=str(
                                                          user.username).lower().strip())).exclude(
                            approval_status='Cancelled'):
                        data.append('Leave')
                        leave_count += 1
                    else:
                        data.append(0.0)
                        missed_entry_count += 1
            data.append(hours_count)
            data.append(leave_count)
            data.append(missed_entry_count)
            list_data.append("")
            list_data.append(data)

            for project in projects:
                if project is not None:
                    name = project
                else:
                    name = "Non-Project tasks"

                detail = ['', '', name]
                for date in list_date:
                    daily_task = tasks.filter(start_time__startswith=date)
                    hours = 0
                for task in daily_task:
                    if project == task.get_projectname(task.task):
                        hours += task.time_spent
                detail.append(hours)
                list_data.append(detail)
    return list_data


def get_column(n):
    MAX = 50
    string = ["\0"] * MAX
    i = 0
    while n > 0:
        rem = n % 26
        if rem == 0:
            string[i] = 'Z'
            i += 1
            n = (n / 26) - 1
        else:
            string[i] = chr((rem - 1) + ord('A'))
            i += 1
            n = n / 26
    string[i] = '\0'
    string = string[::-1]
    return "".join(string)


def _save(title, sheet_header, list_data, user, fromDate, toDate):
    filename = 'PayITStatus.xls'
    folder = 'PayITStatus_xl'
    currentdir = settings.MEDIA_ROOT
    currentosdir = currentdir + '/' + folder
    currentdir = os.listdir(currentdir)
    check = 0
    for each in currentdir:
        if each == folder:
            check = 1
    if(check != 1):
        os.mkdir(currentosdir)
    wb = xlwt.Workbook()
    ws = wb.add_sheet("My Sheet", cell_overwrite_ok=True)
    _set_header(ws, title, sheet_header, user, fromDate, toDate)
    HEADER = easyxf(
        'font: color black, bold on,height 220 ; align: '
        'horiz left;pattern: pattern solid, fore_colour gray25, back_colour gray25')
    SUBHEADER = easyxf(
        'font: color black, bold on,height 220 ; align: '
        'horiz left;pattern: pattern solid, fore_colour yellow, back_colour yellow')
    LEAVE = easyxf('font: color red,bold on,height 210;')
    HOLID = easyxf('font: color green,bold on,height 210;')
    BODY = easyxf('font: color black,height 210;')
    for i, row in enumerate(list_data):
        for j, col in enumerate(row):
            if col in sheet_header:
                ws.write(i, j, col, HEADER)
            else:
                if col == "Holid":
                    ws.write(i, j, col, HOLID)
                elif col == 'Leave':
                    ws.write(i, j, col, LEAVE)
                else:
                    ws.write(i, j, col, BODY)
    #column = get_column(len(sheet_header))
    #ws.write(i+2, 4, xlwt.Formula("SUM('{0}'!G{1}:G{2})".format(u"My Sheet", 9, i+1)))
    wb.save('%s/%s' % (currentosdir, filename))
    return filename


def _set_header_space():
    list_data = []
    for iterate in range(5):
        list_data.append("")
    return list_data


def _set_header(ws, title, header, user, fromDate, toDate):
    now = datetime.now()
    TITLE = easyxf('font: color black,bold on, height 420; align:horiz center')
    ws.write_merge(0, 1, 0, len(header) - 1, title, TITLE)

    ws.write(2, 0, "Report By:")
    ws.write(2, 1, user)
    ws.write(2, len(header) - 2, "From Date")
    ws.write(2, len(header) - 1, fromDate)
    ws.write(3, 0, "Date & Time:")
    ws.write(3, 1, now.strftime('%Y/%m/%d %H:%M:%S'))
    ws.write(3, len(header) - 2, "To Date")
    ws.write(3, len(header) - 1, toDate)


@login_required
def sheet_report(request):
    '''
    Generate the xl sheet fromDate to toDate
    '''
    if request.method == 'POST':
        list_date = []
        list_day = ['', '', '']
        sheet_header = ['Emp_id', 'Name', 'Projects']
        extend_header = [
            'Total Spent Hrs.',
            'No.Of Leaves',
            'Not Entered/Days']

        fromDate = request.POST.get('fromDate', '')
        toDate = request.POST.get('toDate', '')
        fromDate = datetime.strptime(fromDate, '%m-%d-%Y')
        toDate = datetime.strptime(toDate, '%m-%d-%Y')
        date_s = datetime.strftime(fromDate, '%Y-%m-%d')
        date_e = datetime.strftime(toDate, '%Y-%m-%d')
        date_s = datetime.strptime(date_s, "%Y-%m-%d")
        date_e = datetime.strptime(date_e, "%Y-%m-%d")
        for dt in rrule(DAILY, dtstart=date_s, until=date_e):
            list_date.append(dt.strftime("%Y-%m-%d"))
            sheet_header.append(dt.strftime("%d/%m"))
            list_day.append(dt.strftime("%A")[:3])
        sheet_header.extend(extend_header)
        users = _get_users()
        list_data = _set_header_space()

        list_data.append(sheet_header)
        list_data.append(list_day)

        list_data = _append_detail(list_data, users, date_s, date_e, list_date)
        filename = _save(
            "Time Sheet Report",
            sheet_header,
            list_data,
            request.user.first_name,
            datetime.strftime(
                date_s,
                '%d-%m-%Y'),
            datetime.strftime(
                date_e,
                '%d-%m-%Y'))
        FILE_attach = settings.PAY_IT_STATUS_PATH
        filepath = FILE_attach
        wrapper = FileWrapper(file(filepath))
        response = HttpResponse(
            wrapper, content_type='application/vnd.ms-excel')
        response[
            'Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


def _daily_detail(list_data, users, date_s, date_e, list_date):
    vorg = ['5GI', '5GE']
    for user in users:
        # user_code = UserProfile.objects.filter(user=user.id)[0].code
        user_code = UserProfile.objects.filter(user=user.id)
        if user_code.count() != 0:
            user_code = user_code[0].code

            data = [user_code, user.first_name]
            time_spent = []
            tasks = TaskTracking.objects.filter(Q(user=user.id) & Q(
                start_time__range=[date_s, date_e + timedelta(1)]))
            hours_count = 0
            missed_entry_count = 0
            leave_count = 0
            for date in list_date:
                time = tasks.filter(
                    start_time__startswith=date).aggregate(
                    Sum('time_spent')).values()
                if time[0] is not None:
                    data.append(float(time[0]))
                    hours_count += float(time[0])
                else:
                    if Holiday.objects.filter(Q(holdate=date) &
                                              Q(organization__in=vorg)):
                        data.append('Holid')
                    elif LeaveRequests.objects.filter(Q(leave_from__lte=date,
                                                        leave_to__gte=date)
                                                      & Q(empid=str(
                                                          user.username).lower().strip())).exclude(
                            approval_status='Cancelled'):
                        data.append('Leave')
                        leave_count += 1
                    else:
                        data.append(0.0)
                        missed_entry_count += 1
            data.append(hours_count)
            data.append(leave_count)
            data.append(missed_entry_count)
            list_data.append("")
            list_data.append(data)
    return list_data


def daily_report(request):
    '''
    Generate the xl sheet fromDate to toDate
    '''
    if request.method == 'POST':
        list_date = []
        sheet_header = ['Emp_id', 'Name']
        extend_header = [
            'Total Spent Hrs.',
            'No.Of Leaves',
            'Not Entered/Days']

        fromDate = request.POST.get('fromDate', '')
        toDate = request.POST.get('toDate', '')
        fromDate = datetime.strptime(fromDate, '%m-%d-%Y')
        toDate = datetime.strptime(toDate, '%m-%d-%Y')
        date_s = datetime.strftime(fromDate, '%Y-%m-%d')
        date_e = datetime.strftime(toDate, '%Y-%m-%d')
        date_s = datetime.strptime(date_s, "%Y-%m-%d")
        date_e = datetime.strptime(date_e, "%Y-%m-%d")
        for dt in rrule(DAILY, dtstart=date_s, until=date_e):
            list_date.append(dt.strftime("%Y-%m-%d"))
            sheet_header.append(dt.strftime("%d/%m"))
        sheet_header.extend(extend_header)
        users = _get_users()
        list_data = _set_header_space()

        list_data.append(sheet_header)
        list_data = _daily_detail(list_data, users, date_s, date_e, list_date)
        filename = _save(
            "Daily Report",
            sheet_header,
            list_data,
            request.user.first_name,
            datetime.strftime(
                date_s,
                '%d-%m-%Y'),
            datetime.strftime(
                date_e,
                '%d-%m-%Y'))
        FILE_attach = settings.PAY_IT_STATUS_PATH
        filepath = FILE_attach
        wrapper = FileWrapper(file(filepath))
        response = HttpResponse(
            wrapper, content_type='application/vnd.ms-excel')
        response[
            'Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


def _get_resources(task, date_s, date_e):
    return TaskTracking.objects.filter(
        start_time__range=[
            date_s,
            date_e + timedelta(1)],
        task=task) .distinct().values_list(
            'user_id',
        flat=True)


def _get_pjt_header(pjt_header, pjt, list_date):
    total_hrs = 0.0
    for date in list_date:
        hrs = TaskTracking.objects.filter(
            program=pjt, start_time__startswith=date).aggregate(
            Sum('time_spent')).values()
        if hrs[0] is None:
            pjt_header.append(0.0)
        else:
            pjt_header.append(float(hrs[0]))
            total_hrs += float(hrs[0])
    pjt_header.append(float(total_hrs))
    return pjt_header


def _get_pjt_data(list_data, pjt, list_date, date_s, date_e):
    total_hrs = 0.0
    task_obj = TaskTracking.objects.filter(
        program=pjt, start_time__range=[
            date_s, date_e + timedelta(1)])
    tasks = task_obj.distinct().values_list('task', flat=True)
    for task in tasks:
        tsk_name = Task.objects.get(id=task).name
        tsk_data = ['', '', tsk_name]
        resources = _get_resources(task, date_s, date_e)
        list_data.append(tsk_data)
        for resource in resources:
            res_name = User.objects.get(id=resource).first_name
            pjt_data = ['', '', '', res_name]
            tot_tsk_hrs = 0.0
            for date in list_date:
                daily = task_obj.filter(start_time__startswith=date)
                tsk_hrs = daily.filter(
                    task=task).aggregate(
                    Sum('time_spent')).values()
                if tsk_hrs[0] is not None:
                    tot_tsk_hrs += float(tsk_hrs[0])
                print tot_tsk_hrs
                pjt_data.append(tsk_hrs[0])
            pjt_data.append(tot_tsk_hrs)
            list_data.append(pjt_data)
    return list_data


def _project_detail(list_data, date_s, date_e, list_date):
    pjtid_list = TaskTracking.objects.filter(
        start_time__range=[date_s, date_e + timedelta(1)])
    pjts = pjtid_list.distinct().values_list('program', flat=True)
    pjt_resources = []
    for pjt in pjts:
        if pjt is None:
            pjt_header = ['None', 'Non-Project Tak', '', '']
        else:
            project = Project.objects.get(id=pjt).name
            pjt_header = [pjt, project, '', '']
        pjt_header = _get_pjt_header(pjt_header, pjt, list_date)
        list_data.append(pjt_header)
        list_data = _get_pjt_data(list_data, pjt, list_date, date_s, date_e)
    return list_data


def project_report(request):
    '''
    Generate the xl sheet fromDate to toDate
    '''
    if request.method == 'POST':
        list_date = []
        sheet_header = ['Code', 'Project Name', 'Tasks', 'Resources']
        extend_header = ['Total Spent Hrs.']
        fromDate = request.POST.get('fromDate', '')
        toDate = request.POST.get('toDate', '')
        fromDate = datetime.strptime(fromDate, '%m-%d-%Y')
        toDate = datetime.strptime(toDate, '%m-%d-%Y')
        date_s = datetime.strftime(fromDate, '%Y-%m-%d')
        date_e = datetime.strftime(toDate, '%Y-%m-%d')
        date_s = datetime.strptime(date_s, "%Y-%m-%d")
        date_e = datetime.strptime(date_e, "%Y-%m-%d")
        for dt in rrule(DAILY, dtstart=date_s, until=date_e):
            list_date.append(dt.strftime("%Y-%m-%d"))
            sheet_header.append(dt.strftime("%d/%m"))
        sheet_header.extend(extend_header)
        list_data = _set_header_space()

        list_data.append(sheet_header)
        list_data = _project_detail(list_data, date_s, date_e, list_date)
        filename = _save(
            'Project Report',
            sheet_header,
            list_data,
            request.user.first_name,
            datetime.strftime(
                date_s,
                '%d-%m-%Y'),
            datetime.strftime(
                date_e,
                '%d-%m-%Y'))
        FILE_attach = settings.PAY_IT_STATUS_PATH
        filepath = FILE_attach
        wrapper = FileWrapper(file(filepath))
        response = HttpResponse(
            wrapper, content_type='application/vnd.ms-excel')
        response[
            'Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

