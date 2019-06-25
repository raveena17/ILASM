"""
    project views
"""
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.db.models import Q, F
from django.forms.models import modelformset_factory
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
# from django.shortcuts import render_to_response
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
# from django.utils import simplejson
try:
    import django.utils.simplejson
except:
    import json as simplejson

from django.utils.translation import ugettext as _
#from django.views.generic import list_detail


from project_management.logs.logger import CapturLog
from project_management.notifications.models import Event
from project_management.projects.forms import  ProjectInitiationForm, \
    VisiblePrimaryKeyFormset, ProjectGroupForm, ProjectInitiationRequestForm,\
    ProjectSchedulesRequestForm
from project_management.projects.models import DevelopmentEntity, ProjectRole, \
    ProjectSchedule, Project,  ProjectMembership, Domain, ProjectType
from project_management.milestone.models import Milestone, InvoiceTerms
from project_management.projects.plan.forms import PlanForm, InitiationForm, \
    make_responsibility_form, DevelopmentEnvironmentForm
from project_management.common_manager.master_forms import DomainForm, \
    ProjectTypeForm
from project_management.projects.forms import BusinessUnitForm
from project_management.tasks.models import Task
from project_management.users.models import UserProfile
from project_management.Utility import Email
from project_management.customer.models import Customer
from project_management.business_unit.models import BusinessUnit


import datetime
CONTENT_TYPE = 'html'

actionMsg = {
    '':'',
    'Duplicate': _('Project name already exists.'),
    'Create': _('Create'),
    'CreateError': _('Create unsuccessful'),
    'Update': _('Update'),
    'UpdateError': _('Update unsuccessful'),
    'Project_Saved':_('Project saved successfully'),
    'SAVE':_('Resource added successfully'),
    'SaveError':_('Project save unsuccessful'),
    'DeleteSuccess': _('Project deleted successfully'),
    'Deleteunsuccess': _('Project is dependent. Cannot be deleted.'),
    'Stagedeletesuccess': _('Stage deleted successfully'),
    'Stagedeleteunsuccess': _('Stage is dependent and cannot be deleted.'),
    'Access Denied': _('Access Denied'),
    'CostCenterSave' :_('Department saved successfully'),
    'CostCenterDuplicate':_('Department name already exists'),
    'Stage':_(''),
    'StageSave':_('Milestone saved successfully'),
    'StageSaveErr':_('Milestone save unsuccessful'),
    'DuplicateStage': _('Milestone name already exists.'),
    'ProgramInactive': _('Project cannot be saved for an inactive Program.'),
    'Inactive': _('Project is inactive. Cannot be updated.'),
    'CostcenterInactive': _('Project is inactive. Cost Center cannot be added / edited.'),
    'COSTCENTERINACTIVE': _('Project is inactive. Cost Center cannot be added / edited.'),
    'COSTCENTERPROGRAMINACTIVE': _('Program is inactive. Cost Center cannot be added / edited.'),
    'StageInactive':_('Project is inactive. Stage cannot be added / edited / deleted.'),
    'ProgramSave':_('Program saved successfully'),
    'List':_('listed successfully'),
    'ListErr' :_('list unsuccessful'),
    'programResourceSaved':_('project resource saved successfully'),
    'programResourceDeleted':_('project resource deleted successfully'),
    'project_initiated':_('Project initiated successfully'),
    'project_Approve':_('Project Approved successfully'),
    'project_Reject':_('Project was rejected')
    }

ACTION = 'List'
MODULE = 'Project'
ERROR_MESSAGE = '%s:%s:%s'
errMessage = ''
MSG = ''
USERTYPE = ['Internal', 'External']
DEFAULT_DATE = datetime.datetime(2000, 01, 01, 0, 0).date()
PLANNED_EFFORT = {'DAYS' : 1, 'MONTHS':12, 'YEARS':360}
BILLING_CATEGORY = {
        'Milestone': '1',
        'Time-Based': ['2', '3', '4', '5'],
        'Specific-Dates': '6'
        }

