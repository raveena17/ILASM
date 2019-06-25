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
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
# import json
# from django.utils import simplejson
try:
    import django.utils.simplejson
except:
    import json as simplejson
    
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from dateutil.relativedelta import relativedelta


from project_management import settings
from logs.logger import CapturLog
from notifications.models import Event
from projects.forms import  ProjectInitiationForm, \
    VisiblePrimaryKeyFormset, ProjectGroupForm, ProjectInitiationRequestForm,\
    ProjectSchedulesRequestForm
from projects.models import DevelopmentEntity, ProjectRole, \
    ProjectSchedule, Project,  ProjectMembership, Domain, ProjectType, ProjectAlertTime
from milestone.models import Milestone, InvoiceTerms
from projects.plan.forms import PlanForm, InitiationForm, \
    make_responsibility_form, DevelopmentEnvironmentForm
from common_manager.master_forms import DomainForm, \
    ProjectTypeForm
from projects.forms import BusinessUnitForm
from tasks.models import Task
from users.models import UserProfile
from Utility import Email
from customer.models import Customer
from business_unit.models import BusinessUnit
from projectbudget.views import  budget_alert_mail
from projectbudget.models import *
from alert.views import alert_generate

 from django.shortcuts import render



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
    'int_project_Approve':_('Project has been internally approved.'),
    'ext_project_Approve':_('Project has been approved.'),
    'project_Approve':_('Project has been approved.'),
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

