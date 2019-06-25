from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext as _

from project_management.milestone.models import Milestone
from project_management.notifications.icalendar import createics
from project_management.notifications.models import Event
from project_management.projects.models import Project
from project_management.templatecalendar import month_cal, getToday, __getTimes__,__getTimezone__, getEventTimes, \
    adjust_datetime_to_timezone
from project_management.Utility import GetDateType, getUserTypeFilter
from project_management.logs.logger import CapturLog

from datetime import date, timedelta, datetime

ACTION_MESSAGE = {
    'Default'     :'',
    'Save'      :_('Event saved successfully'),
    'Access'        :_('Access Denied'),
    'PASTDATE'      :_('Event cannot be created/updated for the past date'),
    'PASTTIME'      :_('Event cannot be created/updated for the past time'),
    'List'              :_('Event listed successfully'),
    'ListErr'           :_('Event list unsuccessful'),
    'Create'            : _('Create'),
    'Add'               : _('Create'),
    'CreateError'       : _('Create unsuccessful'),
    'Update'            : _('Update'),
    'UpdateError'       : _('Update unsuccessful'),
    'Delete_Success'    :_('Event deleted successfully'),
    'Delete_Unsuccess':_('Event is dependent. Cannot be deleted.'),
    'Delete_Create':_('Only saved event can be deleted.'),
    }

MODULE = 'Event'
FROMTIMEZONE = 'Etc/GMT'
TOTIMEZONE = 'UTC'
CURRENT_DATE = datetime.now()
ERROR_MESSAGE = '%s\n%s\n%s'
errMessage = ''

COUNTRYTIMEZONE = {
    '-5:30':'Asia/Calcutta',
    '-6:30':'Asia/Rangoon',
    '+9:30':'Australia/Adelaide',
    '+4:30':'Asia/Kabul',
    '+5.45':'Asia/Katmandu',
    '+3.30':'Asia/Tehran'
    }



def __getEvent__(request):
    logindata = request.session['LoginData']
    user = logindata['loginUserProfile']
    fiveGUser = [request.user]
    #fiveGUser = FiveGUser.objects.filter(userProfile
    #                = logindata['loginUserProfile'])
    fiveGUser_id = fiveGUser[0].pk if len (fiveGUser) > 0 else ''
    eventdata = Event (
                name = request.POST.get('txtname', ''),
                place = request.POST.get('txtplace', ''),
                program_id = request.POST.get('ddlproject', '0'),
                stage_id = request.POST.get('ddlstage', '0'),
                eventType = request.POST.get('ddltype', ''),
                eventDt = GetDateType(request.POST.get('txtdate', '')),
                startTime = request.POST.get('starttime', ''),
                endTime = request.POST.get('endtime', ''),
                message = request.POST.get('txtmessage', ''),
                creator_id = fiveGUser_id,
                cancel = 0
                )
    event_id = request.POST.get('txteventID', '')
    if event_id:
        eventdata.pk = event_id
    return eventdata

def __getPreEventData__(request):
    preEvent = None
    ACTION = 'Create'
    try:
        preEvent = Event.objects.filter(pk
                        = request.POST.get('txteventID', ''))
        preEvent = preEvent[0] if len(preEvent) > 0 else None
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(request, ACTION+'Err', MODULE, errMessage)
    finally:
        return preEvent

def __checkCurrentTime__(request, eventdate, eventtime):
    FROMTIMEZONE = __getTimezone__(request)
    nowutctime = adjust_datetime_to_timezone(CURRENT_DATE, settings.TIME_ZONE,
                                                                TOTIMEZONE)
    nowutctime = adjust_datetime_to_timezone(nowutctime, TOTIMEZONE,
                                                                FROMTIMEZONE)
    if (nowutctime.year < 1900):
        nowutctime = nowutctime - timedelta(1)
    if (nowutctime.year == 1900 and nowutctime.day > 1):
        nowutctime = nowutctime + timedelta(1)
    timeF = '%I:%M %p'
    starttime = eventtime
    dt = datetime.strptime(starttime, timeF)
    eventdt = datetime.strptime(str(eventdate), "%Y-%m-%d")
    hour = int(dt.strftime('%H'))
    eventdt = eventdt + timedelta(hours =  hour)
    eventdt = eventdt + timedelta(minutes =  int(dt.strftime('%M')))

    diffmonth = nowutctime.month - eventdt.month
    diffyear = nowutctime.year - eventdt.year
    diffdays =  nowutctime.day - eventdt.day
    diffhour =  nowutctime.hour - eventdt.hour
    diffminute =  nowutctime.minute - eventdt.minute

    if (diffdays >= 0 and diffmonth >= 0 and diffyear >= 0):
        if (diffhour > 0 or (diffhour >= 0 and diffminute > 0)):
            return False
    return True