@login_required
def display_project_dashboard(request):
    """
        return project home page
    """
    login_data = request.session.get('LoginData', '')
    project_code = request.GET.get('ids', '')
    project_task_allocated = []
    try:
        project = Project.objects.get(code = project_code)
    except:
        raise Http404
    request.session['projectid'] = project.pk
    project_milestones = __getProjectList__(project)
    todays_events = Event.objects.filter(date =
        (datetime.date.today()), attendees = request.user)
    project_task_allocated = Task.objects.filter(assigned_resources
                                                            = request.user)[:5]
    project_resources = ProjectMembership.objects.filter(project
                                            = project).distinct()
    non_privileged_roles = ProjectRole.objects.all()
    return render(request, 'projectDashboard.html', {
        'title': 'Project Home', 'project':project, 'action': 'Update',
        'updatedStage': project_milestones,
        'todaysEvent': todays_events, 'resources': project_resources,
        'projectTasks': list(project_task_allocated),
        'roles': non_privileged_roles
        },)

def __getProjectList__(project):
    stageColour = {'colour':'a'}
    updatedStage = []
    for stage in project.milestone.filter(cancel = False).filter(category = Milestone.ENGINEERING):
        stageColour['colour'] = "gray"
        stage.__dict__.update(stageColour)
        updatedStage.append(stage)
    return updatedStage


##needed for calculation mail for invoice date
#def __calcInvoiceDate__(request, form):
#    if form.cleaned_data['invoicing_terms'] == '2':
#        form.cleaned_data['next_invoice_date'] = form.cleaned_data['approval_date'] + datetime.timedelta(days = 30)
#    elif form.cleaned_data['invoicing_terms'] == '3':
#        form.cleaned_data['next_invoice_date'] = form.cleaned_data['approval_date'] + datetime.timedelta(days = 120)
#    elif form.cleaned_data['invoicing_terms'] == '4':
#        form.cleaned_data['next_invoice_date'] = form.cleaned_data['approval_date'] + datetime.timedelta(days = 180)
#    elif form.cleaned_data['invoicing_terms'] == '5':
#        form.cleaned_data['next_invoice_date'] = form.cleaned_data['approval_date'] + datetime.timedelta(days = 365)
#    return form.cleaned_data['next_invoice_date']
#
#def __alertNotification__(request, project):
#    email_subject = 'project initiation mail'
#    email_message = 'project ' + str(project.shortName) + 'has been initaited'
#    try:
#        Email().send_email(email_subject, message,
#                        [each.owner.userProfile.authUser.email])
#    except Exception:
#        errMessage = 'Email Sending failed \n %s' % (Exception)
#    return

def get_project(request, project_code):
    """ return a project object """
    try:
        project = Project.objects.get(code = project_code)
    except:
        project = None
    request.session['projectid'] = project.id if project else ''
    return project

def save_milestone_formset(formset, project, invoice_terms = ''):
    """ save milestone from formset """
    formset = formset.save(commit = False)
    for each in formset:
        if invoice_terms:
            each.invoice_terms = invoice_terms
        each.save()
        project.milestone.add(each)


def validate(formList):
    """ validate the forms """
    validation = map(lambda form: form.is_valid(), formList)
    print validation
    if validation.__contains__(False):
        return False
    return True

def get_project_schedule(project_form, project):
    """ create project shedule object from form"""
    project_schedule = ProjectSchedule(
        approval_date = project_form.cleaned_data['approval_date'],
        planned_start_date = project_form.cleaned_data['planned_start_date'],
        planned_end_date = project_form.cleaned_data['planned_end_date']
        )
    if project:
        project_schedule.pk = project.schedules.pk
    return project_schedule

def get_project_details(request, project_form, project_schedule):
    """ create project object from form """
    effortUnit = request.POST.get('planned_effort_unit', 'DAYS')
    plannedEffort =  project_form.cleaned_data['planned_effort']
    if plannedEffort:
        plannedEffort = PLANNED_EFFORT[effortUnit]*plannedEffort
    project = Project(
        code = project_form.cleaned_data['code'],
        project_no = project_form.cleaned_data['project_no'],
        name = project_form.cleaned_data['project_name'],
        short_name = project_form.cleaned_data['short_name'],
        project_type_id = project_form.cleaned_data['project_type'],
        business_unit_id = project_form.cleaned_data['business_unit'],
        owner = project_form.cleaned_data['owner'],
        parent = project_form.cleaned_data['parent'],
        cancel = 0,
        planned_effort = plannedEffort,
        customer_contact_id = project_form.cleaned_data['customer_contact'],
        customer_id = project_form.cleaned_data['customer'],
        domain_id = project_form.cleaned_data['domain'],
        apex_body_owner = project_form.cleaned_data['apex_body_owner'],
        approval_type = project_form.cleaned_data['approval_type'],
        approval_reference = project_form.cleaned_data['approval_reference'],
        schedules_id = project_schedule.pk,
        )
    if not hasattr(project, 'customer'):
        project.customer = None
    try:
        project_instance = Project.objects.get(code
                    = project_form.cleaned_data['code'])
        project.pk = project_instance.pk
    except:
        pass
    return project