class SubListView(ListView):
    extra_context = {}
    def get_context_data(self, **kwargs):
        context = super(SubListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
        
@login_required
def display_project_dashboard(request):
    """
        return project home page
    """
    login_data = request.session.get('LoginData', '')
    project_id = request.GET.get('ids', '')
    project_task_allocated = []
    try:
        project = Project.objects.get(id = project_id)
    except:
        raise Http404
    request.session['projectid'] = project.pk
    project_milestones = __getProjectList__(project)
    todays_events = Event.objects.filter(date =
        (datetime.date.today()), attendees = request.user)
    it_admin_user = User.objects.filter(id = request.user.id,
                 groups__name__icontains = 'IT Admin', is_active = True)    
    project_task_allocated = Task.objects.filter(assigned_resources
                                                            = request.user)[:5]
    project_resources = ProjectMembership.objects.filter(project
                                            = project).distinct()
    non_privileged_roles = ProjectRole.objects.all()
    return render(request, 'projectDashboard.html', {
        'title': 'Project Home', 'project':project,'it_admin_user':it_admin_user, 'action': 'Update',
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
        project = Project.objects.get(id = project_code)
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
        estimation_no = project_form.cleaned_data['estimation_no'],
        proposal_name = project_form.cleaned_data['proposal_name'],
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
        '') if request.method == 'GET' else request.POST.get('ids', '')

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
        project_form = ProjectInitiationForm(schedules = project.schedules,project= project) if project else ProjectInitiationForm()
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
    id = request.GET.get('ids', '')
    project = get_object_or_404(Project, id = id)
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
    budget_bus_head = ProjectBudget.objects.filter(\
        business_head__id=request.user.id, budget_updated=1).values('project_id')

    if searchtext:
        for term in searchtext.split():
            q = Q(name__icontains = term)
        query = query & q

    if int(show_inactive):
        query = Q(is_active = False)
    apex_body_owner = User.objects.filter(id = request.user.id,
                groups__name__icontains = 'Corporate Admin', is_active = True)
    it_admin_user = User.objects.filter(id = request.user.id,
                 groups__name__icontains = 'IT Admin', is_active = True)
    if len(apex_body_owner) > 0 or len(it_admin_user) > 0:
        project_set  = Project.objects.all()
    else:
        project_set = Project.objects.filter(Q(apex_body_owner=request.user) |
                Q(owner=request.user) | 
                Q(team=request.user) | Q(requested_by = request.user)\
                | Q(id__in=budget_bus_head)).distinct().exclude(cancel = True)
    callable = SubListView.as_view(
        queryset = project_set.filter(query).order_by('-id'),
        template_name = "project_list.html",
        context_object_name = "project_list",
        extra_context = {'msg': actionMsg[msg], 'show_inactive': int(show_inactive)}
    )
    return callable(request)

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
            return  HttpResponse(json.dumps([{'id':instance.pk,
                'resource':instance.__unicode__()}]),
                mimetype = 'application/json')
        else:
            return  HttpResponse(json.dumps([{'error':form.errors}]),
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
#    return render_to_response('project_group_detail.html', { 'id' : id,
#        'form': project_group_form},
#        context_instance = RequestContext(request))
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
    json = json.dumps(client)
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
            return HttpResponse(json.dumps(data),
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
            return HttpResponse(json.dumps(data),
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
            return HttpResponse(json.dumps(data),
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
            return HttpResponse(json.dumps(data),
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
    email_to_list = []
    email_request_list = []
    schedules = addressClient = None
    specific_dates_form = None
    time_based_form = None
    milestone_form = None
    id = request.GET.get('id', None)
    user = ProjectInitiationRequestForm(user = request.user)
    project_category = ''
    MilestoneFormSet = init_milestone_formset(('name', 'percentage'), True, extra_form(project, BILLING_CATEGORY['Milestone']))
    TimeBasedFormSet =  init_milestone_formset(('invoice_terms',
        'start_date', 'end_date'), True, extra_form(project,
        BILLING_CATEGORY['Time-Based']), max_num = TIME_BASED_MAX_FORM)
    SpecificDatesFormSet = init_milestone_formset(('start_date', 'percentage'),
        True, extra_form(project, BILLING_CATEGORY['Specific-Dates']))
    if id:
        project = get_object_or_404(Project, id = id)
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
            ex_appr = request.POST.get('ex_appr',0)
            is_approved = request_form.cleaned_data['is_approvedby'] == 'Approve'
            pjtid=request_form.save(schedules = schedules, is_approved = is_approved, ex_approval=ex_appr)
            

            if request.user.has_perm('projects.add_project') and id and is_approved != "":
                if is_approved:
                    email_message = "Project " + str(request_form.cleaned_data['name']) +  ' was approved by '
                    email_message += str(request_form.cleaned_data['approved_by'])
                    if str(ex_appr) == '1':
                        email_message += ' upon customer approval'
                    else:
                        email_message += ' pending customer approval'
                    email_message += ' on ' + str(schedules_form.cleaned_data['approved_date'])
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
                    
                    user = User.objects.get(username = request_form.cleaned_data['requested_by'])
                    recipients = user.email
                    email_to_list.append(recipients)
                    email_message = "Project " + str(request_form.cleaned_data['name']) +  ' was Rejected by ' + str(request_form.cleaned_data['approved_by']) + ' on ' + str(schedules_form.cleaned_data['approved_date']) +'</br></br>Rejection Reason :' + str(request_form.cleaned_data['rejection_reason']) 
                    alert_generate(request, 'Project', 'alertdataconfig17',id, email_to_list)
                    

                user = User.objects.get(username = request_form.cleaned_data['requested_by'])
                recipients = user.email
                email_to_list.append(recipients)
                
                project_name = str(request.POST.get('name'))
                user_name = str(request_form.cleaned_data['requested_by'].username)
                request_date = str(schedules_form.cleaned_data['initiation_request_date'])
                bus_unit=  str(request_form.cleaned_data['business_unit'].name)
                delivery_centre = str(request_form.cleaned_data['delivery_centre'].name)
                project_category = str(request.POST.get('approval_type'))
                project_type = str(request_form.cleaned_data['project_type'])
                expected_start_date = str(schedules_form.cleaned_data['expected_start_date'])
                expected_end_date =str(schedules_form.cleaned_data['expected_end_date'])
                estimated_efforts = str(request_form.cleaned_data['planned_effort'])
                objective = request_form.cleaned_data['objective']
                rejected_reason = str(request_form.cleaned_data['rejection_reason'])
                
                email_message += "<table width='50%'><tr><td></br>Requested by</td><td>:</td><td>"+ user_name + "</td></tr><tr><td></br>Requested on</td><td>:</td>"
                email_message += "<td>"+request_date+"</td></tr><tr><td></br>Business Unit</td><td>:</td><td>"
                email_message += bus_unit+"</td></tr><tr><td></br>Delivery Centre</td><td>:</td><td>"+ delivery_centre +"</td></tr><tr><td></br>Project Name</td><td>:</td><td>"+project_name+"</td></tr>"
                email_message += "<td></br>Project Category</td><td>:</td><td>" + project_category +"</td></tr><tr><td></br>Project Type</td><td>:</td><td>" + project_type + "</td></tr>"
                email_message += "<tr><td></br>Expected Start Date</td><td>:</td><td>"+expected_start_date+"</td><tr><td></br>Expected End Date</td><td>:</td>"
                email_message += "<td>"+expected_end_date+"</td></tr><tr><td></br>Estimated Efforts(man-days)</td><td>:</td><td>"+estimated_efforts+"</td>"
                email_message += "</tr><tr><td></br>Objectives</td><td>:</td><td>"+objective+"</td></tr></table></body></html>"
                email_subject = 'Project Approval Status'

                try:
                    #Email().send_email(email_subject, email_message, [recipients], CONTENT_TYPE)
                    if  rejected_reason == '':
                        if str(ex_appr) == '1' :
                            alert_generate(request, 'Project', 'alertdataconfig13',id, email_to_list)
                        else:
                            alert_generate(request, 'Project', 'alertdataconfig14',id, email_to_list)
                        if is_approved:
                            if project_category == 'internal':
                                msg = 'project_Approve'
                                budget_alert_mail(request, request.GET.get('id', None))
                            else:
                                if str(ex_appr) == '1':
                                    msg = 'ext_project_Approve'       
                                    budget_alert_mail(request, request.GET.get('id', None))
                                else:
                                    msg = 'int_project_Approve'
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
                email_to_list.append(recipients)
                user = User.objects.get(username = request_form.cleaned_data['requested_by'])
                recipients = user.email
                email_request_list.append(recipients)

#                template = get_template('Project_Initiate_Request_Mail.html')
#                data = {'project_name' : request_form.cleaned_data['name'],
#                        'user_name' : request.user,
#                        'request_date' : schedules_form.cleaned_data['initiation_request_date'],
#                        'delivery_centre' : request_form.cleaned_data['delivery_centre'],
#                        'bus_unit' : request_form.cleaned_data['business_unit'],
#                        'project_category' : request_form.cleaned_data['approval_type'],
#                        'project_type' :  project_type,
#                        'expected_start_date' : schedules_form.cleaned_data['expected_start_date'],
#                        'expected_end_date' : schedules_form.cleaned_data['expected_end_date'],
#                        'estimated_efforts' : request_form.cleaned_data['planned_effort'],
#                        'objective' : request_form.cleaned_data['objective'],
#                        'approved_by': request_form.cleaned_data['approved_by'],
#                        }
#                email_message = template.render(Context(data))
                approved_by =  str(request_form.cleaned_data['approved_by'].username)
                project_name = str(request.POST.get('name'))
                user_name = str(request.user.username)
                request_date = str(schedules_form.cleaned_data['initiation_request_date'])
                bus_unit=  str(request_form.cleaned_data['business_unit'].name)
                delivery_centre = str(request_form.cleaned_data['delivery_centre'].name)
                project_category = str(request.POST.get('approval_type'))
                project_type = project_type
                expected_start_date = str(schedules_form.cleaned_data['expected_start_date'])
                expected_end_date =str(schedules_form.cleaned_data['expected_end_date'])
                estimated_efforts = str(request_form.cleaned_data['planned_effort'])
                objective = request_form.cleaned_data['objective']
                
                mail_content =" <html lang='en'><p><b>Dear "+approved_by +"<br/>&nbsp;&nbsp;&nbsp;Project " +project_name +" has been initiated by "+user_name+" on " + request_date + "</b></p>"
                mail_content += "<table width='50%'><tr><td>Requested by</td><td>:</td><td>"+ user_name + "</td></tr><tr><td>Requested on</td><td>:</td>"
                mail_content += "<td>"+request_date+"</td></tr><tr><td>Business Unit</td><td>:</td><td>"
                mail_content += bus_unit+"</td></tr><tr><td>Delivery Centre</td><td>:</td><td>"+ delivery_centre +"</td></tr><tr><td>Project Name</td><td>:</td><td>"+project_name+"</td></tr>"
                mail_content += "<td>Project Category</td><td>:</td><td>" + project_category +"</td></tr><tr><td>Project Type</td><td>:</td><td>" + project_type + "</td></tr>"
                mail_content += "<tr><td>Expected Start Date</td><td>:</td><td>"+expected_start_date+"</td><tr><td>Expected End Date</td><td>:</td>"
                mail_content += "<td>"+expected_end_date+"</td></tr><tr><td>Estimated Efforts(man-days)</td><td>:</td><td>"+estimated_efforts+"</td>"
                mail_content += "</tr><tr><td>Objectives</td><td>:</td><td>"+objective+"</td></tr></table></body></html>"

                try:
                    #Email().send_email(email_subject, mail_content, [recipients], CONTENT_TYPE)
                    alert_generate(request, 'Project', 'alertdataconfig12',pjtid.id, email_to_list)
                    alert_generate(request, 'Project', 'alertdataconfig16',pjtid.id, email_request_list)
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
        'milestone_form': milestone_form,'user': user,'approval_type':project_category,
         'time_based_form':time_based_form, 'project': project, 'schedules': schedules, 'addressClient': addressClient},
        )
        
def ext_appr_cron(request):
    """
    Alert mail for External approval of a project though python cron job
    """
    alert_on = settings.ALERT_ON
    alert_reminder = settings.ALERT_REMINDER
    projects = Project.objects.filter(ex_approval=False, is_approved=True, is_active=True).exclude(cancel=True)
    projects = projects.filter(schedules__approved_date__lt =  datetime.datetime.now().date() - relativedelta(days=alert_on))
    flag = False
    for pjt in projects:
        alerttime_details = ProjectAlertTime.objects.filter(record_id=pjt.id)
        if len(alerttime_details) > 0:
            last_alert_with_days = alerttime_details[0].raised_on + relativedelta(days=alert_reminder)
            if datetime.datetime.now().date() >= last_alert_with_days:
                alerttime_details.update(raised_on=datetime.datetime.now().date())
                flag = True
        else:
            alert_time = ProjectAlertTime(record_id=pjt.id,
                                raised_on=datetime.datetime.now().date())
            alert_time.save()
            flag = True
        if flag:
            user = User.objects.get(id = pjt.approved_by.id)
            recipients = user.email
#            recipients = 'smila@fifthgentech.com'
            approved_by =  str(User.objects.get(id = pjt.approved_by.id).username)
            project_name = str(pjt.name)
            user_name = str(User.objects.get(id = pjt.requested_by.id).username)
            request_date = str(pjt.schedules.initiation_request_date)
            delay_days = str((datetime.datetime.now().date() - pjt.schedules.approved_date).days)
            print 'delay_days', delay_days
            email_subject = "Need customer approval for " + project_name +" project"
            mail_content =" <html lang='en'><p>Dear "+approved_by +"<br/><br/>&nbsp;&nbsp;&nbsp;The project "
            mail_content += project_name +" has not yet got customer approval and is active for past "+ delay_days +" days."
            mail_content += "</p><br/>Thanks.</html>"

            try:
                Email().send_email(email_subject, mail_content, [recipients], CONTENT_TYPE)
                msg = ' Alert mail for project approval'
            except Exception:
                errMessage = 'Email Sending failed \n %s' % (Exception)

def project_request_list(request, page = 1, msg = ''):
    """
        list the project for the users.
    """

    query = Q(is_active = True) & ( Q(ex_approval = 0) |  Q(is_approved = 0))
    searchtext = request.GET.get('search', '')

    if searchtext:
        print "Hi...",searchtext
        if(searchtext == "Waiting for approval"):
            for term in searchtext.split():
                q = Q(name__icontains = term) | Q(is_approved = 0)
            query = query & q            
        elif(searchtext == "Waiting for customer approval"):
            for term in searchtext.split():
                q = Q(name__icontains = term) | Q(is_approved = 1)
            query = query & q



    if request.user.has_perm('projects.add_project'):
        project_set = Project.objects.filter(Q(apex_body_owner=request.user) |
            Q(owner=request.user) |
            Q(team=request.user) | Q(approved_by = request.user)).distinct().exclude(cancel = True)
    else:
        project_set = Project.objects.filter(Q(requested_by=request.user))


    callable = SubListView.as_view(
        queryset = project_set.filter(query).exclude(requested_by = None).order_by('-project_no'),
        template_name = "Project_initiation_request_list.html",
        context_object_name = "project_request_list",
        extra_context = {'msg': actionMsg[msg]}
    )
    return callable(request)

def print_project_details(request,id=None):
    
    form = Project.objects.get(id=id)
    it_admin_user = User.objects.filter(id = request.user.id,
                 groups__name__icontains = 'IT Admin', is_active = True)
    return render(request, 'Approved_project_print.html',
        {'project': form, 'it_admin_user':it_admin_user},
        )


