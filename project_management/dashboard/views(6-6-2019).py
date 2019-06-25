from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from project_management.address.forms import AddressForm
from django.views.generic import RedirectView
from django.views.generic import ListView
from project_management.leave.models import *
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import settings
from mysql.connector import MySQLConnection, Error
from decimal import Decimal
from project_management.dashboard.forms import *

# from python_mysql_dbconfig import read_db_config


host = settings.DATABASES['default']['HOST']
database = settings.DATABASES['default']['NAME']
user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']

def fetch_dashboard_sp(employee):
	try:
	    conn = MySQLConnection(
								host=host,
	                            database=database,
	                            user=user,
	                            password=password)
	    cursor = conn.cursor()
	    args = (employee)
	    cursor.callproc('DashboardValues', [args])
	    for result in cursor.stored_results():
		column_names_list = [x[0] for x in result.description]
		result_dicts = [dict(zip(column_names_list, row))
		for row in result.fetchall()]
		return result_dicts

	except Error as e:
	    print(e)

	finally:
	    cursor.close()
	    conn.close()

def fetch_ThisWeekProjectSummary_sp(employee):
	try:
	    conn = MySQLConnection(
								host=host,
	                            database=database,
	                            user=user,
	                            password=password)
	    cursor = conn.cursor()

	    args = (employee)
	    cursor.callproc('ThisWeekProjectSummary', [args])
	    for result in cursor.stored_results():
		column_names_list = [x[0] for x in result.description]
		result_dicts = [dict(zip(column_names_list, row))
		for row in result.fetchall()]
		return result_dicts

	except Error as e:
	    print(e)

	finally:
	    cursor.close()
	    conn.close()
 
def fetch_ThisMonthProjectSummary_sp(employee):
	try:
	    conn = MySQLConnection(
								host=host,
	                            database=database,
	                            user=user,
	                            password=password)
	    cursor = conn.cursor()

	    args = (employee)
	    cursor.callproc('ThisMonthProjectSummary', [args])
	    for result in cursor.stored_results():
		column_names_list = [x[0] for x in result.description]
		result_dicts = [dict(zip(column_names_list, row))
		for row in result.fetchall()]
		return result_dicts

	except Error as e:
	    print(e)

	finally:
	    cursor.close()
	    conn.close()

def fetch_ThisYearProjectSummary_sp(employee):
	try:
	    conn = MySQLConnection(
								host=host,
	                            database=database,
	                            user=user,
	                            password=password)
	    cursor = conn.cursor()

	    args = (employee)
	    cursor.callproc('ThisYearProjectSummary', [args])
	    for result in cursor.stored_results():
		column_names_list = [x[0] for x in result.description]
		result_dicts = [dict(zip(column_names_list, row))
		for row in result.fetchall()]
		return result_dicts

	except Error as e:
	    print(e)

	finally:
	    cursor.close()
	    conn.close()


def getUserGoals(employee):
	try:
	    conn = MySQLConnection(
								host=host,
	                            database=database,
	                            user=user,
	                            password=password)
	    cursor = conn.cursor()
	    args = (employee)
	    cursor.callproc('getUserGoals', [args])
	    for result in cursor.stored_results():
		column_names_list = [x[0] for x in result.description]
		result_dicts = [dict(zip(column_names_list, row))
		for row in result.fetchall()]
		return result_dicts

	except Error as e:
	    print(e)

	finally:
	    cursor.close()
	    conn.close()





