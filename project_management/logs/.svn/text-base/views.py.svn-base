from django.shortcuts import render_to_response
from django.core.paginator import Paginator
from django.conf import settings
from django.template import RequestContext

from project_management.Utility import GetDateType
from django.contrib.auth.decorators import permission_required
from project_management.logs.models import EventLog, ErrorLog, \
    AuditLog, SecurityLog

import datetime

LOG_TYPE = {'Event Log':EventLog, 'Error Log':ErrorLog,
    'Audit Log':AuditLog, 'Security Log':SecurityLog }

SORTING_COLS = {'': '-timeStamp',
                'DateTime': '-timeStamp','-DateTime': 'timeStamp',
                'Client': 'client','-Compnay':'-client',
                'User':'users','-User':'-users',
                'Screen':'screen','-Screen':'-screen',
                'Action':'actionPerformed','-Action':'-actionPerformed',
                'Message':'notes','-Message':'-notes'
                }

@permission_required('log.add_errorlog')
def DisplayLog(request):
    request.session["logFilterData"] = None
    userName = ''
    LoginData = request.session.get('LoginData','')
    if LoginData != '':
        userName = LoginData['userName'][0]
    return render_to_response('Logs.html', {'title': 'Logs',
        'userName':userName}, context_instance = RequestContext(request) )

@permission_required('log.add_errorlog')
def DisplayLogData(request):
    LoginData = request.session.get('LoginData', '')
    userName = ''
    if LoginData != '':
        userName = LoginData['userName'][0]
    header_cols = ['DateTime', 'User', 'Screen', 'Action', 'Message']
    filterData = request.session.get("logFilterData", None)
    if request.method == 'POST' :
        filterData = __getFilterData__(request)
        request.session["logFilterData"] = filterData
    title = filterData['logType']
    pageNo = request.GET.get('pageNo', '')
    if(pageNo == ''):
        pageNo = 1
    else:
        pageNo = int(pageNo)

    sortCol = request.GET.get('sortCol', '')
    if sortCol == '[object Screen]':
        sortCol = 'Screen'
    if(sortCol != '' and sortCol == request.session.get('sortCol','')):
        sortCol = '-' + sortCol
    request.session['sortCol'] = sortCol
    logData = __getLogData__(filterData, sortCol)
    paginator = Paginator(logData, settings.PAGE_SIZE)
    page_range = paginator.page_range

    if pageNo != 0:
        page_data = paginator.page(int(pageNo))
        logData = page_data.object_list
    return render_to_response('Logs.html', {'title': title,
        'page_list':logData, 'header_cols':header_cols,
        'page_range': page_range, 'log':filterData,
        'userName':userName,
        }, context_instance = RequestContext(request))

def __getLogData__(filterData, sortCol):
    if filterData == None:
        module = LOG_TYPE['AuditLog']
    else:
        module = LOG_TYPE[filterData['logType']]
    moduleLog = module.objects.all()
    if filterData != None:
        if((filterData['fromDate'] != '') and (filterData['toDate'] != '')):
            startDt = GetDateType(filterData['fromDate'])
            endDt = GetDateType(filterData['toDate'])
            endDt = endDt + datetime.timedelta(hours = 24)
            moduleLog = moduleLog.filter(timeStamp__range = (startDt, endDt))
    return moduleLog.order_by(SORTING_COLS[sortCol])

def __getFilterData__(request):
    filterData = { 'client': request.POST.get('client', ''),
                    'logType': request.POST.get('logType', ''),
                    'users' : request.POST.get('users', ''),
                    'fromDate' : request.POST.get('fromDate', ''),
                    'toDate' : request.POST.get('toDate', ''),
                }
    return filterData

def __getUsers__(models):
    Users = [model.users for model in models.objects.all()]
    return set(Users)

def __getClient__(models):
    clients = [model.client for model in models.objects.all()]
    return set(clients)

@permission_required('log.add_errorlog')
def GetLog(request):
    logID = request.GET.get('ids', '')
    logtype = request.GET.get('logType', '')
    userName = ''
    LoginData = request.session.get('LoginData','')
    if LoginData != '':
        userName = LoginData['userName']
    if userName:
        userName = userName[0]
    module = LOG_TYPE[logtype]
    moduleLog = module.objects.filter(pk = logID)
    if moduleLog:
        moduleLog = moduleLog[0]
#   log = logType.objects.filter(pk = logID)
    return render_to_response('LogPopUp.html',
        {'title': 'Log Detail', 'userName':userName,
        'log':moduleLog, 'Type':logtype })
