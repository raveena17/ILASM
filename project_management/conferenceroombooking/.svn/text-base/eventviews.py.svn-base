from django.shortcuts import render_to_response, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_str
from django.utils import simplejson


from project_management.templatecalendar import month_cal,  getToday,\
				__getTimes__,__getTimezone__, getEventTimes, adjust_datetime_to_timezone


from datetime import date, timedelta, datetime
import time
import pytz

ACTION_MESSAGE = {'Default'    		:'',
				'Save'				:_('Event saved successfully'),				
				'Access'        	:_('Access Denied'),
				'PASTDATE'      	:_('Event cannot be created/updated for the past date'),
				'PASTTIME'      	:_('Event cannot be created/updated for the past time'),
				'List'              :_('Event listed successfully'),
				'ListErr'           :_('Event list unsuccessful'),
				'Create'            : _('Create'),
				'Add'               : _('Create'),
				'CreateError'       : _('Create unsuccessful'),                         
				'Update'            : _('Update'),
				'UpdateError'       : _('Update unsuccessful'),
				'Delete_Success'    :_('Event deleted successfully'),
				'Delete_Unsuccess'	:_('Event is dependent. Cannot be deleted.'),
				'Delete_Create'		:_('Only saved event can be deleted.'),
				}
				
MODULE = 'Event'
FROMTIMEZONE = 'Etc/GMT'
TOTIMEZONE = 'UTC'
CURRENT_DATE = datetime.now()
ERROR_MESSAGE = '%s\n%s\n%s'
errMessage = ''

COUNTRYTIMEZONE = { '-5:30':'Asia/Calcutta',
'-6:30':'Asia/Rangoon',
'+9:30':'Australia/Adelaide',
'+4:30':'Asia/Kabul',
'+5.45':'Asia/Katmandu',
'+3.30':'Asia/Tehran'}	
isValid = False

def MonthlyCalendar(request):
	result = month_cal(CURRENT_DATE.year, CURRENT_DATE.month, request)
	request.session["years"]  = CURRENT_DATE.year
	request.session["months"] = CURRENT_DATE.month
	request.session["days"] = CURRENT_DATE.day
	times, today = getToday(request)
	return render_to_response('MonthlyCalendar.html', {'page_name':'Monthly View', 'today':today, 
								'calendar': result['calendar'], 'headers': result['headers'], 
								'monthyear': result['monthyear'], 'monthdata': result['monthdata']},
								context_instance = RequestContext(request))

def WeeklyCalendar(request):	
	request.session["weekyears"]  = CURRENT_DATE.year
	request.session["weekmonths"] = CURRENT_DATE.month
	request.session["weekdays"] = CURRENT_DATE.day
	return showweekcalendar(request, CURRENT_DATE.year, CURRENT_DATE.month,CURRENT_DATE.day)	


def showweekcalendar(request,year='2000',month='01',day='01'):
	if "weekmonths" in request.session and   "weekdays" in request.session:
		year = int(request.session["weekyears"])
		month = int(request.session["weekmonths"])
		day = int(request.session["weekdays"])
	result = weekly_cal(year,month,day,request)
	return render_to_response('WeeklyCalendar.html', {'page_name':'Weekly View', 'calendar': result['calendar'], 
	'headers': result['headers'], 'monthyear': result['monthyear'], 'monthdata': result['monthdata'],
	'eventfirstdatatime':result['eventfirstdatatime'],
	'eventsecdatatime':result['eventsecdatatime'], 'eventthirddatatime':result['eventthirddatatime'], 
	'eventfourthdatatime':result['eventfourthdatatime'], 'eventfifthdatatime':result['eventfifthdatatime'], 
	'eventsixthdatatime':result['eventsixthdatatime'], 'eventseventhdatatime':result['eventseventhdatatime']},
	context_instance = RequestContext(request))
	
def DayCalendar(request):	
	request.session["todayyears"]  = CURRENT_DATE.year
	request.session["todaymonths"] = CURRENT_DATE.month
	request.session["todaydays"] = CURRENT_DATE.day
	return showdaycalendar(request,CURRENT_DATE.year,CURRENT_DATE.month,CURRENT_DATE.day)	

def showdaycalendar(request,year='2000',month='01',day='01'):
	if "todayyears" in request.session and  "todaydays" in request.session:
		year = int(request.session["todayyears"])
		month = int(request.session["todaymonths"])
		day = int(request.session["todaydays"])		
	result = day_cal(year,month,day,request)	
	return render_to_response('DayCalendar.html', {'page_name':'Daily View', 'calendar': result['calendar'], 
							'headers': result['headers'], 'monthyear': result['monthyear'], 
							'monthdata': result['monthdata']},context_instance = RequestContext(request))
	
def showcalendar(request):
	try:
		years = int(request.session["years"])
		months = int(request.session["months"])		
		result = month_cal(int(years),int(months), request)
		return render_to_response('MonthlyCalendar.html', {'page_name':'Monthly View', 'today':CURRENT_DATE.date(), 
								'calendar': result['calendar'], 'headers': result['headers'], 
								'monthyear': result['monthyear'], 'monthdata': result['monthdata']},
								context_instance = RequestContext(request))
	except:
		return render_to_response('MonthlyCalendar.html', {'page_name':'Monthly View',
							'error_message': "You didn't enter year and month"}, context_instance = RequestContext(request))

def previousyear(request):
	if "years" in request.session:
		request.session["years"] =int(request.session["years"])-1
	return showcalendar(request)

def nextyear(request):
	if "years" in request.session:           
		request.session["years"] =int(request.session["years"])+1
	return showcalendar(request)        

def previousmonth(request):
	if "months" in request.session:           
		if (int(request.session["months"]) != 1):
			request.session["months"] =int(request.session["months"])-1
		else:
			request.session["months"] = 12;
			request.session["years"] = int(request.session["years"])-1
	return showcalendar(request)

def nextmonth(request):
	if "months" in request.session:            
		if (int(request.session["months"]) != 12):
			request.session["months"] =int(request.session["months"])+1
		else:
			request.session["months"] = 1;
			request.session["years"] = int(request.session["years"])+1
	return showcalendar(request)
		
def __getDays__(request, days):
	if "todaydays" in request.session:
		year =  int(request.session["todayyears"])
		month = int(request.session["todaymonths"])
		day = int(request.session["todaydays"])
		dt = date(year,month,day)
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
		dt = date(year,month,day)
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