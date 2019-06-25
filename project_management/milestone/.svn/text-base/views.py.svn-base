"""
    Milestone views
"""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import list_detail
from django.db.models import Q

#from project_management.users.models import FiveGUser
from project_management.milestone.models import Milestone
from project_management.projects.models import Project
from project_management.milestone.forms import EngineeringMilestoneForm


def milestone_list(request, pageNo = 1):
    project_code = request.GET.get('pid', '')
    try:
        project = Project.objects.get(id = project_code)
    except:
        #TODO: very bad logic. remove project id from session.
        project = Project.objects.get(id = request.session['projectid'])
    query = Q()
    search_text = request.GET.get('search', '')
    if search_text:
        q = Q()
        for term in search_text.split():
            q = Q(name__icontains = term)
        query = query & q
    milestone_set = Milestone.objects.filter(query, project = project,
        category = Milestone.ENGINEERING)
    return list_detail.object_list(
        request,
        queryset = milestone_set,
        template_name = "milestone_list.html",
        template_object_name = "milestone",
        extra_context = {'project': project }
        )

@login_required
def milestone_delete(request):
    """
        delete milestones
    """
    milestone_ids = request.POST.getlist('milestone_pk')
    Milestone.objects.filter(pk__in = milestone_ids).delete()
    return HttpResponseRedirect(reverse(milestone_list))

@login_required
def manage_milestone(request, id = None):
    """
        create and modify milestones
    """
    milestone = None
    project_id = request.GET.get('pid', None)
    project = get_object_or_404(Project, code = project_id)
    if id:
        milestone = get_object_or_404(Milestone, pk = id)
    if request.method == 'POST':
        milestone_form = EngineeringMilestoneForm(request.POST,
                                instance = milestone)
        if milestone_form.is_valid():
            milestone_form.save(project = project, id = id)
            return HttpResponseRedirect(reverse(milestone_list))
    else:
        milestone_form = EngineeringMilestoneForm(instance = milestone)
    return render_to_response('milestone.html', {'form': milestone_form,
        'project': project}, context_instance = RequestContext(request))