EXTRA_FORM = {'empty': 0, 'Milestone': 1}
def extra_form(project, invoice_terms):
    """ return the extra form for the formset """
    if project and len(get_milestone(project, invoice_terms)) > 0:
        return EXTRA_FORM['empty']
    return EXTRA_FORM['Milestone']

def get_milestone(project, invoice_terms):

    """ return the milestone for the formset based on the invoice terms """
    return project.milestone.filter(invoice_terms__in =
        invoice_terms) if project else Milestone.objects.none()

def init_milestone_formset(fields, can_delete, extra, max_num =''):
    """ initialize the milestone formset """
    milestone_form = modelformset_factory(Milestone,
        formset=VisiblePrimaryKeyFormset, fields=fields,
        can_delete= can_delete, extra= extra)
    if max_num: milestone_form.max_num = max_num
    return milestone_form

TIME_BASED_MAX_FORM = 1
@login_required
def project_initiation(request, msg = ''):
    '''
        Create and modify project.
    '''
    projectId = request.GET.get('ids',
        '') if request.method == 'GET' else request.POST.get('code', '')

    project = get_project(request, projectId)

    action = 'Update' if project else 'Create'
    MilestoneFormSet = init_milestone_formset(('name', 'percentage'), True,
        extra_form(project, BILLING_CATEGORY['Milestone']))
    TimeBasedFormSet =  init_milestone_formset(('invoice_terms',
        'start_date', 'end_date'), True, extra_form(project,
        BILLING_CATEGORY['Time-Based']), max_num = TIME_BASED_MAX_FORM)
    SpecificDatesFormSet = init_milestone_formset(('start_date', 'percentage'),
        True, extra_form(project, BILLING_CATEGORY['Specific-Dates']))

    if request.method == 'POST':
        project_form = ProjectInitiationForm(request.POST)
        milestone_form = MilestoneFormSet(request.POST, queryset=get_milestone(
            project, BILLING_CATEGORY['Milestone']), prefix = 'milestone')
        time_based_form = TimeBasedFormSet(request.POST, queryset=get_milestone(
            project, BILLING_CATEGORY['Time-Based']), prefix = 'timebased')
        specific_dates_form = SpecificDatesFormSet(request.POST, queryset =
            get_milestone(project, BILLING_CATEGORY['Specific-Dates']),
            prefix = 'specificdates')

        if validate([project_form, milestone_form, time_based_form,
                specific_dates_form]):

            project_schedule = get_project_schedule(project_form, project)
            project_schedule.save()
            project = get_project_details(request, project_form, project_schedule)
            project.save()
            save_milestone_formset(milestone_form, project,
                InvoiceTerms.objects.get(name='Milestone'))
            save_milestone_formset(time_based_form, project)
            save_milestone_formset(specific_dates_form, project,
                InvoiceTerms.objects.get(name='Specific-Date'))
            redirectionUrl = request.POST.get('redirectionUrl', '')
            return HttpResponseRedirect(redirectionUrl) if redirectionUrl else\
                project_list(request, msg = 'Project_Saved')
    else:
        project_form = ProjectInitiationForm(schedules = project.schedules,
           project= project) if project else ProjectInitiationForm()
        milestone_form = MilestoneFormSet(queryset = get_milestone(project,
            BILLING_CATEGORY['Milestone']), prefix='milestone')
        time_based_form = TimeBasedFormSet(queryset = get_milestone(project,
            BILLING_CATEGORY['Time-Based']), prefix='timebased')
        specific_dates_form = SpecificDatesFormSet(queryset = get_milestone(
            project, BILLING_CATEGORY['Specific-Dates']), prefix='specificdates')
    return render(request, 'project.html', {'title': 'Project',
        'action': action,
        'project': project, 'specific_dates_form': specific_dates_form,
        'form': project_form, 'milestone_form': milestone_form,
        'duplicatealert': actionMsg[msg], 'time_based_form':time_based_form},
        )