def __geteventdatetime__(request, eventDt, startTime, endTime):
    FROMTIMEZONE = __getTimezone__(request)
    tempst = datetime.strptime(startTime,'%I:%M %p')
    tempst = tempst.strftime('%H:%M')
    tempst = datetime.strptime(tempst,'%H:%M')

    utctime = adjust_datetime_to_timezone(tempst, FROMTIMEZONE, TOTIMEZONE)
    settingtime = adjust_datetime_to_timezone(utctime, TOTIMEZONE,
                                                        FROMTIMEZONE)

    if (utctime.year < 1900):
        utctime = utctime + timedelta(1)
        eventDt = eventDt - timedelta(1)
    startTime = utctime.strftime('%H:%M')
    if (utctime.day > 1):
        eventDt = eventDt + timedelta(1)

    tempet = datetime.strptime(endTime,'%I:%M %p')
    tempet = tempet.strftime('%H:%M')
    tempet = datetime.strptime(tempet,'%H:%M')
    utcetime = adjust_datetime_to_timezone(tempet, FROMTIMEZONE, TOTIMEZONE)
    settingtime = adjust_datetime_to_timezone(utcetime, TOTIMEZONE,
                                                                FROMTIMEZONE)
    if (utcetime.year < 1900):
        utcetime = utcetime + timedelta(1)
    endTime = utcetime.strftime('%H:%M')
    return eventDt, startTime, endTime

#def __getAttendees__(request, logindata, pk):
#    selected_resources = request.POST.getlist('selectedresources') + request.POST.getlist('ext_selectedresources')
#    seletedResources = set([FiveGUser.objects.get(userID = ID)
#                            for ID in selected_resources])
#    existingAssignees = set([each.user
#            for each in EventAttendee.objects.filter(event = pk)])
#    loginuser = FiveGUser.objects.get(userProfile
#                                = logindata['loginUserProfile'])
#    seletedResources =  seletedResources | set([loginuser])
#
#    deleteAssignees = set(existingAssignees) - set (seletedResources)
#    insertAssignees = set (seletedResources) - set(existingAssignees)
#
#    return deleteAssignees, insertAssignees

def getStage(request):
    project_id = request.GET.get('projectID')
    if project_id != '0':
        project =  get_object_or_404(Project, pk = project_id)
        milestones = project.milestone.filter(category
                                    = Milestone.category_choices[1][1])
        event_team = project.team.all()
    else:
        milestones = Milestone.objects.none()
        event_team = FiveGUser.objects.all()
        event_team = User.objects.all()
    stages = [{'name':each.name, 'id':each.pk} for each in milestones]
    team = [{'name':user.name, 'sysuserType': user.sysuserType, 'id':user.pk}
                for user in event_team]
    json = simplejson.dumps([stages, team])
    return HttpResponse(json, mimetype='application/json')

