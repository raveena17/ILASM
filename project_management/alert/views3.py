import sys
import datetime
import csv
import os
import xlwt

from django.conf import settings
#from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.http import Http404
# from django.shortcuts import render_to_response
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db.models import Q
# from django.utils import simplejson
try:
    import django.utils.simplejson
except:
    import json as simplejson

from dateutil.relativedelta import *
from dateutil.rrule import rrule, DAILY
from django.db.models import Sum
from xlwt import Workbook, easyxf
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User

from project_management.alert.models import *
from project_management.projects.models import * 
from project_management.announcements.models import *
from project_management.projectbudget.models import *
from project_management.users.models import *
from project_management.timesheet.models import *
from project_management.Utility import EmailWithCC
from django.contrib.auth.models import User


MODULE = 'Alert'
ERROR_MESSAGE = 'ERROR : %s \nLINE NUMBER : %s'

def get_perms(request):
    
    alert_owners = User.objects.filter(groups__name__icontains='Alertmail_permission', is_active=True).values('id')
    return alert_owners

def alert_generate(request, module_name, alert_id, record_id, to_id = [], cc_id = [], comments=''):
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
                subject_fields_lsit.append(eval('model_object.' + str(each_subfield)))
        body_fields = alert_configuration.body_fields.split(',')
        
        if str(alert_configuration.body_fields).strip() != '':
            for each_bodyfield in body_fields:
                body_fields_list.append(eval('model_object.' + str(each_bodyfield)))            
        subject_content = alert_configuration.subject % tuple(subject_fields_lsit)
        alert_body = alert_configuration.body
        #body_fields_list.append(request.user.first_name+' '+request.user.last_name)
        
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
            total_to_email_list = reduce(lambda x, y: x + y if y[0] not in x else x, map(lambda x: [x], total_to_email_list))
        if len(total_cc_email_list) > 0:
            total_cc_email_list = reduce(lambda x, y: x + y if y[0] not in x else x, map(lambda x: [x], total_cc_email_list))
        print 'total_to_email_list',total_to_email_list,total_cc_email_list
        send_mail_flag = True       
        if(send_mail_flag):
            alert_transaction = AlertDataTransaction(alert_id=alert_id, record_id=record_id,
            to_id=total_to_email_list, cc_id=total_cc_email_list,
            body=body_content, subject=subject_content)
            alert_transaction.save()
            if(alert_configuration.is_email):
                total_to_email_list = total_to_email_list + total_cc_email_list
                EmailWithCC().send_email(subject_content, body_content, total_to_email_list, settings.EMAIL_CONTENT_TYPE)            
    except:
        errMessage = ERROR_MESSAGE % (sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
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
            alert_transaction = AlertDataTransaction(alert_id=alert_id,
                record_id=str(record[0].id),to_id=mail_id,
                body=body_content, subject=subject_content)
            alert_transaction.save()            
            EmailWithCC().send_email(subject_content, body_content,
                                     [mail_id],
                                     settings.EMAIL_CONTENT_TYPE,
                                     attach, '', total_cc_email_list)
    except:
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
    alertlist = AlertDataConfiguration.objects.filter(is_active=
                                                      int(show_inactive))
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
    if status == True:
        msg = 'Alert Configuration Activated Successfully'
    else:
        msg = 'Alert Configuration Deactivated Successfully'
    return HttpResponseRedirect('/alert/list/' +
                                "?msg=%s "%msg)


def _append_list(date_check, user_data):
    vorg = ['5GI']
    return_data = ['HOLIDAY', 'LEAVE', 'N/A', '']

    if Holiday.objects.filter(Q(holdate=date_check) &
                              Q(organization__in=vorg)):
        return  return_data[0]

    if LeaveRequests.objects.filter(Q(leave_from__lte=date_check,
            leave_to__gte=date_check)
            & Q(empid__startswith=str(\
            user_data.username).lower().strip())).exclude(\
            approval_status = 'Cancelled'):
        return return_data[1]
    
    if TaskTracking.objects.filter(Q(start_time__startswith=
                                     date_check)
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
        fromDate =datetime.strptime(fromDate, '%m-%d-%Y')
        toDate = datetime.strptime(toDate, '%m-%d-%Y')
        date_s = datetime.strftime(fromDate, '%Y-%m-%d')
        date_e = datetime.strftime(toDate, '%Y-%m-%d')       
        _pay_it_status_convrsn(date_s, date_e)
        filename = 'PayITStatus_'+str(date_s)+'_to_'+str(date_e)+'.xls'
        FILE_attach = settings.PAY_IT_STATUS_PATH
        filepath = FILE_attach
        wrapper = FileWrapper(file(filepath))
        response = HttpResponse(
            wrapper, content_type='application/vnd.ms-excel')
        response[
            'Content-Disposition'] = 'attachment; filename=%s'%filename
        return response

@login_required
def pay_it_status_hours_genrte(request):
    '''
    Generate the xl sheet with hours data
    '''
    pjtid_list = []
    sum_of_pjt = {}
    sum_of_person = {}
    pjt_n = ''
    list_data = []
    user_data = []
    user_list = []
    flag = False
    if request.method == 'POST':       
        fromDate = request.POST.get('fromDate', '')
        toDate = request.POST.get('toDate', '')
        fromDate = datetime.strptime(fromDate, '%m-%d-%Y')
        toDate = datetime.strptime(toDate, '%m-%d-%Y') + relativedelta(days=+1)
        date_s = datetime.strftime(fromDate, '%Y-%m-%d')
        date_e = datetime.strftime(toDate, '%Y-%m-%d')  
        pjtid_list = TaskTracking.objects.filter(start_time__range=[date_s,date_e])       
        pjtid = pjtid_list.distinct().values('program')
        pjt = [each['program'] for each in pjtid]       
        data = ['Projects','Hours']
        list_data.append(data)
        for data in pjt:
            if data == None:
                pjt_n = u'Non Project Task'
                sum_of_pjt[pjt_n] = pjtid_list.filter(program = data).aggregate(total_pjt = Sum('time_spent'))
                sum_of_person[pjt_n] = pjtid_list.filter(program = data).values(\
                    'user__username').order_by('user').annotate(total =
                    Sum('time_spent'))
            else:
                pjt_n = Project.objects.filter(id = data)[0].name                
                sum_of_pjt[pjt_n] = pjtid_list.filter(program = data).aggregate(total_pjt = Sum('time_spent'))
                sum_of_person[pjt_n] = pjtid_list.filter(program = data).values('user__username').order_by('user').annotate(total = 
                                    Sum('time_spent'))
                                    
        for key,values in sum_of_pjt.iteritems():
            data = []
            data = [key,values['total_pjt']]
            list_data.append(data)            
            for keys,val in sum_of_person.iteritems():
                if key == keys:                    
                    for lt in val:
                        datas = []
                        datas = [lt['user__username'],lt['total']]                        
                        list_data.append(datas)
        user = User.objects.filter(is_active = True)
        data = ['User','Hours']
        user_data.append(data)
        for usr in user:
            flag = True            
            for keys,val in sum_of_person.iteritems():
                for lt in val:
                    if usr.username ==lt['user__username']:
                        if flag == True:
                            user_name = []
                            total = pjtid_list.filter(user__username = usr.username).aggregate(total_prsn = Sum('time_spent'))
                            user_name = [str(usr.username),total['total_prsn']]
                            user_data.append(user_name)
                            user_list.append(usr.username)
                            flag = False
                        data = []                        
                        data = [keys,lt['total']]
                        user_data.append(data)            
       
        total_sum = pjtid_list.aggregate(total_pjt = Sum('time_spent'))
        data = ['Total',total_sum['total_pjt']]
        list_data.append(data)
        filename = 'PayITStatus_Hours_'+str(date_s)+'_to_'+str(date_e)+'.xls'
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
        HEADER = easyxf('font: color black, bold on,height 220 ; align: '\
            'horiz left;pattern: pattern solid, fore_colour yellow, back_colour yellow')
        BODY = easyxf('font: color black,height 210;')
        for i, row in enumerate(list_data):
            for j, col in enumerate(row):                
                if col in sum_of_pjt :
                    ws.write(i, j, col,HEADER)  
                else:
                    ws.write(i, j, col,BODY)
        ws.col(0).width = 256 * (50)        
        for i, row in enumerate(user_data):
            for j, col in enumerate(row):
                if col in user_list :
                    userbook.write(i, j, col,HEADER)
                else:
                    userbook.write(i, j, col,BODY)
        userbook.col(0).width = 256 * (50) 
        response = HttpResponse(mimetype='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        wb.save(response)
        return response
            
        
    
    
def _pay_it_status_convrsn(start_date, end_date):
    '''
    Conversion of daily task into spread sheet

    '''
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
        
    list_data.append(date_header)
    for user in user_list:
        user_code = UserProfile.objects.filter(user=user.id)[0].code
        data = []
        data = [user_code, user.first_name]
        for date_item in list_date:
            data.append(_append_list(date_item, user))
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
    for i, row in enumerate(list_data):
        for j, col in enumerate(row):
            ws.write(i, j, col)
    wb.save('%s/%s' % (currentosdir, filename))


def timesheet_alert(request):
    '''
    Time Sheet Alert
    '''
    email_to_list = []    
    start_date = ''
    end_date = ''
    vorg = ['5GI']
    today_date = datetime.now().date()       
    if not Holiday.objects.filter(Q(holdate=today_date) &
                                  Q(organization__in=vorg)):
        emp_in_leave = LeaveRequests.objects.filter(Q(leave_from__lte=today_date,
                          leave_to__gte=today_date)).exclude(approval_status = 'Cancelled').values('empid')

        emailomission = Emailomission.objects.all().values('adsslogin')
        user = User.objects.filter(is_active=True).exclude(
            username__in=emp_in_leave).exclude(username__in=emailomission)
        for userdata in user:
            if not TaskTracking.objects.filter(\
                    Q(start_time__startswith=today_date) & \
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
        alert_owners = User.objects.filter(groups__name__icontains='Alertmail_permission', is_active=True).values('username')
        email_pmto_list = [each['username'] for each in alert_owners]         
        alert_generate_timesheet(
            request, 'alertdataconfig11',email_pmto_list, FILE_attach)