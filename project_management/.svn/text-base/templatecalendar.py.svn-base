from django import template
from django.utils.translation import ugettext as _
from django.conf import settings
from django.utils.encoding import smart_str

from project_management.Utility import flatten
from project_management.conferenceroombooking.models import ConferenceRoom, BookConference
from django.contrib.auth.models import User
from datetime import date, timedelta, datetime
import time
import pytz

FROMTIMEZONE = 'Etc/GMT'
TOTIMEZONE = 'UTC'

COUNTRYTIMEZONE = { '-5:30':'Asia/Calcutta',
'-6:30':'Asia/Rangoon',
'+9:30':'Australia/Adelaide',
'+4:30':'Asia/Kabul',
'+5.45':'Asia/Katmandu',
'+3.30':'Asia/Tehran'}

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December']
register = template.Library()

def get_last_day_of_month(year, month):
    """
    >>>
    """
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)

def get_times2():
    times = []
    for hour in range(0, 9):
        for min in ('00', '30'):
            times.append('0%d:%s' %(hour, min))
    for hour1 in range(10, 24):
        for min1 in ('00', '30'):
            times.append('%d:%s' %(hour1, min1))
    return times


def __getTimes__():
    return get_times2()
    dtstart = datetime( 1900, 01, 01, 0, 0, 0, 0 )
    dtend = datetime( 1900, 01, 01, 23, 0, 0, 0 )
    times = []
    times.append(dtstart.strftime("%I:%M %p"))
    while dtstart <= dtend:
        dtstart = dtstart + timedelta(minutes=30)
        times.append(dtstart.strftime("%I:%M %p"))
    return times

def month_cal (year, month,request = None):
    event_list = []
    apex_body_owner = User.objects.filter(groups__name__icontains = 'Corporate Admin', is_active = True)
    event_list = BookConference.objects.filter(meeting_date__year = year, meeting_date__month = month).exclude(is_approved = 0)	#eventDt__month=month
    for each in apex_body_owner:
        if each.username == str(request.user):
            event_list = BookConference.objects.filter(meeting_date__year = year, meeting_date__month = month).all()
    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())
    month_cal = []
    week = []
    week_headers = []
    
    for each in event_list:
        dummystartTime, each.meeting_date = getEventTimes(request, each.from_time, each.meeting_date, True)
    monthyear = _(MONTHS[month-1])+' '+str(year)
    i = 0
    day = first_day_of_calendar
    daytime = datetime(day.year, day.month, day.day, 0, 0, 0, 0)
    monthdata = []
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['event'] = False
        
        for event in event_list:
            daydata = {}               
            daydata['desc'] = event.name_of_meeting[0:10]+'..,'
            daydata['day'] = day
            daydata['eventid'] = event.id
            daydata['start_date'] = event.meeting_date
            daydata['is_approved'] = event.is_approved
            cal_day['event'] = True
            monthdata.append(daydata)
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False
        week.append(cal_day)
        if day.weekday() == 6:
            month_cal.append(week)
            week = []
        i += 1
        day += timedelta(1)
        daytime += timedelta(1)
    return {'calendar': month_cal, 'headers': week_headers,
    'monthyear': monthyear, 'monthdata':monthdata}

