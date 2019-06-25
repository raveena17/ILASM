"""
   Task Views
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
# from django.shortcuts import render_to_response
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
# from django.utils import simplejson
try:
    import django.utils.simplejson
except BaseException:
    import json as simplejson

from django.utils.translation import ugettext_lazy as _
#from django.views.generic import list_detail
from django.db.models import F, Q
from django.db import IntegrityError
from django.core.urlresolvers import reverse

from project_management.projects.models import Project
from project_management.tasks.models import *
from project_management.timesheet.models import *
from project_management.tasks.forms import TaskForm, TypeForm, SubTaskForm, \
    NonProjectTaskForm
from project_management.tasks.models import Task, Type, SubType
from django.views.generic import RedirectView
# from project_management.tasks.views import *

from django.views.generic import ListView


class SubListView(ListView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(SubListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        # import pdb;pdb.set_trace()
        return context


@login_required
def manage_task(request, tid=0):
    """
        function defines create and modify task that belongs to a project.
    """
    # import pdb;pdb.set_trace()
    project_code = request.GET.get('pid', '')
    next = request.GET.get('next', None)
    project = get_object_or_404(Project, id=project_code)
    task = None
    if tid:
        task = get_object_or_404(Task, pk=tid)
        # import pdb;pdb.set_trace()
    # unassigned_tasks = Task.tree.filter(lft = F('rght')-1,project = project)
    unassigned_tasks = Task.objects.filter(lft=F('rght') - 1, project=project)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, project=project)
        sub_task_form = SubTaskForm(request.POST, task=task)
        if form.is_valid() and sub_task_form.is_valid():
            try:
                task = form.save(user=request.user, project=project)
            except IntegrityError:
                messages.error(request, _('Task name already exists.'))
            else:
                sub_task_form.save(task=task)
                messages.success(request, _('Task saved successfully.'))
                if next:
                    return HttpResponseRedirect(
                        next + '?pid=' + str(project.id))
    else:
        form = TaskForm(instance=task, project=project)
        if not task:
            form.initial = {'owner': request.user.pk,
                            'assigned_resources': [request.user.pk]}
        sub_task_form = SubTaskForm(task=task)
    return render(request, 'task.html', {
        'form': form, 'unassigned_tasks': unassigned_tasks,
        'sub_task_form': sub_task_form, 'project': project},
    )


@login_required
def manage_type(request, id=None):
    """
        create and Edit task type
    """
    if request.method == 'POST':
        id = request.POST.get('id')
    try:
        type = Type.objects.get(pk=id)
        type.save()
    except BaseException:
        type = None
    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type)
        if form.is_valid():
            type = form.save()
            return HttpResponse(simplejson.dumps([{'id': type.pk,
                                                   'name': type.name}]), mimetype='application/json')
        else:
            return HttpResponse(simplejson.dumps([{'error': form.errors}]),
                                mimetype='application/json')
    else:
        form = TypeForm(instance=type)
        print form
    return render(request, 'task_type.html',
                  {'form': form, 'type': type})


@login_required
def delete_task_type(request, id=None):
    """
        delete task type
    """
    if not Task.objects.filter(type=id).count() > 0:
        Type.objects.get(pk=id).delete()
        return HttpResponse(status=200)  # success
    return HttpResponse(status=403)  # forbidden


@login_required
def task_list(request, page=1):
    """
        list the project task.
    """
    project_code = request.GET.get('pid', '')
    show_all_task = request.GET.get('all_task', '0')
    global it_admin_user
    try:
        project = Project.objects.get(id=project_code)
    except BaseException:
        # TODO: very bad logic. remove project id from session.
        project = Project.objects.get(id=request.session['projectid'])
    query = Q()
    search_text = request.GET.get('search', '')
    if search_text:
        q = Q()
        for term in search_text.split():
            q = Q(name__icontains=term)
        query = query & q
    if not show_all_task == '1':
        query = query & Q(assigned_resources=request.user)
    task_set = Task.objects.filter(query, project=project)
    #task_set = Task.objects.filter(query)
    callable = SubListView.as_view(
        queryset=task_set,
        template_name="task_list.html",
        context_object_name="task_list",
        paginate_by=20,
        extra_context={'project': project, 'show_all_task': int(show_all_task)}
        # extra_context = ({'project': project, 'it_admin_user':it_admin_user,
        #     'show_all_task': int(show_all_task)})
    )
    return callable(request)


# @login_required
# def task_list(request, page = 1):
#     """
#         list the project task.
#     """
#     project_code = request.GET.get('pid', '')
#     show_all_task = request.GET.get('all_task', '0')

