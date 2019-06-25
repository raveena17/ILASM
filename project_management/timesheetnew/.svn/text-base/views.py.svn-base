"""
    View functions.
"""

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
#from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound, \
    HttpResponseForbidden, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core import serializers
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.contrib import messages

from project_management.non_project_task.models import NonProjectTaskAssignees
from project_management.projects.models import Project
#from project_management.timesheetnew.forms import PartialTaskTrackingForm, \
#    TaskSelectionForm
from project_management.timesheetnew.models import TaskTrackingNew
from project_management.timesheetnew.models import ProjTimeExceedNew
from project_management.tasks.models import Task
#from project_management.users.models import FiveGUser

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import datetime as dt
import time
from datetime import datetime 
from dateutil.relativedelta import relativedelta
import sys,time,string,getopt

MAX_TASK_COUNT = 20
date_format = '%m/%d/%Y'
forbidden_msg = _('Date selected is too old. Timesheet entry cannot be made.')
pagenotfound_msg = _('Timesheet cannot be entered for a future date.')

@login_required
def task_tracking(request):
    """
        Task tracking entries display and CRUD.
    """
    task_name = []   
    date_text = request.GET.get('date', datetime.today().strftime(date_format))
    try:
        date = datetime.strptime(date_text.strip('/'), date_format)
    except ValueError:
        return HttpResponseNotFound(pagenotfound_msg)
#    if date > (datetime.today()).date():
#        return HttpResponseNotFound(pagenotfound_msg)
#    elif date < (datetime.today()).date() + relativedelta(months=-1):
#        return HttpResponseForbidden(forbidden_msg)
#        selected_tasks1 = Task.objects.filter(id__in = cache.get(request.user.pk, []))
    selected_tasks = TaskTrackingNew.objects.filter(user = request.user)
    project_set = Project.objects.filter(Q(apex_body_owner=request.user, is_active = True) |
                Q(owner=request.user, is_active = True) |
                Q(team=request.user, is_active = True) | Q(requested_by = request.user, is_active = True)).distinct().exclude(cancel = True)
    project_id = request.GET.get('project')
    nonprojecttask = Task.objects.filter(project=None)
    for each_pjt in project_set:
        task = Task.objects.filter(project= each_pjt.id).filter(assigned_resources = request.user)            
        sel_task = []   
        each_pjt.__dict__.update({'Task':task,'sel_task':sel_task})
        tasks = serializers.serialize('json', task, fields=('name','id'))
        json = simplejson.dumps(tasks)
    dtstart = datetime( 1900, 01, 01,0, 0, 0, 0 )
    dtend = datetime( 1900, 01, 01, 23, 0, 0, 0 )
    times = []
    times.append(dtstart.strftime("%H.%M"))
    while dtstart <= dtend:
        dtstart = dtstart + timedelta(minutes=30)
        times.append(dtstart.strftime("%H.%M"))
    if request.method == 'POST':        
        dif = TaskTrackingNew.objects.filter(date = date,user=request.user)
        dif.delete()
        for element in range(1, 5):
            for each in project_set:                
                task = request.POST.get(str(each.id)+'_task'+str(element))
                if task == '' or task == None :
                    continue
                Timefrom = request.POST.get(str(each.id)+'_Timefrom' + str(element))
                if Timefrom == '' or Timefrom == None :
                    continue
                Timeto = request.POST.get(str(each.id)+'_Timeto' + str(element)) 
                if Timeto == '' or Timeto == None :
                    continue
                start_dt = dt.datetime.strptime(Timefrom, '%H.%M')
                end_dt = dt.datetime.strptime(Timeto, '%H.%M')
                diff = (end_dt - start_dt)
                diff.seconds/60 
                date_text = request.POST.get('date','')
                date = datetime.strftime(datetime.strptime(str(date_text.strip('/')),'%m/%d/%Y'),'%Y-%m-%d')
                project_dict = ({'user_id':request.user.id,
                'project_id' :each.id,
                'task_id':task,
                'time_from':Timefrom,
                'time_to':Timeto,
                'time_spent':diff,
                'date':date,
                })
                time_save = TaskTrackingNew(**project_dict)
                time_save.save()                
            task = request.POST.get('0_task' + str(element))
            if task == '' or task == None :
                continue
            Timefrom = request.POST.get('0_Timefrom' + str(element))
            if Timefrom == '' or Timefrom == None :
                continue
            Timeto = request.POST.get('0_Timeto' + str(element))
            if Timeto == '' or Timeto == None :
                continue
            start_dt = dt.datetime.strptime(Timefrom, '%H.%M')
            end_dt = dt.datetime.strptime(Timeto, '%H.%M')
            diff = (end_dt - start_dt)
            diff.seconds/60 
            date_text = request.POST.get('date','')
            date = datetime.strftime(datetime.strptime(str(date_text.strip('/')),'%m/%d/%Y'),'%Y-%m-%d')             
            nonproject_dict = ({'user_id':request.user.id,
                'project_id' :'0',
                'task_id':task,
                'time_from':Timefrom,
                'time_to':Timeto,
                'time_spent':diff,
                'date':date,
                })           
            timesheet_save = TaskTrackingNew(**nonproject_dict)
            timesheet_save.save()
        return HttpResponseRedirect('/timesheetnew/edit/?date='+date_text)
    return render_to_response('timesheet2.html', {'projects' : project_set,'each_pjt' : each_pjt,'sel_non_pjt_tsk': [],'Task' : nonprojecttask,'times':times,'date_text': date_text }, context_instance = RequestContext(request))
    

