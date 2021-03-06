import vobject
import datetime
from pytz import timezone

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from project_management.conferenceroombooking.models import *
#from project_management.clientUsers.models import UserProfile
from project_management.users.models import *
from project_management.Utility import Email, Util
from project_management.logs.logger import CapturLog
from project_management.templatecalendar import getEventTimes, adjust_datetime_to_timezone, __getTimezone__

EVENT_ITEMS = (
    ('uid', 'item_uid'),
    ('dtstart', 'item_start'),
    ('dtend', 'item_end'),
    ('summary', 'item_summary'),
    ('description', 'item_description'),
    ('location', 'item_location'),
    ('DTSTAMP', 'item_Dtstamp'),
)

EVENT_VTIMEZONE = (
    ('DTSTART', 'item_DTStart'),
    ('TZOFFSETTO', 'item_TZoffsetto'),
    ('TZOFFSETFROM', 'item_TZoffsetfrom'),
)

MODULE = 'Event'


def setUTCTimeZone(request, eventdt, eventTime):
    print ' method called '
    timeF = '%I:%M %p'
    dt = datetime.datetime.strptime(eventTime, timeF)
    eventdt = eventdt + datetime.timedelta(hours=int(dt.strftime('%H')))
    eventdt = eventdt + datetime.timedelta(minutes=int(dt.strftime('%M')))
    eventdt = adjust_datetime_to_timezone(
        eventdt, __getTimezone__(request), 'UTC')
    return eventdt


class createics:
    """
    >>>
    """

    def __init__(self, eventid, otherids, request):
        self.eventid = eventid
        self.otherids = otherids
        self.request = request
        print 'Called !'
        self.sendingIds, self.sendingIdsPwd = self.mailIDs(eventid, otherids)
        self.tzone = self.getLocalTimezone(self.request)
        self.tzoffset = self.getLocalTimezoneOffset(self.request)
        print 'self.sendingIds ', self.sendingIds
        print 'sendingIdsPwd ', self.sendingIdsPwd
        if len(self.sendingIds) > 0:
            self.__createICS__()
        return

    def item_uid(self, item):
        return item.eventID

    def item_start(self, item):
        eventdt = setUTCTimeZone(self.request, item.eventDt, item.startTime)
        return eventdt

    def item_end(self, item):
        eventdt = setUTCTimeZone(self.request, item.eventDt, item.endTime)
        return eventdt

    def item_summary(self, item):
        return item.name

    def item_location(self, item):
        return item.place

    def item_description(self, item):
        return item.message

    def item_Dtstamp(self, item):
        return item.eventDt

    def item_TZoffsetto(self):
        return '0000'  # self.tzoffset

    def item_TZoffsetfrom(self):
        return '0000'  # self.tzoffset

    def item_DTStart(self):
        return datetime.datetime.now()

    def __createICS__(self):
        try:
            cal = vobject.iCalendar()
            cal.add('method').value = 'PUBLISH'

            item = Event.objects.get(pk=self.eventid)
            item.startTime, item.eventDt = getEventTimes(
                self.request, item.startTime, item.eventDt, True)
            item.endTime, item.eventDt = getEventTimes(
                self.request, item.endTime, item.eventDt, False)

            vEvent = cal.add('vevent')
            for vkey, key in EVENT_ITEMS:
                value = getattr(self, key)(item)
                if value:
                    vEvent.add(vkey).value = value

            vtzone = cal.add('vtimezone')
            vtzone.add('TZID').value = 'UTC'  # self.tzone
            VtimeDet = vtzone.add('STANDARD')
            for vkey, key in EVENT_VTIMEZONE:
                value = getattr(self, key)()
                if value:
                    VtimeDet.add(vkey).value = value

            response = HttpResponse(cal.serialize())
            strdata = str(response)
            RESPONSE_HDR_TXT = 'Content-Type: text/html; charset=utf-8'
            if (strdata.__contains__(RESPONSE_HDR_TXT)):
                strdata = strdata.replace(RESPONSE_HDR_TXT, '')
            eventpath = settings.EVENT_PATH + '/Event.ics'
            w = open(eventpath, "w")
            w.write(strdata)
            w.close()
            Email().send_email(item.name, item.message, self.sendingIds, '', eventpath)
            for each in self.sendingIdsPwd:
                user = User.objects.filter(email=each)
                pwd = Util().Guid()[:6]
                email_message = ''
                if len(user) > 0:
                    user[0].set_password(pwd)  # setting the encrypted PWD
                    user[0].save()
                    email_message = settings.EMAIL_MESSAGE % (
                        user[0].email, pwd)
                email_message = email_message + '\n' + item.message
                Email().send_email(
                    item.name, email_message, [
                        each, ], '', eventpath)
        except Exception:
            errMessage = 'Email Sending failed \n %s' % (Exception)
            CapturLog().LogData(request, 'E-MailError', MODULE, errMessage)
        else:
            CapturLog().LogData(request, 'E-Mail', MODULE, 'Email sent successfully')
        finally:
            return ''

    def mailIDs(self, eventid, otherids):
        """
        >>>
        """
        eventusers = EventAttendee.objects.filter(event=eventid)
        sendingIDS = []
        sendingIDSPWD = []
        if (len(eventusers) > 0):
            fundausers = [
                FundaUser.objects.filter(
                    pk=each.user_id) for each in eventusers]
            userprofiles = [
                UserProfile.objects.get(
                    pk=each[0].userProfile_id) for each in fundausers]
            users = [User.objects.get(pk=each.authUser_id)
                     for each in userprofiles]
            emailID = '%s'
            for each in users:
                forgotans = ForgotPasswordAnswer.objects.filter(user=each)
                if len(forgotans) <= 0:
                    sendingIDSPWD.append(each.email)
                else:
                    sendingIDS.append(emailID % (each.email))

            sendingIDS = sendingIDS + [emailID % (each) for each in otherids]
        return sendingIDS, sendingIDSPWD

    def getLocalTimezone(self, request):
        logindata = request.session['LoginData']
        offset = logindata['localTimeZone']
        if (offset is None or offset == ''):
            offset = 0
        offsetmod = abs(int(offset)) % 60
        offset = float(offset) / 60.0
        offset = int(offset)
        data = str(offset) + '.' + str(offsetmod)
        data = data if(offsetmod > 0) else str(abs(offset))
        TIMEZONE = ('GMT+' if (offset > 0) else 'GMT') + data
        return TIMEZONE

    def getLocalTimezoneOffset(self, request):
        logindata = request.session['LoginData']
        offset = logindata['localTimeZone']
        if (offset is None or offset == ''):
            offset = 0
        offsetmod = abs(int(offset)) % 60
        offset = float(offset) / 60.0
        offset = int(offset)
        data = str(offset) + '.' + str(offsetmod)
        data = data if(offsetmod > 0) else str(abs(offset))
        timeZoneOffset = '+' + data if (offset > 0) else data
        return timeZoneOffset