def saveEvent(request):
    action = 'Default'
    profile = request.user.get_profile()
    preeventdata = __getPreEventData__(request)
    eventdata = __getEvent__(request)
    if(profile == '0'):
        CapturLog().LogData(request, 'Save', MODULE, ACTION_MESSAGE['Access'])
        return Events(request,'Access')
    eventaction = 'create' if(eventdata.pk == '') else 'modify'
    #serprofile = FiveGUser.objects.get(userProfile
    #                   = logindata['loginUserProfile'])
    #ventteam = EventAttendee.objects.filter(user = userprofile,
    eventteam = EventAttendee.objects.filter(user = request.user,
                                        event = eventdata)
    if (len(eventteam) <= 0):
        CapturLog().LogData(request, 'Save', MODULE,
                                    ACTION_MESSAGE['Access'])
        return Events(request, 'Access', eventdata.eventID)

    else:
        CapturLog().LogData(request, 'Save', MODULE, ACTION_MESSAGE['Access'])
        return Events(request, 'Access', eventdata.eventID)

    ispasttime = __checkCurrentTime__(request, eventdata.eventDt,
                                                eventdata.startTime)
    if (ispasttime == False):
        return Events(request, 'PASTTIME', eventdata.pk)

    eventdata.eventDt, eventdata.startTime, eventdata.endTime = __geteventdatetime__(request, eventdata.eventDt, eventdata.startTime, eventdata.endTime)
    eventdata.save()
    insetAssignees = request.POST.get('selectedresources', '')
    #    deleteAssignees, insertAssignees = __getAttendees__(request,
    #                                            logindata, eventdata.pk)
    [EventAttendee.objects.filter(event = eventdata, user = each).delete()
                                            for each in deleteAssignees]
    [EventAttendee(event = eventdata, user = each).save()
                                            for each in insertAssignees]

    otherAttendees = request.POST.getlist('otherAttendees')
    [each.delete() for each in EventOtherAttendee.objects.filter(event
                                                            = eventdata)]
    [EventOtherAttendee(event = eventdata, otheruser = each).save()
                                                for each in otherAttendees]
    createics(eventdata.pk, otherAttendees, request)
    action = 'Update' if preeventdata != None else 'Create'
    CapturLog().LogData(request, 'Save', MODULE, ACTION_MESSAGE['Save'],
                                                eventdata, preeventdata)
    try:
        pass
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(request, action + 'Err', MODULE, errMessage)
    return MonthlyCalendar(request, msg='Save')

def updateEvent(request):
    return Events(request)

def accessEvent(request):
    return Events(request,'PASTDATE')

def Events(request, action='Default', eventpk = None, eventattendees = '', actiontype = ''):
    try:
        project_id = stage_id = ''
        stages = []
        logindata = request.session.get('LoginData','')
        profile = logindata['loginUserProfile']
        if not eventpk :
            if request.GET.get('eventid','') != '':
                eventpk = request.GET.get('eventid', None)
            else:
                eventpk = request.GET.get('ids', None)
        todaydate = request.GET.get('selecteddate','')
        times, currentdate = getToday(request)
        allattendees = FiveGUser.objects.all().exclude(cancel
                                = '1').exclude(status='0')
        eventAttendeesset = [each.user
                for each in EventAttendee.objects.filter(event = eventpk)]

        attendees = set(allattendees) - set (eventAttendeesset)

        int_attendees, ext_attendees = getUserTypeFilter (attendees)
        int_eventattendees, ext_eventattendees = getUserTypeFilter (eventAttendeesset)
        program = Project.objects.all().exclude(cancel = '1').exclude(pk
                                                                = '0').order_by('name')
        eventattendees = EventAttendee.objects.filter(event=eventpk)
        eventotherattendees = EventOtherAttendee.objects.filter(event=eventpk)
        try:
            events = Event.objects.get(eventID=eventpk)
            actiontype = 'Update' if events else 'Create'
        except:
            events = None
            actiontype = 'Create'
        times = __getTimes__()
        if (events):
            try:
                stages = events.program.milestone.all()
            except:
                stages = Milestone.objects.none()
            events.startTime, events.eventDt = getEventTimes(request,
                                events.startTime, events.eventDt, True)
            events.endTime, events.eventDt = getEventTimes(request,
                                events.endTime, events.eventDt, False)
            try:
                project_id = events.program.pk
            except:
                project_id = '0'
            try:
                stage_id = events.stage.pk
            except:
                stage_id = '0'
            if project_id != '0':
                int_attendees = set(events.program.team.filter(sysuserType
                                    = 'Internal')) - set(int_eventattendees)
                ext_attendees = set(events.program.team.filter(sysuserType
                                    = 'External')) - set(ext_eventattendees)
            if not times.__contains__(events.startTime):
                times.append(events.startTime)
            if not times.__contains__(events.endTime):
                times.append(events.endTime)
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(request, actiontype+'Err', MODULE, errMessage)
    else:
        CapturLog().LogData(request, actiontype, MODULE, ACTION_MESSAGE[actiontype])

    return render_to_response('EventEditor.html', {
        'msg':ACTION_MESSAGE[action], 'currentdate':currentdate,
        'events':events, 'eventattendees':int_eventattendees,
        'program':program, 'times':times, 'attendees':int_attendees,
        'ext_eventattendees':ext_eventattendees, 'ext_attendees':ext_attendees,
        'eventotherattendees':eventotherattendees, 'stages':stages,
        'projectID':project_id, 'stageID':stage_id,
        'todaydate':todaydate,
        'action':actiontype, 'title': 'Event', 'profile':profile},
        context_instance = RequestContext(request) )