@login_required
def project_plan(request):
    """
        Planning and assigning resouces.
    """
    code = request.GET.get('ids', '')
    project = get_object_or_404(Project, code = code)
    TeamForm = make_responsibility_form(project = project)

    if request.method == 'POST':
        plan_form = PlanForm(data = request.POST, instance = project)
        team_form = TeamForm(data = request.POST)
        if plan_form.is_valid() and team_form.is_valid():
            project = plan_form.save()
            project = team_form.save()
    else:
        plan_form = PlanForm(instance = project)
        team_form = TeamForm()

    request.session['projectid'] = project.id if project else ''
    initiation_form = InitiationForm(instance = project, disabled = True)
    return render(request, 'project_plan.html', {
        'plan_form' : plan_form, 'initiation_form' : initiation_form,
        'team_form' : team_form, 'project': project,
        'user_set' : User.objects.filter(is_active = True, is_staff = False),
        'action': 'Update',
        },)

@login_required
def project_list(request, page = 1, msg = ''):
    """
        list the project for the users.
    """
    query = Q(is_active = True) & Q(is_approved = True)

    searchtext = request.GET.get('search', '')
    show_inactive = request.GET.get('is_active', '0')

    if searchtext:
        for term in searchtext.split():
            q = Q(name__icontains = term)
        query = query & q

    if int(show_inactive):
        query = query | Q(is_active = False)

    apex_body_owner = User.objects.filter(
                groups__name__icontains = 'Corporate Admin', is_active = True)
    for each in apex_body_owner:
        if str(request.user) == str(each.username):
            project_set  = Project.objects.all()
        else:
            project_set = Project.objects.filter(Q(apex_body_owner=request.user) |
                Q(owner=request.user) |
                Q(team=request.user) | Q(requested_by = request.user)).distinct().exclude(cancel = True)
    #print project_set

    return list_detail.object_list(
        request,
        queryset = project_set.filter(query),
        template_name = "project_list.html",
        template_object_name = "project",
        extra_context = {'msg': actionMsg[msg], 'show_inactive': int(show_inactive)}
    )

def manage_development_environment(request, id = None):
    """
        create/Edit development entity.
    """
    instance = None
    if id:
        instance = get_object_or_404(DevelopmentEntity, pk = id)
    if request.method == 'POST' :
        project_id = request.POST.get('project_id', None)
        project = get_object_or_404(Project, code = project_id)
        form = DevelopmentEnvironmentForm(request.POST, instance = instance)
        if form.is_valid() and request.is_ajax():
            instance = form.save()
            project.development_environment.add(instance)
            return  HttpResponse(simplejson.dumps([{'id':instance.pk,
                'resource':instance.__unicode__()}]),
                mimetype = 'application/json')
        else:
            return  HttpResponse(simplejson.dumps([{'error':form.errors}]),
                                             mimetype = 'application/json')
    else:
        form = DevelopmentEnvironmentForm(instance = instance)
    return render(request, 'development_environment.html', {
        'form': form})

def delete_development_environment(request):
    """
        delete the development environment.
    """
    DevelopmentEntity.objects.filter(pk__in
            = request.POST.get('todelete', '')).delete()
    return HttpResponse(mimetype = 'application/json')

@login_required
def ProgramDelete(request):
    """
        delete the project.
    """
    msg = ''
    programsToDelete = request.POST.getlist('project_pk')

    try:
        for program in programsToDelete:
            program = Project.objects.get(project_no = program)

            if program.milestone.all() or Event.objects.filter(name = program).exclude(cancel = True):
                msg = 'Deleteunsuccess'
            else:
                program.cancel = True
                program.save()
                msg = 'DeleteSuccess'
                CapturLog().LogData(request, 'Delete', MODULE, actionMsg[msg], program)
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(request, 'Delete', MODULE, errMessage)
    return project_list(request, msg=msg)

@login_required
def manage_project_status(request, is_active = True):
    """
        Change project status
    """
    if request.method == 'POST':
        ids = request.POST.getlist('project_pk')

        try:
            for project_id in ids:
                project = Project.objects.get(project_no = project_id)
                project.is_active = is_active
                project.save()
            messages.success(request, _('Project(s) status saved sucessfully'))
        except Exception as e:

            messages.error(request, _('Project(s) status change failed'))
    return HttpResponseRedirect(reverse(project_list))