@login_required
def manage_dashboard(request, id=None):


	# import pdb;pdb.set_trace()

	if id==request.user.id:
		userid = request.user.id
	elif id==None:
		userid = request.user.id
	else:
		userid = id
        username =User.objects.get(id=userid, is_active=True).username


	today = datetime.date.today()
	list_data =[]

	emp = request.user.username
	# employee = request.user
	# get_user_goals = getUserGoals(employee.id)
	# fetch_leave_data = fetch_dashboard_sp(employee.id)
	# weekly_project_task = fetch_ThisWeekProjectSummary_sp(employee.id)
	# mothly_project_task = fetch_ThisMonthProjectSummary_sp(employee.id)
	# yearly_project_task = fetch_ThisYearProjectSummary_sp(employee.id)

	late_attendance = LateAttendance.objects.filter(month_of_year = today.month, emp_name=userid)
	get_user_goals = getUserGoals(userid)
	fetch_leave_data = fetch_dashboard_sp(userid)
	weekly_project_task = fetch_ThisWeekProjectSummary_sp(userid)
	mothly_project_task = fetch_ThisMonthProjectSummary_sp(userid)
	yearly_project_task = fetch_ThisYearProjectSummary_sp(userid)
	
	user_goals = []

	if get_user_goals:
		for goal in get_user_goals:
			goal_items ={
				'goal':goal['goal'],
				'setDate':goal['setDate'].strftime("%d-%m-%Y"),
				'targetDate':goal['targetDate'].strftime("%d-%m-%Y"),
			}
			user_goals.append(goal_items)

	

	adict = {
                'login_username':userid,
		'username' : fetch_leave_data[0]['username'],
		'thisMonthLeave': '%g' % fetch_leave_data[0]['thisMonthLeave'],
		'thisYearLeave': '%g' % fetch_leave_data[0]['thisYearLeave'],
		'lateAttendanceCount': '%g' % fetch_leave_data[0]['lateAttendanceCount'] if fetch_leave_data[0]['lateAttendanceCount'] != None else 0,
		# 'lateAttendance': '%g' % len(late_attendance),
	}


	week_projects = []
	week_projects_efforts = []
	monthly_projects = []
	monthly_projects_efforts = []
	yearly_projects = []
	yearly_projects_efforts = []

	data_list = {}

	
	for weektask in weekly_project_task:
		week_projects.append(weektask['Project'])
		week_projects_efforts.append(weektask['TimeSpent'])

	week_projects_efforts = list(map(float, week_projects_efforts))
	week_projects = map(str, week_projects)
	week_projects = ", ".join(week_projects)




	for monthly_task in mothly_project_task:
		monthly_projects.append(monthly_task['Project'])
		monthly_projects_efforts.append(monthly_task['TimeSpent'])

	monthly_projects_efforts = list(map(float, monthly_projects_efforts))
	monthly_projects = map(str, monthly_projects)
	monthly_projects = ", ".join(monthly_projects)




	for yearly_task in yearly_project_task:
		yearly_projects.append(yearly_task['Project'])
		yearly_projects_efforts.append(yearly_task['TimeSpent'])

	yearly_projects_efforts = list(map(float, yearly_projects_efforts))
	yearly_projects = map(str, yearly_projects)
	yearly_projects = ", ".join(yearly_projects)


	data_list = {

		'week_projects' : week_projects,
		'week_projects_efforts' : week_projects_efforts,
		'monthly_projects' : monthly_projects,
		'monthly_projects_efforts' : monthly_projects_efforts, 
		'yearly_projects' : yearly_projects, 
		'yearly_projects_efforts' : yearly_projects_efforts,

		}
	report_form = ReportForm()
	# return render(request, 'dashboard3.html', {'adict':adict, 'data_list':data_list, 'user_goals':user_goals, 'report_form': report_form})
	# return render(request, 'dashboard4.html', {'adict':adict, 'data_list':data_list, 'user_goals':user_goals, 'report_form': report_form})
	return render(request, 'ms_dashboard.html', {'username':username,'adict':adict, 'data_list':data_list, 'user_goals':user_goals, 'report_form': report_form})


def manage_charts(request, id=None):
	# import pdb;pdb.set_trace()
	today = datetime.date.today()
	list_data =[]

	emp = request.user.username
	late_attendance = LateAttendance.objects.filter(month_of_year = today.month, emp_name=request.user)
	

	return render(request, 'charts.html', {'emp':emp, } )