#     try:
#         project = Project.objects.get(id = project_code)
#     except:
#         #TODO: very bad logic. remove project id from session.
#         project = Project.objects.get(id = request.session['projectid'])
#     query = Q()
#     search_text = request.GET.get('search', '')
#     if search_text:
#         q = Q()
#         for term in search_text.split():
#             q = Q(name__icontains = term)
#         query = query & q
#     if not show_all_task == '1':
#         query = query & Q(assigned_resources = request.user)
#     task_set = Task.objects.filter(query, project = project)
#     #task_set = Task.objects.filter(query)
#     callable = SubListView.as_view(
#         queryset = task_set,
#         template_name = "task_list.html",
#         context_object_name = "task_list",
#         extra_context = { 'project': project, 'it_admin_user':it_admin_user,
#             'show_all_task': int(show_all_task) }
#         )
#     return callable(request)

@login_required
# @csrf_token
def non_project_task_list(request):
    query = Q()
    search_text = request.GET.get('search', '')
    if search_text:
        q = Q()
        for term in search_text.split():
            q = Q(name__icontains=term)
        query = query & q
    task_set = Task.objects.filter(query).filter(
        project=None).filter(
        status=None).filter(
            priority=None)
    callable = SubListView.as_view(
        queryset=task_set,
        template_name="non_project_task_list.html",
        context_object_name="task_list",
        paginate_by=20
    )
    return callable(request)


#@login_required
# def task_list(request, page = 1):
#     """
#         list the project task.
#     """
#     project_code = request.GET.get('pid', '')
#     show_all_task = request.GET.get('all_task', '0')
#     it_admin_user = User.objects.filter(id = request.user.id,
#                  groups__name__icontains = 'IT Admin', is_active = True)

#     try:
#         project = Project.objects.get(id = project_code)
#     except:
#         #TODO: very bad logic. remove project id from session.
#         project = Project.objects.get(id = request.session['projectid'])
#     query = Q()
#     search_text = request.GET.get('search', '')
#     if search_text:
#         q = Q()
#         for term in search_text.split():
#             q = Q(name__icontains = term)
#         query = query & q
#     if not show_all_task == '1':
#         query = query & (Q(assigned_resources = request.user) )
#     task_set = Task.objects.filter(query, project = project)
#     #task_set = Task.objects.filter(query)
#     return list_detail.object_list(
#         request,
#         queryset = task_set,
#         template_name = "task_list.html",
#         template_object_name = "task",
#         extra_context = { 'project': project,'it_admin_user':it_admin_user,
#             'show_all_task': int(show_all_task) }
#         )


# @login_required
# def non_project_task_list(request):
#     query = Q()
#     search_text = request.GET.get('search', '')
#     if search_text:
#         q = Q()
#         for term in search_text.split():
#             q = Q(name__icontains = term)
#         query = query & q
#     task_set = Task.objects.filter(query).filter(project = None).filter(status
#                                                 = None).filter(priority = None)
#     return list_detail.object_list(
#         request,
#         queryset = task_set,
#         template_name = "non_project_task_list.html",
#         template_object_name = "task",
#         )


@login_required
def manage_non_project_task(request, id=None):
    """
        Add/Edit non project task.
    """
    non_project_task = None
    if id:
        non_project_task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        form = NonProjectTaskForm(request.POST, instance=non_project_task)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(
                request, _('Non Project Task saved successfully.'))
            return HttpResponseRedirect(reverse(non_project_task_list))
    else:
        form = NonProjectTaskForm(instance=non_project_task)
    return render(request, 'non_project_task.html', {'form': form},
                  )


@login_required
def delete_task(request, is_project_task=False):
    """
        Delete project/non-project-task task.
    """
    task_id = request.POST.getlist('task_pk')
    print task_id
    for i in task_id:
        val_check = TaskTracking.objects.filter(task=i)
        if len(val_check) == 0:
            Task.objects.filter(pk__in=task_id).delete()
            messages.success(request, _('Task(s) deleted successfully.'))
        else:
            messages.error(
                request,
                _('Task used in Timesheet, Unable to delete this Task'))
    if is_project_task:
        RedirectView = reverse(task_list) + '?pid=' \
            + request.GET.get('pid', '')
    else:
        RedirectView = reverse(non_project_task_list)
    return HttpResponseRedirect(RedirectView)


def get_sub_type(request):
    """
        Return sub type.
    """
    result = []
    type_id = request.POST.get('type', None)
    for sub_type in SubType.objects.filter(type=type_id):
        result.append({'id': sub_type.id, 'name': sub_type.name})
    return HttpResponse(simplejson.dumps(result),
                        content_type='application/json')