#def weekly_cal (year, month, day, request = None):
#    event_list = []
#    first_day_of_month = date(year, month, day)
#    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
#    last_day_of_week = first_day_of_calendar+timedelta(6)
#    timedata = __getTimes__()
#    month_cal = []
#    week = []
#    week_headers = []
#
#    monthyear = _(MONTHS[month-1])+' '+str(year)
#    i = 0
#    j = 0
#    day = first_day_of_calendar
#    daytime = datetime(day.year, day.month, day.day, 0, 0, 0, 0)
#
#    eventfirstdatatime = {}
#    eventsecdatatime = {}
#    eventthirddatatime = {}
#    eventfourthdatatime = {}
#    eventfifthdatatime = {}
#    eventsixthdatatime = {}
#    eventseventhdatatime = {}
#
#    while j < len(timedata):
#        strval = timedata[j]
#        eventfirstdatatime[strval] = ""
#        eventsecdatatime[strval] = ""
#        eventthirddatatime[strval] = ""
#        eventfourthdatatime[strval] = ""
#        eventfifthdatatime[strval] = ""
#        eventsixthdatatime[strval] = ""
#        eventseventhdatatime[strval] = ""
#        j = j+1
#
#    event_list = BookConference.objects.filter(meeting_date__year = year, meeting_date__month = month).exclude(is_approved = 0)	#eventDt__month=month
#    
#    for event in event_list:
#        if (event != None and  len(event) > 0):
#            event = event[0]
#            dummystartTime, event.meeting_date = getEventTimes(request, event.from_time, event.meeting_date, True)
#
#    monthdata = []
#    while day <= last_day_of_week:
#        if i < 7:
#            week_headers.append(day)
#        dayformat = datetime(day.year, day.month, day.day, 0, 0, 0, 0)
#
#        event_list = list(flatten(event_list))
#        if (isValid):
#            for event in event_list:
#                if daytime >= event.eventDt and daytime <= event.eventDt:
#
#                    j = 0
#                    while j < len(timedata):
#                        times = datetime.strptime(timedata[j], "%I:%M %p")
#                        timestart = getEventDayTimes(request, event.startTime)
#                        timeend = getEventDayTimes(request, event.endTime)
#                        strval = timedata[j]
#                        desc = "<a href='/UpdateEvent/?eventid=%s' > %s </a>"
#                        times = times.strftime('%I:%M %p')
#                        time1 = time.strptime(times,"%I:%M %p")
#                        time2 = time.strptime(timestart,"%I:%M %p")
#                        time3 = time2
#
#                        if j+1 < len(timedata):
#                            time3 = time.strptime(timedata[j+1], "%I:%M %p")
#                        elif j+1 == len(timedata):
#                            time3 = time.strptime(timedata[0], "%I:%M %p")
#                        if time1 <= time2 and (time2 < time3 or (time3.tm_min == 0 and time3.tm_hour == 0)) :
#                        #if times == timestart and daytime == dayformat:
#                            desc =   desc % (event.pk, event.name[0:10]) +'..,'
#                            if (i == 0):
#                                eventfirstdatatime[strval] =  eventfirstdatatime[strval] + desc
#                            if(i == 1):
#                                eventsecdatatime[strval] =  eventsecdatatime[strval]  + desc
#                            if(i == 2):
#                                eventthirddatatime[strval] = eventthirddatatime[strval] + desc
#                            if(i == 3):
#                                eventfourthdatatime[strval] = eventfourthdatatime[strval]  + desc
#                            if(i == 4):
#                                eventfifthdatatime[strval] = eventfifthdatatime[strval] + desc
#                            if(i == 5):
#                                eventsixthdatatime[strval] =  eventsixthdatatime[strval] + desc
#                            if(i == 6):
#                                eventseventhdatatime[strval] = eventseventhdatatime[strval] + desc
#                        j = j+1
#
#        i += 1
#        day += timedelta(1)
#        daytime += timedelta(1)
#
#    return {'calendar': month_cal, 'headers': week_headers,
#    'monthyear': monthyear, 'monthdata':monthdata, 'timedata':timedata,
#    'eventfirstdatatime':eventfirstdatatime,
#    'eventsecdatatime':eventsecdatatime, 'eventthirddatatime':eventthirddatatime,
#    'eventfourthdatatime':eventfourthdatatime,
#    'eventfifthdatatime':eventfifthdatatime, 'eventsixthdatatime':eventsixthdatatime,
#    'eventseventhdatatime':eventseventhdatatime}
#
#def day_cal(year, month, day, isValid=False, accessAll=False, userprofile=None, request = None):
#    """
#    >>>
#    """
#    event_list = []#Event.objects.filter(eventDt__year=year, eventDt__month=month, eventDt__day=day)
#    month_cal = []
#    week = []
#    week_headers = []
#
#    timedata = __getTimes__()
#    monthyear = _(MONTHS[month-1])+' '+str(year)
#    i = 0
#    j = 0
#    day = date(year, month, day)
#    daytime = datetime(day.year, day.month, day.day, 0, 0, 0, 0)
#    week_headers.append(day)
#
#    eventdatatime = {}
#    while j < len(timedata):
#        strval = timedata[j]
#        eventdatatime[strval] = ""
#        j = j+1
#
#    if (isValid):
#        event_list = [Event.objects.filter(eventDt__year=day.year, eventDt__month=day.month).exclude(cancel = 1)]
#        if (accessAll == False):
#            event_list = [Event.objects.filter(eventDt__year=day.year,  pk= each.event_id, eventDt__month=day.month).exclude(cancel = 1)
#                for each in EventAttendee.objects.filter(user= userprofile)]
#
#        event_list = list(flatten(event_list))
#
#        for event in event_list:
#            dummystartTime, event.meeting_date = getEventTimes(request, event.from_date, event.meeting_date, True)
#
#        for event in event_list:
#            j = 0
#            while j < len(timedata):
#                times = datetime.strptime(timedata[j], "%I:%M %p")
#                timestart = getEventDayTimes(request, event.startTime)
#                timeend = getEventDayTimes(request, event.endTime)
#                strval = timedata[j]
#                desc = "<a href='/UpdateEvent/?eventid=%s' > %s </a>"
#                times = times.strftime('%I:%M %p')
#                time1 = time.strptime(times,"%I:%M %p")
#                time2 = time.strptime(timestart,"%I:%M %p")
#                time3 = time2
#
#                if j+1 < len(timedata):
#                    time3 = time.strptime(timedata[j+1], "%I:%M %p")
#                elif j+1 == len(timedata):
#                    time3 = time.strptime(timedata[0], "%I:%M %p")
#
#                if time1 <= time2 and event.eventDt.date() == day and (time2 < time3 or (time3.tm_min == 0 and time3.tm_hour == 0)) :
#                    desc =   desc % (event.pk, event.name[0:10]) +'.. '
#                    eventdatatime[strval] = eventdatatime[strval] + desc
#                j = j+1
#
#    return {'calendar': "", 'headers': week_headers, 'monthyear': monthyear,
#'monthdata':eventdatatime, 'timedata':timedata}

