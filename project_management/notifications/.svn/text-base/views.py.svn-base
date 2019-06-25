from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.views.generic import list_detail

from project_management.notifications.models import Event
from project_management.notifications.forms import EventForm

def event_list(request):
    query = Q()
    searchtext = request.GET.get('search', '')
    if searchtext:
        for term in searchtext.split():
            q = Q(name__icontains = term)
        query = query & q
    event_set = Event.objects.filter(query)
    return list_detail.object_list(
        request,
        queryset = event_set,
        template_name = "event_list.html",
        template_object_name = "event",
        )

def manage_event(request, id = None, redirect_to = event_list):
    event = None
    if id:
        event = get_object_or_404(Event, pk = id)
    if request.method == 'POST':
        event_form = EventForm(request.POST, instance = event)
        if event_form.is_valid():
            event_form.save(user = request.user)
            messages.success(request, _('Event saved successfully.'))
            return HttpResponseRedirect(reverse(redirect_to))
    else:
        event_form = EventForm(instance = event)
    return render_to_response('event.html', {'event_form': event_form},
        context_instance = RequestContext(request))

def delete_event(request):
    if request.method == 'POST':
        business_unit_ids = request.POST.getlist('event_pk')
        Event.objects.filter(pk__in = business_unit_ids).delete()
        messages.success(request, _('Event(s) deleted sucessfully'))
    return HttpResponseRedirect(reverse(event_list))

#from django.shortcuts import render_to_response
#from django.template import RequestContext
#from django.utils.translation import ugettext as _
#
#from project_management.logs.logger import CapturLog
#from project_management.notifications.models import NotificationModule, \
#    NotificationConfig
#from project_management.projects.models import Project
##from project_management.projects.views import isActive
#
#ERROR_MESSAGE = '%s\n%s\n%s'
#MODULE = 'Alert Configuration'
#ACTION = 'Save'
#errMessage = ''
#msg = ''
#
#CONTROLS_PREFIX = {
#    'EMAIL':'chkEmail',
#    'SMS':'chkSMS',
#    'TEXT':'txt',
#    'TEXTPK':'txtpk'
#    }
#
#ACTION_MESSAGE = {
#    'Default':'',
#    'Alert Configuration': _('Alert Configuration'),
#    'Save'      :_('Alert configuration saved successfully'),
#    'ProjectInactive': _('Project/Project is inactive. Alert configuration cannot be saved.'),
#    'Access Denied': _('Access Denied'),
#    }
#
#def AlertConfiguration(request):
#    return __getAlertConfigData__(request)
#
#def SaveAlertConfiguration(request):
#    return __save__(request)
#
#def __getAlertConfigData__(request,action='Default'):
#    notificationList = NotificationModule.objects.all().order_by('notificationModuleID')
#    projectid = request.session.get('projectid', '0')
#    program = Project.objects.get(pk = projectid)
#    notificationconfig = NotificationConfig.objects.filter(program = program)
#    mod_list = []
#    logindata = request.session['LoginData']
#    try:
#        for each in notificationList:
#            message = ''
#            email = ''
#            pk = ''
#            if(len(notificationconfig) > 0):
#                notificationdata = notificationconfig.filter(notificationModule
#                                                = each.notificationModuleID )
#                message = notificationdata[0].message
#                pk = notificationdata[0].pk
#                if (notificationdata[0].email == 1):
#                    email = 'checked'
#            mod_list.append({'name': each,'message':message,'email':email,
#                'notificationModuleID':each.notificationModuleID, 'pk':pk })
#    except (RuntimeError, TypeError, NameError):
#        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
#        CapturLog().LogData(response, 'ListErr', MODULE, errMessage)
#    return render_to_response('Notification.html', {
#        'programid':'0', 'notificationconfig':notificationconfig,
#        'msg':ACTION_MESSAGE[action], 'notifications':mod_list,
#        'project': program,
#        'userName':logindata['userName'][0], 'action': 'Update'},
#        context_instance = RequestContext(request))
#
#def __save__(request):
#    flag = ''
#    msg = 'Default'
#    notificationrow = ''
#    notificationList = NotificationModule.objects.all().order_by('notificationModuleID')
#    try:
#        if(request.method == 'POST'):
#            program = Project.objects.get(pk = request.session.get('projectid', '0'))
#            flag = 1
#            for each in notificationList:
#                pkid = request.POST.get(str(CONTROLS_PREFIX['TEXTPK'] + each.notificationModuleID), '')
#                if (pkid.strip() == ''):
#                    notificationrow = NotificationConfig (
#                    notificationModule_id = each.notificationModuleID,
#                    program = program,
#                    message = request.POST.get(str(CONTROLS_PREFIX['TEXT'] + each.notificationModuleID), ''),
#                    SMS = request.POST.get(str(CONTROLS_PREFIX['SMS'] + each.notificationModuleID), ''),
#                    email = request.POST.get(str(CONTROLS_PREFIX['EMAIL'] + each.notificationModuleID), '')
#                    )
#                else:
#                    notificationrow = NotificationConfig (
#                    pk = pkid,
#                    notificationModule_id = each.notificationModuleID,
#                    program = program,
#                    message = request.POST.get(str(CONTROLS_PREFIX['TEXT'] + each.notificationModuleID), ''),
#                    SMS = request.POST.get(str(CONTROLS_PREFIX['SMS'] + each.notificationModuleID), ''),
#                    email = request.POST.get(str(CONTROLS_PREFIX['EMAIL'] + each.notificationModuleID), '')
#                    )
#                notificationrow.save()
#                msg = 'Save'
#    except (RuntimeError, TypeError, NameError):
#        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
#        CapturLog().LogData(request, 'SaveErr', MODULE, errMessage)
#    else:
#        if flag == 0:
#            CapturLog().LogData(request, 'Save', MODULE, ACTION_MESSAGE[msg])
#
#        else:
#            CapturLog().LogData(request, 'Save', MODULE, ACTION_MESSAGE[msg], notificationrow)
#    return __getAlertConfigData__(request, msg)