#def manage_project_group(request, id=None):
#    id = request.POST.get('id', None) if request.method == 'POST' else id
#    try:
#        project_group = Project.objects.get(pk = id)
#    except:
#        project_group = None
#    if request.method == 'POST':
#        project_group_form = ProjectGroupForm(request.POST,
#                                        instance = project_group)
#        if project_group_form.is_valid():
#            project_group_form.save()
#    else:
#        project_group_form = ProjectGroupForm(instance = project_group)
#    return render(request, 'project_group_detail.html', { 'id' : id,
#        'form': project_group_form},
#        )
#
#@login_required
#def project_group_list(request, page = 1, msg = ''):
#    project_group = Project.objects.filter(id = F('parent__id'))
#    no_of_pages = (len(project_group)/settings.PAGE_SIZE) + 1
#    paginated_by, page_no = [settings.PAGE_SIZE, page
#                                        ] if int(page) > 0 else [None, None]
#    return list_detail.object_list(
#        request,
#        queryset = project_group,
#        template_name = "project_group_list.html",
#        template_object_name = "project_group",
#        paginate_by = paginated_by,
#        page = page_no,
#        extra_context = { "no_of_pages": no_of_pages, 'msg': actionMsg[msg] }
#        )

def EditProgramDisplayList(request):

    if request.user.has_perm('projects.add_project'):
        return project_initiation(request)
    else:
        return project_plan(request)

def ProgramContentDetails(request):
    program = request.session.get('projectid', default = None)
    if program != None:
        if len(Project.objects.filter(pk = program))>0:
            program = Project.objects.filter(pk = program)[0]
    return program

def get_clients(request):
    """
        Returns the customer contact for a given customer.
    """
    customer_id = request.GET.get('customer','')
    clients = UserProfile.objects.filter(business_unit
                = customer_id).order_by('user__first_name')
    client = []
    for each in clients:
        client.append( {'name':str(each.user.first_name + ' ' + each.user.last_name),
                        'id':each.pk} )
    json = simplejson.dumps(client)
    return HttpResponse(json, mimetype='application/javascript')

def manage_domain(request, id = ''):
    """
        Create/Edit the business unit from the project.
    """
    instance = None
    id = request.POST.get('domainID', '') if request.POST.get('domainID', '') != '' else id
    if id:
        instance = get_object_or_404(Domain, id = id)
    if request.method == 'POST':
        form = DomainForm(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            data = [{'id':instance.pk, 'resource':instance.__unicode__()}]
        else:
            data = [{'error':form.errors}]
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(data),
                        mimetype = 'application/json')
    else:
        form = DomainForm(instance = instance)
    return render(request, 'domain.html', {'form': form, 'domainID':id})

def manage_project_type(request, id = ''):
    """
        Create/Edit the project type from the project.
    """
    instance = None
    id = request.POST.get('projectTypeID', '') if request.POST.get('projectTypeID', '') != '' else id
    if id:
        instance = get_object_or_404(ProjectType, id = id)
    if request.method == 'POST':
        form = ProjectTypeForm(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            data = [{'id':instance.pk, 'resource':instance.__unicode__()}]
        else:
            data = [{'error':form.errors}]
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(data),
                            mimetype = 'application/json')
    else:
        form = ProjectTypeForm(instance = instance)
    return render(request, 'project_type.html',
        {'form': form, 'projectTypeID':id})

def manage_business_unit(request, id = ''):
    """
        Create/Edit business unit from the project.
    """
    instance = None
    id = request.POST.get('businessunitID', '') if request.POST.get('businessunitID', '') != '' else id
    if id:
        instance = get_object_or_404(ProjectType, id = id)
    if request.method == 'POST':
        form = BusinessUnitForm(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            data = [{'id':instance.pk, 'resource':instance.__unicode__()}]
        else:
            data = [{'error':form.errors}]
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(data),
                            mimetype = 'application/json')
    else:
        form = BusinessUnitForm(instance = instance)
    return render(request, 'business_unit.html',
        {'form': form, 'businessunitID':id})

def manage_project_group(request, id=None):
    """
        Create/Edit project group.
    """
    instance = None
    id = request.POST.get('project_group_id', None) if request.method == 'POST' else id
    if id:
        instance = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        form = ProjectGroupForm(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            data = [{'id': instance.pk, 'name':instance.__unicode__()}]
        else:
            data = [{'error': form.errors}]
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(data),
                mimetype = 'application/json')
    else:
        form = ProjectGroupForm(instance = instance)
    return render(request, 'project_group.html',
        {'form': form, 'project_group_id': id})

