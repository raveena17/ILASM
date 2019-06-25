from django.conf import settings
from django.template import Library

import os

register = Library()

def tagvalid(dicttimes, timeval):
    if dicttimes.__contains__(timeval):
        return dicttimes[timeval]
    return ""

def tags(strlinks):
    return strlinks

#def tagstatus(taskid):
#	tasks = TaskAllocation.objects.filter(programTask = taskid)
#	if(len(tasks)>0):
#		tasks = tasks.filter(status = 'Incomplete')
#		if(len(tasks)>0):
#			return "Incomplete"
#		else:
#			return "Completed"
#	else:
#			return "Incomplete"
#	return "Incomplete"

#def tagnonprojecttaskstatus(taskid):
#    tasks = NonProjectTaskAssignees.objects.filter(non_project_taskID = taskid)
#    if(len(tasks)>0):
#        tasks = tasks.filter(status = 'Incomplete')
#        if(len(tasks)>0):
#            return "Incomplete"
#        else:
#            return "Completed"
#    else:
#            return "Incomplete"
#    return "Incomplete"

#def tagtaskliststatus(tasklistid):
#    status = False
#    listdetails = ProjectTaskListDetail.objects.filter(programTasklist=tasklistid)
#
#    if (len(listdetails)>0):
#        for each in listdetails:
#           programtask = ProjectTask.objects.filter(	pk = each.programTask_id, cancel = 1)
#           if len(programtask) <= 0:
#                tasks = TaskAllocation.objects.filter(programTask = each.programTask)
#                if(len(tasks)>0):
#                    tasks = tasks.filter(status = 'Incomplete')
#                    if(len(tasks)>0):
#                        status = False
#                        return 'Incomplete'
#                    else:
#                        status = True
#                else:
#                    status = False
#                    return 'Incomplete'
#    if status:
#        return 'Completed'
#    else:
#        return 'Incomplete'

#def seltaskname(seltasks):
#	if (seltasks.__dict__.keys().__contains__('name')):
#			return seltasks.name
#	else:
#			return seltasks.programTask.name

#def seltaskid(seltasks):
#	if (seltasks.__dict__.keys().__contains__('name')):
#			return seltasks.pk
#	else:
#			return seltasks.programTask.pk

def validdate(data):
    if (str(data).__contains__('2000-01-01')):
	    return " class=vDateField "
    return " oncontextmenu='return false;' onkeydown = 'javascript:return false;' onkeyup = 'javascript:return false;' onkeypress = 'javascript:return false;' "

def validdateactual(data):
    if (str(data).__contains__('2000-01-01')):
	    return " oncontextmenu='return false;' onkeydown = 'javascript:return false;' "
    return " oncontextmenu='return false;' onkeydown = 'javascript:return false;' onkeyup = 'javascript:return false;' onkeypress = 'javascript:return false;' "

#def artifactreadonly(data):
#   if (str(data).strip() != ''):
#		return 'readonly'
#	return ''

def fileexists(downloadpath, fname):
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
register.simple_tag(validdate)
register.simple_tag(validdateactual)
register.simple_tag(fileexists)
register.filter(truncchar)