def __getActionValid__(request):
    logindata = request.session.get('LoginData','')
    userprofile = [request.user]
	#    userprofile = FiveGUser.objects.filter(userProfile
	#                                = logindata['loginUserProfile'])
    userprofile = userprofile[0] if len (userprofile) > 0 else None
    return userprofile, logindata, True, True



def MonthlyCalendar(request, msg = 'Default'):
    userprofile, logindata, isValid, accessAll = __getActionValid__(request)
    result = month_cal(CURRENT_DATE.year, CURRENT_DATE.month, isValid,
                                            accessAll, userprofile, request)
    request.session["years"]  = CURRENT_DATE.year
    request.session["months"] = CURRENT_DATE.month
    request.session["days"] = CURRENT_DATE.day
    times, today = getToday(request)
    return render_to_response('MonthlyCalendar.html', {
        'today':today, 'msg': ACTION_MESSAGE[msg],
        'calendar': result['calendar'], 'userName':logindata['userName'][0] ,
        'headers': result['headers'], 'monthyear': result['monthyear'],
        'monthdata': result['monthdata']},
        context_instance = RequestContext(request))

def WeeklyCalendar(request):
    request.session["weekyears"]  = CURRENT_DATE.year
    request.session["weekmonths"] = CURRENT_DATE.month
    request.session["weekdays"] = CURRENT_DATE.day
    return showweekcalendar(request, CURRENT_DATE.year, CURRENT_DATE.month,
                                                        CURRENT_DATE.day)

def showweekcalendar(request, year='2000', month='01', day='01'):
    userprofile, logindata, isValid, accessAll = __getActionValid__(request)
    if "weekmonths" in request.session and   "weekdays" in request.session:
        year = int(request.session["weekyears"])
        month = int(request.session["weekmonths"])
        day = int(request.session["weekdays"])
    result = weekly_cal(year, month, day, isValid,
                        accessAll, userprofile, request)
    return render_to_response('WeeklyCalendar.html', {
    'userName':logindata['userName'][0] ,
    'calendar': result['calendar'], 'headers': result['headers'],
    'monthyear': result['monthyear'], 'monthdata': result['monthdata'],
    'timedata':result['timedata'], 'eventfirstdatatime':result['eventfirstdatatime'],
    'eventsecdatatime':result['eventsecdatatime'],
    'eventthirddatatime':result['eventthirddatatime'],
    'eventfourthdatatime':result['eventfourthdatatime'],
    'eventfifthdatatime':result['eventfifthdatatime'],
    'eventsixthdatatime':result['eventsixthdatatime'],
    'eventseventhdatatime':result['eventseventhdatatime']},
     context_instance = RequestContext(request))

def DayCalendar(request):
    request.session["todayyears"]  = CURRENT_DATE.year
    request.session["todaymonths"] = CURRENT_DATE.month
    request.session["todaydays"] = CURRENT_DATE.day
    return showdaycalendar(request, CURRENT_DATE.year, CURRENT_DATE.month,
                                                        CURRENT_DATE.day)

def showdaycalendar(request, year='2000', month='01', day='01'):
    userprofile, logindata, isValid, accessAll = __getActionValid__(request)
    if "todayyears" in request.session and   "todaydays" in request.session:
        year = int(request.session["todayyears"])
        month = int(request.session["todaymonths"])
        day = int(request.session["todaydays"])
    result = day_cal(year, month, day, isValid,
                    accessAll, userprofile, request)
    return render_to_response('DayCalendar.html', {
        'userName':logindata['userName'][0] , 'calendar': result['calendar'],
        'headers': result['headers'], 'monthyear': result['monthyear'],
        'monthdata': result['monthdata'], 'timedata':result['timedata']},
         context_instance = RequestContext(request))