@login_required
def edit(request,date=None):    
    date_text = request.GET.get('date', datetime.today().strftime(date_format))        
    date = datetime.strftime(datetime.strptime(str(date_text.strip('/')),'%m/%d/%Y'),'%Y-%m-%d')         
    tasks = TaskTrackingNew.objects.filter(date = date,user
                    = request.user)    
    tot_timespent = relativedelta()
    for time_diff in tasks:
        diff = str(time_diff.time_spent).split(":")
        tot_timespent += relativedelta(hours=int(diff[0]),minutes=int(diff[1]))
    diff = str(tot_timespent.hours)+"."+str(tot_timespent.minutes)
    project_id = request.GET.get('project')
    selected_tasks = TaskTrackingNew.objects.filter(date = date,user
                    = request.user)
    project_set = Project.objects.filter(Q(apex_body_owner=request.user, is_active = True) |
    Q(owner=request.user, is_active = True) |
    Q(team=request.user, is_active = True) | Q(requested_by = request.user, is_active = True)).distinct().exclude(cancel = True) 
    sel_task_list = selected_tasks.filter(project=0).order_by('time_from')
    sel_non_pjt_tsk = []        
    for each_task in sel_task_list:
        sel_non_pjt_tsk.append({'nonprojecttask':each_task.task.id,'nonprojecttask_timefrom':each_task.time_from,'nonprojecttask_timeto':each_task.time_to})
    nonprojecttask = Task.objects.filter(project=None)    
    for each_pjt in project_set:
        sel_task_list = selected_tasks.filter(project=each_pjt.id).order_by('time_from')
        sel_task = []        
        for each_task in sel_task_list:
            sel_task.append({'task':each_task.task.id,'timefrom':each_task.time_from,'timeto':each_task.time_to})
        task = Task.objects.filter(project= each_pjt.id).filter(assigned_resources = request.user)
        each_pjt.__dict__.update({'Task':task})
        each_pjt.__dict__.update({'sel_task':sel_task})
        tasks = serializers.serialize('json', task, fields=('name','id'))
        json = simplejson.dumps(tasks)
        dtstart = datetime( 1900, 01, 01,0, 0, 0, 0 )
        dtend = datetime( 1900, 01, 01, 23, 0, 0, 0 )
        times = []
        times.append(dtstart.strftime("%H.%M"))
        while dtstart <= dtend:
            dtstart = dtstart + timedelta(minutes=30)
            times.append(dtstart.strftime("%H.%M"))    
    return render_to_response('timesheet2.html', {'projects' : project_set,
        'selected_tasks': selected_tasks,'sel_non_pjt_tsk':sel_non_pjt_tsk,
        'Task' : nonprojecttask,'times':times,'date_text': date_text,'time_spent': diff}, 
    context_instance = RequestContext(request))

    
#@login_required
#def task_lookup(request):
#    """
#        Lookup task for the logged in user,
#        by comparing task name queries against task allocation tables.
#        TODO: Bad logic. Inconsitencies related to different type of tasks has to be addressed.
#    """
#    result = []
#    query = ''
#    user = request.user
#    if request.method == 'GET':
#        query = request.GET.get(u'q', '').lower()
#    if len(query) > 2:
#        allocated_tasks = [ allocated for allocated in\
#            request.user.task_set.filter(name__icontains = query).filter(
#            project__is_active = True).exclude(status = 'closed') ]
#        allocated_tasks.extend(
#             [ non_project_task for non_project_task in Task.objects.filter(
#                name__icontains = query).filter(project = None).filter(
#                milestone = None)])
#        query_matching_tasks = [ task for task in allocated_tasks\
#                                 if query in task.name.lower() ]
#        result = [ { 'id' : str(task.id), 'name' : task.name,
#            'project': (task.project.name if task.project\
#            else 'Non Project Task'), } for task in query_matching_tasks ]
#    try:
#        return HttpResponse(simplejson.dumps(result), mimetype = 'application/json')
#    except Exception as e:
#        pass
#
#
#@login_required
#def Total_Time_Spent(request,date_text):
#    """
#       calulate the total time spent in the timesheet
#  """
#    date_text = request.GET.get('date', datetime.today().strftime(date_format))    
#   date = datetime.strptime(date_text.strip('/'), date_format)    
#
#next_day = date + timedelta(hours = 23.99)
#    time_spent = TaskTrackingNew.objects.filter(time_from__range
#                    = (date, next_day)).filter(user
#                   = request.user).aggregate(total = Sum('time_spent'))
#    time_spent['total'] = str(time_spent['total'])
#    return HttpResponse(simplejson.dumps(time_spent), mimetype = 'application/json')