def getToday(request):
    gmtime = time.gmtime()
    data = str(gmtime.tm_hour)+':'+str(gmtime.tm_min)+':'+str(gmtime.tm_sec)
    times, today = getEventTimes(request, data, datetime.now().date(), True)
    return times, today

def getEventDayTimes(request, data):
    
    FROMTIMEZONE = __getTimezone__(request)
    starttime = str(data)
    tempst = datetime.strptime(starttime,'%H:%M:%S')
    data = adjust_datetime_to_timezone(tempst, TOTIMEZONE, FROMTIMEZONE)
    if (data.year < 1900):
        data = data + timedelta(1)
    data = data.strftime('%I:%M %p')
    return data

def getEventTimes(request, data, eventdate , firsttime):
    FROMTIMEZONE = __getTimezone__(request)
    starttime = str(data)
    tempst = datetime.strptime(starttime,'%H:%M:%S')
    data = adjust_datetime_to_timezone(tempst, TOTIMEZONE, FROMTIMEZONE)
    if (data.year < 1900):
        if (firsttime):
            eventdate = eventdate - timedelta(1)
        data = data + timedelta(1)
    if (data.year >= 1900 and data.day > 1 and firsttime):
        eventdate = eventdate + timedelta(1)
    data = data.strftime('%I:%M %p')

    return data, eventdate

def adjust_datetime_to_timezone(value, from_tz, to_tz=None):

    if to_tz is None:
        to_tz = settings.TIME_ZONE
    if value.tzinfo is None:
        if not hasattr(from_tz, "localize"):
            from_tz = pytz.timezone(smart_str(from_tz))
        value = from_tz.localize(value)
    return value.astimezone(pytz.timezone(smart_str(to_tz)))

def __getTimezone__(request):
    request.session['localTimeZone'] = request.POST.get('localTimeZone','')
    offset = request.session['localTimeZone']
    if (offset == None or offset == ''):
        offset  = 0
    offsetmod = abs(int(offset))%60
    offset = float(offset) / 60.0
    offset = int(offset)
    data = str(offset)+':'+str(offsetmod)
    if COUNTRYTIMEZONE.__contains__(data):
        FROMTIMEZONE = COUNTRYTIMEZONE[data]
    else:
        FROMTIMEZONE = 'Etc/GMT+' + str(abs(offset)) if (offset > 0) else 'Etc/GMT-' + str(abs(offset))

    return FROMTIMEZONE
