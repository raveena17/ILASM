"""
    View functions.
"""

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
#from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseNotFound, \
    HttpResponseForbidden, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.contrib import messages

from project_management.non_project_task.models import NonProjectTaskAssignees
from project_management.projects.models import Project
from project_management.timesheet.forms import PartialTaskTrackingForm, \
    TaskSelectionForm
from project_management.timesheet.models import TaskTracking
from project_management.timesheet.models import ProjTimeExceed
from project_management.tasks.models import Task
#from project_management.users.models import FiveGUser

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
    if request.method == 'POST':
        user = request.user
        form = PartialTaskTrackingForm(request.POST)
        date_text = request.POST.get(u'date', datetime.today().strftime(date_format))
        if request.is_ajax():
            errors = crud_task_entry_ajax(form, user)
            return HttpResponse(simplejson.dumps(errors), mimetype = 'application/json')
        elif form.is_valid():
            form.save(user = user)
    else:
        form = PartialTaskTrackingForm()
        date_text = request.GET.get(u'date', datetime.today().strftime(date_format))
        try:
            date = datetime.strptime(date_text, date_format).date()
        except ValueError:
            return HttpResponseNotFound(pagenotfound_msg)
        if date > (datetime.today()).date():
            return HttpResponseNotFound(pagenotfound_msg)
        elif date < (datetime.today()).date() + relativedelta(months=-1):
            return HttpResponseForbidden(forbidden_msg)
#        selected_tasks1 = Task.objects.filter(id__in = cache.get(request.user.pk, []))
        selected_tasks = TaskTracking.objects.filter(user = request.user).order_by('-start_time')[:15]
        task_name = Task.objects.filter(id__in = [selTask.task for selTask in selected_tasks], project__is_active=1 )
    return render_to_response('timesheet.html', {
                'task_tracking_form' : form,
                'date_text': date_text,
                'task_name': task_name,
            }, context_instance = RequestContext(request))

@login_required
def task_lookup(request):
    """
        Lookup task for the logged in user,
        by comparing task name queries against task allocation tables.
        TODO: Bad logic. Inconsitencies related to different type of tasks has to be addressed.
    """
    result = []
    query = ''
    user = request.user
    if request.method == 'GET':
        query = request.GET.get(u'q', '').lower()
    if len(query) > 2:
        allocated_tasks = [ allocated for allocated in\
            request.user.task_set.filter(name__icontains = query).filter(
            project__is_active = True).exclude(status = 'closed') ]
        allocated_tasks.extend(
             [ non_project_task for non_project_task in Task.objects.filter(
                name__icontains = query).filter(project = None).filter(
                milestone = None)])
        query_matching_tasks = [ task for task in allocated_tasks\
                                 if query in task.name.lower() ]
        result = [ { 'id' : str(task.id), 'name' : task.name,
            'project': (task.project.name if task.project\
            else 'Non Project Task'), } for task in query_matching_tasks ]
    try:
        return HttpResponse(simplejson.dumps(result), mimetype = 'application/json')
    except Exception as e:
        pass


@login_required
def total_time_spent(request):
    """
        calulate the total time spent in the timesheet
    """
    date_text = request.GET.get('date', datetime.today().strftime(date_format))
#    try:
    date = datetime.strptime(date_text.strip('/'), date_format)
#    except ValueError:
#        return HttpResponseNotFound(pagenotfound_msg)
    next_day = date + timedelta(hours = 23.99)
    time_spent = TaskTracking.objects.filter(start_time__range
                    = (date, next_day)).filter(user
                    = request.user).aggregate(total = Sum('time_spent'))
    time_spent['total'] = str(time_spent['total'])
    return HttpResponse(simplejson.dumps(time_spent), mimetype = 'application/json')

@login_required
def daywise_task_lookup(request):
    """
        Day wise lookup of tasks.
    """
    if request.method != 'GET':
        return None
    date_text = request.GET.get(u'date', datetime.today().strftime(date_format))
#    try:
    date = datetime.strptime(date_text.strip('/'), date_format)
#    except ValueError:
#        return HttpResponseNotFound(pagenotfound_msg)
    next_day = date + timedelta(hours = 23.99)
    days_tasks = TaskTracking.objects.filter(start_time__range
                    = (date, next_day)).filter(user = request.user)
    tasks = simplejson.dumps( [ { 'id' : task.task,
        'name' : TaskTracking.get_task(task.task).name,
        'projname' : TaskTracking.get_projectname(task.task),
        'time_spent' : float(task.time_spent), #TODO: Try removing float.
        'start_time' : '%02d%02d'%(task.start_time.hour, task.start_time.minute)
#        'is_rework' : 'checked' if task.is_rework else None
        } for task in days_tasks ] ) 
    return HttpResponse(tasks, mimetype = 'application/json')

def crud_task_entry_ajax(form, user):
    """
        Do CRUD operations for the task tracking entry.
    """
    """form = PartialTaskTrackingForm({
        'task' : request.POST.get('task'),
        'start_time' : datetime.strptime(request.POST.get('startTime'), '%Y-%m-%d %H%M'),
        'time_spent' : request.POST.get('timeSpent', '0'),
        })"""
    error = "None"
    if form.is_valid() and form.cleaned_data['task'] != u'undefined':
        try:
            form.save(user = user)
            error = "None"
        except:
            error = "Exceeded"
    elif form.data.get('task') == u'undefined':
        delete_entry(user, form.data.get('start_time'))
#    else:
#        return form.errors
    return error

def delete_entry(user, start_time):
    """
        Delete a TaskTracking entry, for the specified user and start time.
    """
    TaskTracking.objects.filter(user = user, start_time = start_time).delete()

def get_tasks_for_project(request):
    """
        Get Tasks from a project
    """
    tasks = []
    result = []
    project_id = request.POST.get('project', None)
    if request.method == 'POST':
        if not project_id == '0':
            tasks = Task.objects.filter(project
                = project_id).filter(assigned_resources = request.user)
        else:
            tasks = Task.objects.filter(project = None)
        for task in tasks:
             result.append({'name': task.name, 'id': task.id})
        return HttpResponse(simplejson.dumps(result), mimetype='application/json')
    return HttpResponse(status = 403)

def cache_tasks(user, selected_tasks):
    cached_tasks = cache.get(user.pk, [])
    tasks = selected_tasks + cached_tasks
    if len(tasks) > MAX_TASK_COUNT:
        tasks = tasks[:20]
    if cache.has_key(user.pk):
        cache.set(user.pk, tasks)
    else:
        cache.add(user.pk, tasks)
    return tasks

@login_required
def add_task_to_task_pane(request):
    result = []
    project_id = request.POST.get('project', None)
    if request.method == 'POST':
        form = TaskSelectionForm(request.POST,
           project = project_id, user = request.user)
        if form.is_valid():
            tasks = cache_tasks(request.user, form.cleaned_data['tasks'])
            map(lambda task: result.append({'id': task.pk,
                'name': unicode(task.project.name if task.project else \
                'Non Project Task')+ ' : ' + unicode(task.name)}),
                Task.objects.filter(id__in = tasks))
            return HttpResponse(simplejson.dumps(result),
                                mimetype='application/json')
        return HttpResponse(status = 403)
    else :
        form = TaskSelectionForm(user = request.user)
    return render_to_response('add_task_to_task_pane.html', {'form': form})