#def get_Times():
#    dtstart = datetime( 1900, 01, 01,0, 0, 0, 0 )
#    dtend = datetime( 1900, 01, 01, 23, 0, 0, 0 )
#    times = []
#    times.append(dtstart.strftime("%I:%M %p"))
#    while dtstart <= dtend:
#        dtstart = dtstart + timedelta(minutes=30)
#        times.append(dtstart.strftime("%I:%M %p"))
#    return times
#    render_to_response('timesheet2.html',{'times':times})
#
#@login_required
#def daywise_task_lookup(request):
#    """
#        Day wise lookup of tasks.
#    """
#    if request.method != 'GET':
#        return None
#    date_text = request.GET.get(u'date', datetime.today().strftime(date_format))
#    try:
#    date = datetime.strptime(date_text.strip('/'), date_format)
#    except ValueError:
#        return HttpResponseNotFound(pagenotfound_msg)
#    next_day = date + timedelta(hours = 23.99)
#    days_tasks = TaskTrackingNew.objects.filter(start_time__range
#                    = (date, next_day)).filter(user = request.user)
#    tasks = simplejson.dumps( [ { 'id' : task.task,
#        'name' : TaskTrackingNew.get_task(task.task).name,
#        'projname' : TaskTrackingNew.get_projectname(task.task),
#        'time_spent' : float(task.time_spent), #TODO: Try removing float.
#        'start_time' : '%02d%02d'%(task.start_time.hour, task.start_time.minute)
#        'is_rework' : 'checked' if task.is_rework else None
#        } for task in days_tasks ] ) 
#    return HttpResponse(tasks, mimetype = 'application/json')
#
#def crud_task_entry_ajax(form, user):
#    """
#        Do CRUD operations for the task tracking entry.
#    """
#    """form = PartialTaskTrackingForm({
#        'task' : request.POST.get('task'),
#        'start_time' : datetime.strptime(request.POST.get('startTime'), '%Y-%m-%d %H%M'),
#        'time_spent' : request.POST.get('timeSpent', '0'),
#        })"""
#    error = "None"
#    if form.is_valid() and form.cleaned_data['task'] != u'undefined':
#        try:
#            form.save(user = user)
#            error = "None"
#        except:
#            error = "Exceeded"
#    elif form.data.get('task') == u'undefined':
#        delete_entry(user, form.data.get('start_time'))
#    else:
#        return form.errors       
#    return error
#
#def delete_entry(user, start_time):
#    """
#        Delete a TaskTracking entry, for the specified user and start time.
#    """
#    TaskTrackingNew.objects.filter(user = user, start_time = start_time).delete()
#
#def get_task(request):
#    """
#        Get Tasks from selected project
#    """
#    project_id = request.GET.get('project')
#    if project_id == '0':
#        task = Task.objects.filter(project = None)
#    else:
#        task = Task.objects.filter(project=project_id)
#    tasks = serializers.serialize('json', task, fields=('name','id'))
#    json = simplejson.dumps(tasks)
#    return HttpResponse(json, mimetype = 'application/javascript')
#
#def cache_tasks(user, selected_tasks):
#    cached_tasks = cache.get(user.pk, [])
#    tasks = selected_tasks + cached_tasks
#    if len(tasks) > MAX_TASK_COUNT:
#        tasks = tasks[:20]
#    if cache.has_key(user.pk):
#        cache.set(user.pk, tasks)
#    else:
#        cache.add(user.pk, tasks)
#    return tasks
#
#@login_required
#def add_task_to_task_pane(request):
#    result = []
#    project_id = request.POST.get('project', None)
#    if request.method == 'POST':
#        form = TaskSelectionForm(request.POST,
#           project = project_id, user = request.user)
#        if form.is_valid():
#            tasks = cache_tasks(request.user, form.cleaned_data['tasks'])
#            map(lambda task: result.append({'id': task.pk,
#                'name': unicode(task.project.name if task.project else \
#                'Non Project Task')+ ' : ' + unicode(task.name)}),
#                Task.objects.filter(id__in = tasks))
#            return HttpResponse(simplejson.dumps(result),
#                                mimetype='application/json')
#        return HttpResponse(status = 403)
#    else :
#        form = TaskSelectionForm(user = request.user)
#    return render_to_response('add_task_to_task_pane.html', {'form': form})
#