@login_required
def manage_project_initiation_request(request):
    """
        Create/Edit project Initiation request.
    """
    project =  None
    user = request.user.id
    is_approved = ''
    msg = ''
    schedules = addressClient = None
    specific_dates_form = None
    time_based_form = None
    milestone_form = None
    id = request.GET.get('id', None)
    user = ProjectInitiationRequestForm(user = request.user)
    MilestoneFormSet = init_milestone_formset(('name', 'percentage'), True, extra_form(project, BILLING_CATEGORY['Milestone']))
    TimeBasedFormSet =  init_milestone_formset(('invoice_terms',
        'start_date', 'end_date'), True, extra_form(project,
        BILLING_CATEGORY['Time-Based']), max_num = TIME_BASED_MAX_FORM)
    SpecificDatesFormSet = init_milestone_formset(('start_date', 'percentage'),
        True, extra_form(project, BILLING_CATEGORY['Specific-Dates']))
    if id:
        project = get_object_or_404(Project, code = id)
        schedules = project.schedules
        projectOwner  = project.customer
        address_client = BusinessUnit.objects.filter(type__name = 'Customer')
        for each in address_client:
            if str(projectOwner) == each.name:
                addressClient = each.address


        MilestoneFormSet = init_milestone_formset(('name', 'percentage'), True, extra_form(project, BILLING_CATEGORY['Milestone']))
        TimeBasedFormSet =  init_milestone_formset(('invoice_terms',
        'start_date', 'end_date'), True, extra_form(project,
        BILLING_CATEGORY['Time-Based']), max_num = TIME_BASED_MAX_FORM)
        SpecificDatesFormSet = init_milestone_formset(('start_date', 'percentage'),
        True, extra_form(project, BILLING_CATEGORY['Specific-Dates']))

    if request.method == 'POST':
        request_form = ProjectInitiationRequestForm(request.POST,
                            instance = project, user = request.user)
        schedules_form = ProjectSchedulesRequestForm(request.POST,
                            instance = schedules)

        if request.user.has_perm('projects.add_project'):
            if id:
                milestone_form = MilestoneFormSet(request.POST, queryset=get_milestone(
                    project, BILLING_CATEGORY['Milestone']), prefix = 'milestone')
                time_based_form = TimeBasedFormSet(request.POST, queryset=get_milestone(
                    project, BILLING_CATEGORY['Time-Based']), prefix = 'timebased')
                specific_dates_form = SpecificDatesFormSet(request.POST, queryset =
                    get_milestone(project, BILLING_CATEGORY['Specific-Dates']),
                    prefix = 'specificdates')


                if validate([milestone_form, time_based_form,specific_dates_form]):


                    save_milestone_formset(milestone_form, project,
                        InvoiceTerms.objects.get(name='Milestone'))
                    save_milestone_formset(time_based_form, project)
                    save_milestone_formset(specific_dates_form, project,
                    InvoiceTerms.objects.get(name='Specific-Date'))



        if request_form.is_valid() and schedules_form.is_valid():
            schedules = schedules_form.save()
            is_approved = request_form.cleaned_data['is_approvedby'] == 'Approve'
            request_form.save(schedules = schedules, is_approved = is_approved)

            if request.user.has_perm('projects.add_project') and id and is_approved != "":
                if is_approved:
                    email_message = "Project " + str(request_form.cleaned_data['name']) +  ' was approved by ' + str(request_form.cleaned_data['approved_by']) + ' on ' + str(schedules_form.cleaned_data['approved_date'])
                    #template = get_template('Approved_Project_Link_Mail.html')
                    #if request_form.is_valid():
                    #    project_id = Project.objects.get(name = request_form.cleaned_data['name'])
                    #    email_subject1 = "Print of Project detail"
                    #    recipent_list = ['raghunath@fifthgentech.com']
                    #    data = {'project_id': project_id.id,
                    #            'user': request.user,
                    #            'project': project_id}
                    #    email_message1 = template.render(Context(data))
                    #    for email_id in recipent_list:
                    #        Email().send_email(email_subject1, email_message1, [email_id], CONTENT_TYPE)
                else:
                    email_message = "Project " + str(request_form.cleaned_data['name']) +  ' was Rejected by ' + str(request_form.cleaned_data['approved_by']) + ' on ' + str(schedules_form.cleaned_data['approved_date'])
                email_subject = 'Project Approval Status'

                user = User.objects.get(username = request_form.cleaned_data['requested_by'])
                recipients = user.email


                try:
                    Email().send_email(email_subject, email_message, [recipients], CONTENT_TYPE)
                    if is_approved:
                        msg = 'project_Approve'
                    else:
                        msg = 'project_Reject'
                    #next = request.GET.get("next", None)
                    #if next:
                    #    return HttpResponseRedirect(next)
                except Exception:
                    errMessage = 'Email Sending failed \n %s' % (Exception)

            if (id == None) or (not request.user.has_perm('projects.add_project') and request.user.has_perm('projects.change_project') and id):

                email_subject = 'Project initiation request'
                if request_form.cleaned_data['project_type'].name == 'Others':
                    project_type =  str(request_form.cleaned_data['other_project_type']) + '\r\n'
                else:
                    project_type = str(request_form.cleaned_data['project_type']) + '\r\n'



                user = User.objects.get(username = request_form.cleaned_data['approved_by'])
                recipients = user.email

                template = get_template('Project_Initiate_Request_Mail.html')
                data = {'project_name' : request_form.cleaned_data['name'],
                        'user_name' : request.user,
                        'request_date' : schedules_form.cleaned_data['initiation_request_date'],
                        'division' : request_form.cleaned_data['business_unit'],
                        'project_category' : request_form.cleaned_data['approval_type'],
                        'project_type' :  project_type,
                        'expected_start_date' : schedules_form.cleaned_data['expected_start_date'],
                        'expected_end_date' : schedules_form.cleaned_data['expected_end_date'],
                        'estimated_efforts' : request_form.cleaned_data['planned_effort'],
                        'objective' : request_form.cleaned_data['objective'],
                        'approved_by': request_form.cleaned_data['approved_by'],
                        }
                email_message = template.render(Context(data))

                try:
                    Email().send_email(email_subject, email_message, [recipients], CONTENT_TYPE)
                    msg = 'project_initiated'
                except Exception:
                    errMessage = 'Email Sending failed \n %s' % (Exception)
        #next = request.GET.get("next", None)
        #if next:
        #    return HttpResponseRedirect(next)


    else:


        request_form = ProjectInitiationRequestForm(instance = project,
                                            user = request.user)
        schedules_form = ProjectSchedulesRequestForm(instance = schedules)
        milestone_form = MilestoneFormSet(queryset = get_milestone(project,
            BILLING_CATEGORY['Milestone']), prefix='milestone')
        time_based_form = TimeBasedFormSet(queryset = get_milestone(project,
            BILLING_CATEGORY['Time-Based']), prefix='timebased')
        specific_dates_form = SpecificDatesFormSet(queryset = get_milestone(
            project, BILLING_CATEGORY['Specific-Dates']), prefix='specificdates')


    return render(request, 'project_initiation_request.html',
        {'request_form': request_form, 'schedules_form': schedules_form,  'msg': actionMsg[msg], 'is_approved': is_approved,
          'specific_dates_form': specific_dates_form,
        'milestone_form': milestone_form,'user': user,
         'time_based_form':time_based_form, 'project': project, 'schedules': schedules, 'addressClient': addressClient},
        )

def project_request_list(request, page = 1, msg = ''):
    """
        list the project for the users.
    """

    query = Q(is_active = True) & Q(is_approved = False)
    searchtext = request.GET.get('search', '')

    if searchtext:
        for term in searchtext.split():
            q = Q(name__icontains = term)
        query = query & q



    if request.user.has_perm('projects.add_project'):
        project_set = Project.objects.filter(Q(apex_body_owner=request.user) |
            Q(owner=request.user) |
            Q(team=request.user) | Q(approved_by = request.user)).distinct().exclude(cancel = True)
    else:
        project_set = Project.objects.filter(Q(requested_by=request.user))


    return list_detail.object_list(
        request,
        queryset = project_set.filter(query).exclude(requested_by = None).order_by('-project_no'),
        template_name = "Project_initiation_request_list.html",
        template_object_name = "project_request",
        extra_context = {'msg': actionMsg[msg],
        }
    )

def print_project_details(request,id=None):
    form = Project.objects.get(id=id)
    return render(request, 'Approved_project_print.html',
        {'project': form},
        )
