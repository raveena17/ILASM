import os

from django import template
from django.template import Library, Node, VariableDoesNotExist
#from projectManagement.settings import *
from projectManagement.taskGroupII.models import *
from projectManagement.nonProjectTask.models import *
from projectManagement.Utility import GetDateType
from django.conf import settings
register = Library()


def tagvalid(dicttimes,timeval):
	if dicttimes.__contains__(timeval):
		return dicttimes[timeval]
	return ""

def tags(strlinks): 
	return strlinks
	
def tagstatus(taskid):
	taskstatus = "Incomplete"	
	tasks = TaskAllocation.objects.filter(programTask = taskid)
	if(len(tasks)>0):
		tasks = tasks.filter(status = 'Incomplete')
		if(len(tasks)>0):
			taskstatus = "Incomplete"	
		else:
			taskstatus = "Completed"
	else:
			taskstatus = "Incomplete"  	
	### Added to handle approval image for approval task
	programTask = ProgramTask.objects.filter(pk = taskid)
	if len(programTask) > 0:
		programTask = programTask[0]
		if programTask.isapproved:
			color = getTaskApprovalColor(programTask)
			taskstatus += '&nbsp;&nbsp;<td class="'+ color +'_task_approval" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>'			
	return taskstatus

def getTaskApprovalColor(task):
	taskApprover = TaskApprover.objects.filter(programTask = task)
	color = 'Default'
	app_status = []
	for approver in taskApprover:			
		taskCmd = TaskApproverCommand.objects.get(taskApprover = approver)			
		if (taskCmd.approvedDate == None) or (taskCmd.approvedDate == GetDateType('2000-01-01')):
			app_msg = 'inprogress'
		elif taskCmd.isapproved:
			app_msg = 'completed'
		else:
			app_msg = 'rejected'			
		app_status.append(app_msg)	
	if app_status.__contains__('inprogress'):
		color = 'blue'
	else:
		completed = 0
		rejected = 0
		for each in app_status:
			if each == 'completed':
				completed += 1
			elif each == 'rejected':
				rejected += 1	
		if settings.APPROVAL_ROLE == 'MIN' and len(app_status) > 0:		
			color = 'green' if  completed > 0 else 'red'		
		elif len(app_status) > 0 :		
			color = 'green' if 	completed >= rejected and completed > 0 else 'red'
	return color

def tagnonprojecttaskstatus(taskid):
	tasks = NonProjectTaskAssignees.objects.filter(nonProjectTaskID = taskid)
	if(len(tasks)>0):
		tasks = tasks.filter(status = 'Incomplete')
		if(len(tasks)>0):
			return "Incomplete"	
		else:
			return "Completed"
	else:
			return "Incomplete"  	
	return "Incomplete"

def tagtaskliststatus(tasklistid):
	status = False
	listdetails = ProgramTasklistDetail.objects.filter(programTasklist=tasklistid)

	if (len(listdetails)>0):
		for each in listdetails:
			programtask = ProgramTask.objects.filter(	pk = each.programTask_id, cancel = 1)		   
			if len(programtask) <= 0: 
					tasks = TaskAllocation.objects.filter(programTask = each.programTask)				
					if(len(tasks)>0):
						tasks = tasks.filter(status = 'Incomplete')
						if(len(tasks)>0):
							status = False
							return 'Incomplete'
						else:
							status = True
					else:
						status = False
						return 'Incomplete'
	if status:
		return 'Completed'
	else:
		return 'Incomplete'		

def seltaskname(seltasks):	
	if (seltasks.__dict__.keys().__contains__('name')):
			return seltasks.name 
	else:
			return seltasks.programTask.name
			
def seltaskid(seltasks):	
	if (seltasks.__dict__.keys().__contains__('name')):
			return seltasks.taskID	 
	else:
			return seltasks.programTask.taskID	

def validdate(data):
	if (str(data).__contains__('2000-01-01')):
		return " class=vDateField "
	return " oncontextmenu='return false;' onkeydown = 'javascript:return false;' onkeyup = 'javascript:return false;' onkeypress = 'javascript:return false;' "
	
def validdateactual(data):
	if (str(data).__contains__('2000-01-01')):
		return " oncontextmenu='return false;' onkeydown = 'javascript:return false;' "
	return " oncontextmenu='return false;' onkeydown = 'javascript:return false;' onkeyup = 'javascript:return false;' onkeypress = 'javascript:return false;' "	

def artifactreadonly(data):
	if (str(data).strip() != ''):
		return 'readonly'
	return ''

def fileexists(downloadpath,fname):
	import os
	filenotexits = 'File not exists'
	path = settings.MEDIA_ROOT    
	if (fname != ''):
		path = path+'/'+str(fname)
		downloadpath = downloadpath+str(fname)	    
		if (os.path.isfile(path)):		
			return "href='"+downloadpath+"'"
	return " href=# onclick=javascript:alert('File-doesnot-exists');"

def truncchar(value, arg):
	if len(value) < arg:
		return value
	else:
		return value[:arg] + '...'

				
register.simple_tag(tags)
register.simple_tag(tagvalid)
register.simple_tag(tagtaskliststatus)
register.simple_tag(tagnonprojecttaskstatus)
register.simple_tag(tagstatus)
register.simple_tag(seltaskname)
register.simple_tag(seltaskid)
register.simple_tag(validdate)
register.simple_tag(validdateactual)
register.simple_tag(artifactreadonly)
register.simple_tag(fileexists)
register.filter(truncchar)