def showcalendar(request):
    try:
        years = int(request.session["years"])
        months = int(request.session["months"])
        userprofile, logindata, isValid, accessAll = __getActionValid__(request)
        result = month_cal(int(years), int(months),
                    isValid, accessAll, userprofile, request)
        return render_to_response('MonthlyCalendar.html', {
            'userName':logindata['userName'][0] , 'today':CURRENT_DATE.date(),
            'calendar': result['calendar'], 'headers': result['headers'],
            'monthyear': result['monthyear'], 'monthdata': result['monthdata']},
             context_instance = RequestContext(request))
    except:
        return render_to_response('MonthlyCalendar.html',
            {'error_message': "You didn't enter year and month",})

NEXT_YEAR_CALENDER_TYPE = { 'month': 'years', 'week': 'weekyears',
                            'day': 'todayyears' }
def previousyear(request, type=""):
    if NEXT_YEAR_CALENDER_TYPE[type] in request.session:
        request.session[NEXT_YEAR_CALENDER_TYPE[type]] = int(
            request.session[NEXT_YEAR_CALENDER_TYPE[type]])-1
    if type == 'month':
        return showcalendar(request)
    elif type == 'day':
        return showdaycalendar(request)
    return showweekcalendar(request)

def nextyear(request, type=""):
    if NEXT_YEAR_CALENDER_TYPE[type] in request.session:
        request.session[NEXT_YEAR_CALENDER_TYPE[type]] = int(
            request.session[NEXT_YEAR_CALENDER_TYPE[type]])+1
    if type == 'month':
        return showcalendar(request)
    elif type == 'day':
        return showdaycalendar(request)
    return showweekcalendar(request)

def previousmonth(request):
    if "months" in request.session:
        if (int(request.session["months"]) != 1):
            request.session["months"] = int(request.session["months"])-1
        else:
            request.session["months"] = 12
            request.session["years"] = int(request.session["years"])-1
    return showcalendar(request)

def nextmonth(request):
    if "months" in request.session:
        if (int(request.session["months"]) != 12):
            request.session["months"] = int(request.session["months"])+1
        else:
            request.session["months"] = 1
            request.session["years"] = int(request.session["years"])+1
    return showcalendar(request)

def __getDays__(request, days):
    if "todaydays" in request.session:
        year =  int(request.session["todayyears"])
        month = int(request.session["todaymonths"])
        day = int(request.session["todaydays"])
        dt = date(year, month, day)
        dt  = dt + timedelta(days = days)
        request.session["todayyears"] = dt.year
        request.session["todaymonths"] = dt.month
        request.session["todaydays"] = dt.day

def nextday(request):
    __getDays__(request, 1)
    return showdaycalendar(request)

def previousday(request):
    __getDays__(request, -1)
    return showdaycalendar(request)

def __getWeeks__(request, days):
    if "weekdays" in request.session:
        year =  int(request.session["weekyears"])
        month = int(request.session["weekmonths"])
        day = int(request.session["weekdays"])
        dt = date(year, month, day)
        dt  = dt + timedelta(days = days)
        request.session["weekyears"] = dt.year
        request.session["weekmonths"] = dt.month
        request.session["weekdays"] = dt.day

def nextweek(request):
    __getWeeks__(request, 7)
    return showweekcalendar(request)

def previousweek(request):
    __getWeeks__(request, -7)
    return showweekcalendar(request)

def eventDeleteModels(eventToDelete):
    msg = 'Delete_Unsuccess'
    for each in eventToDelete:
        if (each != ''):
            event = Event.objects.get(eventID = each)
            event.cancel = 1
            event.save()
            msg = 'Delete_Success'
    return msg

def eventDelete(request):
    ACTION = 'Delete'
    msg = 'Default'
    try:
        if request.method == 'POST':
            eventsToDelete = request.POST.getlist('deleteChecked')
            eventToDelete = eventsToDelete if len(eventsToDelete) > 0 else [request.POST.get('txteventID', '')]
            msg = eventDeleteModels(eventToDelete) if len(eventToDelete) > 0 else 'Delete_Create'
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(request, ACTION, MODULE, errMessage)
    finally:
        return MonthlyCalendar(request, msg=msg)
