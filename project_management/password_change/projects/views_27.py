
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
except BaseException:
    import json as simplejson

from django.utils.translation import ugettext as _
#from django.views.generic import list_detail
from dateutil.relativedelta import relativedelta


from project_management import settings
from project_management.logs.logger import CapturLog
from project_management.notifications.models import Event
from project_management.projects.forms import ProjectInitiationForm, \
    VisiblePrimaryKeyFormset, ProjectGroupForm, ProjectInitiationRequestForm,\
    ProjectSchedulesRequestForm,ProjectBillingDetailForm
from project_management.projects.models import DevelopmentEntity, ProjectRole, \
    ProjectSchedule, Project, ProjectMembership, Domain, ProjectType, ProjectAlertTime
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
from project_management.projectbudget.views import budget_alert_mail
from project_management.projectbudget.models import *
from project_management.alert.views import alert_generate
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from project_management.projects.forms import *

import datetime
CONTENT_TYPE = 'html'

actionMsg = {
    '': '',
    'Duplicate': _('Project name already exists.'),
    'Create': _('Create'),
    'CreateError': _('Create unsuccessful'),
    'Update': _('Update'),
    'UpdateError': _('Update unsuccessful'),
    'Project_Saved': _('Project saved successfully'),
    'SAVE': _('Resource added successfully'),
    'SaveError': _('Project save unsuccessful'),
    'DeleteSuccess': _('Project deleted successfully'),
    'Deleteunsuccess': _('Project is dependent. Cannot be deleted.'),
    'Stagedeletesuccess': _('Stage deleted successfully'),
    'Stagedeleteunsuccess': _('Stage is dependent and cannot be deleted.'),
    'Access Denied': _('Access Denied'),
    'CostCenterSave': _('Department saved successfully'),
    'CostCenterDuplicate': _('Department name already exists'),
    'Stage': _(''),
    'StageSave': _('Milestone saved successfully'),
    'StageSaveErr': _('Milestone save unsuccessful'),
    'DuplicateStage': _('Milestone name already exists.'),
    'ProgramInactive': _('Project cannot be saved for an inactive Program.'),
    'Inactive': _('Project is inactive. Cannot be updated.'),
    'CostcenterInactive': _('Project is inactive. Cost Center cannot be added / edited.'),
    'COSTCENTERINACTIVE': _('Project is inactive. Cost Center cannot be added / edited.'),
    'COSTCENTERPROGRAMINACTIVE': _('Program is inactive. Cost Center cannot be added / edited.'),
    'StageInactive': _('Project is inactive. Stage cannot be added / edited / deleted.'),
    'ProgramSave': _('Program saved successfully'),
    'List': _('listed successfully'),
    'ListErr': _('list unsuccessful'),
    'programResourceSaved': _('project resource saved successfully'),
    'programResourceDeleted': _('project resource deleted successfully'),
    'project_initiated': _('Project initiated successfully'),
    'int_project_Approve': _('Project has been internally approved.'),
    'ext_project_Approve': _('Project has been approved.'),
    'project_Approve': _('Project has been approved.'),
    'project_Reject': _('Project was rejected')
}

ACTION = 'List'
MODULE = 'Project'
ERROR_MESSAGE = '%s:%s:%s'
errMessage = ''
MSG = ''
USERTYPE = ['Internal', 'External']
DEFAULT_DATE = datetime.datetime(2000, 0o1, 0o1, 0, 0).date()
PLANNED_EFFORT = {'DAYS': 1, 'MONTHS': 12, 'YEARS': 360}
BILLING_CATEGORY = {
    'Milestone': '1',
    'Time-Based': ['2', '3', '4', '5'],
    'Specific-Dates': '6'
}


class ProjectListView(ListView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

show_inactive = 0
@login_required
def project_list(request, page=1, msg=''):
    """
        list the project for the users.
    """
    query = Q(is_active=True) & Q(is_approved=True)

    searchtext = request.GET.get('search', '')

    if request.GET.get('is_active'):
        global show_inactive
        show_inactive = request.GET.get('is_active')
        
    # show_inactive = request.GET.get('is_active', '0')
    budget_bus_head = ProjectBudget.objects.filter(
        business_head__id=request.user.id, budget_updated=1).values('project_id')

    if searchtext:
        for term in searchtext.split():
            q = Q(name__icontains=term)
        query = query & q

    if int(show_inactive):
        query = Q(is_active=False)
    apex_body_owner = User.objects.filter(id=request.user.id,
                                          groups__name__icontains='Corporate Admin', is_active=True)  # request.user.id = 307L
    it_admin_user = User.objects.filter(id=request.user.id,
                                        groups__name__icontains='IT Admin', is_active=True)  # it_admin_user= [<User: raveena>]
    if len(apex_body_owner) > 0 or len(
            it_admin_user) > 0:  # len(apex_body_owner) = 0 , 0>0 = false
        project_set = Project.objects.all()
    else:
        project_set = Project.objects.filter(Q(apex_body_owner=request.user) |
                                             Q(owner=request.user) |
                                             Q(team=request.user) | Q(
                                                 requested_by=request.user)
                                             | Q(id__in=budget_bus_head)).distinct().exclude(cancel=True)  # (apex_body_owner=request.user) for all  (<User: raveena>=<User: raveena>) condition is True
    callable = ProjectListView.as_view(
        queryset=project_set.filter(query).order_by('-id'),
        template_name="project_list.html",
        context_object_name="project_list",
        extra_context={
            'msg': actionMsg[msg],
            'show_inactive': int(show_inactive)},
        paginate_by=20
    )
    return callable(request)


@login_required
def display_project_dashboard(request):
    """
        return project home page
    """
    login_data = request.session.get('LoginData', '')
    project_id = request.GET.get('ids', '')
    project_task_allocated = []
    try:
        project = Project.objects.get(id=project_id)
    except BaseException:
        raise Http404
    request.session['projectid'] = project.pk
    project_milestones = __getProjectList__(project)
    todays_events = Event.objects.filter(
        date=(datetime.date.today()), attendees=request.user)
    it_admin_user = User.objects.filter(id=request.user.id,
                                        groups__name__icontains='IT Admin', is_active=True)
    project_task_allocated = Task.objects.filter(
        assigned_resources=request.user)[:5]
    project_resources = ProjectMembership.objects.filter(
        project=project).distinct()
    non_privileged_roles = ProjectRole.objects.all()
    return render(request, 'projectDashboard.html', {
        'title': 'Project Home', 'project': project, 'it_admin_user': it_admin_user, 'action': 'Update',
        'updatedStage': project_milestones,
        'todaysEvent': todays_events, 'resources': project_resources,
        'projectTasks': list(project_task_allocated),
        'roles': non_privileged_roles
    },)


def __getProjectList__(project):
    stageColour = {'colour': 'a'}
    updatedStage = []
    for stage in project.milestone.filter(
            cancel=False).filter(category=Milestone.ENGINEERING):
        stageColour['colour'] = "gray"
        stage.__dict__.update(stageColour)
        updatedStage.append(stage)
        # print updateStage
    return updatedStage

def get_project(request, project_code):
    """ return a project object """
    try:
        project = Project.objects.get(id=project_code)
    except BaseException:
        project = None
    request.session['projectid'] = project.id if project else ''
    return project


def save_milestone_formset(formset, project, invoice_terms=''):
    """ save milestone from formset """
    formset = formset.save(commit=False)
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
        approval_date=project_form.cleaned_data['approval_date'],
        planned_start_date=project_form.cleaned_data['planned_start_date'],
        planned_end_date=project_form.cleaned_data['planned_end_date']
    )
    if project:
        project_schedule.pk = project.schedules.pk
    return project_schedule


def get_project_details(request, project_form, project_schedule):
    """ create project object from form """
    effortUnit = request.POST.get('planned_effort_unit', 'DAYS')
    plannedEffort = project_form.cleaned_data['planned_effort']
    if plannedEffort:
        plannedEffort = PLANNED_EFFORT[effortUnit] * plannedEffort
    project = Project(
        code=project_form.cleaned_data['code'],
        project_no=project_form.cleaned_data['project_no'],
        name=project_form.cleaned_data['project_name'],
        short_name=project_form.cleaned_data['short_name'],
        project_type_id=project_form.cleaned_data['project_type'],
        business_unit_id=project_form.cleaned_data['business_unit'],
        owner=project_form.cleaned_data['owner'],
        parent=project_form.cleaned_data['parent'],
        cancel=0,
        planned_effort=plannedEffort,
        customer_contact_id=project_form.cleaned_data['customer_contact'],
        customer_id=project_form.cleaned_data['customer'],
        domain_id=project_form.cleaned_data['domain'],
        apex_body_owner=project_form.cleaned_data['apex_body_owner'],
        approval_type=project_form.cleaned_data['approval_type'],
        approval_reference=project_form.cleaned_data['approval_reference'],
        #estimation_no = project_form.cleaned_data['estimation_no'],
        #proposal_name = project_form.cleaned_data['proposal_name'],
        schedules_id=project_schedule.pk,
    )
    if not hasattr(project, 'customer'):
        project.customer = None
    try:
        project_instance = Project.objects.get(
            code=project_form.cleaned_data['code'])
        project.pk = project_instance.pk
    except BaseException:
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
    return project.milestone.filter(
        invoice_terms__in=invoice_terms) if project else Milestone.objects.none()


def init_milestone_formset(fields, can_delete, extra, max_num=''):
    """ initialize the milestone formset """
    milestone_form = modelformset_factory(ProjectBillingDetails,
                                          formset=VisiblePrimaryKeyFormset, fields=fields,
                                          can_delete=can_delete, extra=extra)
    if max_num:
        milestone_form.max_num = max_num
    return milestone_form


TIME_BASED_MAX_FORM = 1


@login_required
@permission_required('users.add_userprofile')
def project_initiation(request, msg=''):
    '''
        Create and modify project.
    '''
    projectId = request.GET.get('ids','') if request.method == 'GET' else request.POST.get('ids', '')

    project = get_project(request, projectId)

    action = 'Update' if project else 'Create'

    if request.method == 'POST':
        project_form = ProjectInitiationForm(request.POST)

        if validate([project_form]):
            project_schedule = get_project_schedule(project_form, project)
            project_schedule.save()

            project = get_project_details(
                request, project_form, project_schedule)
            project.save()

            redirectionUrl = request.POST.get('redirectionUrl', '')
            return HttpResponseRedirect(redirectionUrl) if redirectionUrl else\
                project_list(request, msg='Project_Saved')
    else:
        project_form = ProjectInitiationForm(
            schedules=project.schedules,
            project=project) if project else ProjectInitiationForm()
       
    return render(request, 'project.html', {'title': 'Project',
                                            'action': action,
                                            'project': project,'form': project_form})


@login_required
def project_plan(request):
    """
        Planning and assigning resouces.
    """
    id = request.GET.get('ids', '')
    project = get_object_or_404(Project, id=id)
    TeamForm = make_responsibility_form(project=project)

    if request.method == 'POST':
        plan_form = PlanForm(data=request.POST, instance=project)
        team_form = TeamForm(data=request.POST)
        if plan_form.is_valid() and team_form.is_valid():
            project = plan_form.save()
            project = team_form.save()
    else:
        plan_form = PlanForm(instance=project)
        team_form = TeamForm()

    request.session['projectid'] = project.id if project else ''
    initiation_form = InitiationForm(instance=project, disabled=True)
    return render(request, 'project_plan.html', {
        'plan_form': plan_form, 'initiation_form': initiation_form,
        'team_form': team_form, 'project': project,
        'user_set': User.objects.filter(is_active=True, is_staff=False),
        'action': 'Update',
    },)


def manage_development_environment(request, id=None):
    """
        create/Edit development entity.
    """
    instance = None
    if id:
        instance = get_object_or_404(DevelopmentEntity, pk=id)
    if request.method == 'POST':
        project_id = request.POST.get('project_id', None)
        project = get_object_or_404(Project, code=project_id)
        form = DevelopmentEnvironmentForm(request.POST, instance=instance)
        if form.is_valid() and request.is_ajax():
            instance = form.save()
            project.development_environment.add(instance)
            return HttpResponse(simplejson.dumps([{'id': instance.pk,
                                                   'resource': instance.__unicode__()}]),
                                content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps([{'error': form.errors}]),
                                content_type='application/json')
    else:
        form = DevelopmentEnvironmentForm(instance=instance)
    return render(request, 'development_environment.html', {
        'form': form})


def delete_development_environment(request):
    """
        delete the development environment.
    """
    DevelopmentEntity.objects.filter(
        pk__in=request.POST.get(
            'todelete', '')).delete()
    return HttpResponse(content_type='application/json')


@login_required
def ProgramDelete(request):
    """
        delete the project.
    """
    msg = ''
    programsToDelete = request.POST.getlist('project_pk')

    try:
        for program in programsToDelete:
            program = Project.objects.get(project_no=program)

            if program.milestone.all() or Event.objects.filter(
                    name=program).exclude(cancel=True):
                msg = 'Deleteunsuccess'
            else:
                program.cancel = True
                program.save()
                msg = 'DeleteSuccess'
                CapturLog().LogData(
                    request, 'Delete', MODULE, actionMsg[msg], program)
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(request, 'Delete', MODULE, errMessage)
    return project_list(request, msg=msg)


@login_required
@permission_required('users.add_userprofile')
def manage_project_status(request, is_active=True):
    """
        Change project status
    """
    if request.method == 'POST':
        ids = request.POST.getlist('project_pk')

        try:
            for project_id in ids:
                project = Project.objects.get(project_no=project_id)
                project.is_active = is_active
                project.save()
            messages.success(request, _('Project(s) status saved sucessfully'))
        except Exception as e:

            messages.error(request, _('Project(s) status change failed'))
    return HttpResponseRedirect(reverse(project_list))

@csrf_exempt
def EditProgramDisplayList(request):

    if request.user.has_perm('projects.add_project'):
        return project_initiation(request)
    else:
        return project_plan(request)


def ProgramContentDetails(request):
    program = request.session.get('projectid', default=None)
    if program is not None:
        if len(Project.objects.filter(pk=program)) > 0:
            program = Project.objects.filter(pk=program)[0]
    return program


def get_clients(request):
    """
        Returns the customer contact for a given customer.
    """
    customer_id = request.GET.get('customer', '')

    clients = UserProfile.objects.filter(
        business_unit=customer_id).order_by('user__first_name')
    client = []
    for each in clients:
        client.append({'name': str(each.user.first_name + ' ' + each.user.last_name),
                       'id': each.pk})
    json = simplejson.dumps(client)
    return HttpResponse(json, content_type='application/javascript')







def manage_domain(request, id=''):
    """
        Create/Edit the business unit from the project.
    """
    instance = None
    id = request.POST.get(
        'domainID',
        '') if request.POST.get(
        'domainID',
        '') != '' else id
    if id:
        instance = get_object_or_404(Domain, id=id)
    if request.method == 'POST':
        form = DomainForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            data = [{'id': instance.pk, 'resource': instance.__unicode__()}]
        else:
            data = [{'error': form.errors}]
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(data),
                                content_type='application/json')
    else:
        form = DomainForm(instance=instance)
    return render(request, 'domain.html', {'form': form, 'domainID': id})


def manage_project_type(request, id=''):
    """
        Create/Edit the project type from the project.
    """
    instance = None
    id = request.POST.get(
        'projectTypeID',
        '') if request.POST.get(
        'projectTypeID',
        '') != '' else id
    if id:
        instance = get_object_or_404(ProjectType, id=id)
    if request.method == 'POST':
        form = ProjectTypeForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            data = [{'id': instance.pk, 'resource': instance.__unicode__()}]
        else:
            data = [{'error': form.errors}]
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(data),
                                content_type='application/json')
    else:
        form = ProjectTypeForm(instance=instance)
    return render(request, 'project_type.html',
                  {'form': form, 'projectTypeID': id})


def manage_business_unit(request, id=''):
    """
        Create/Edit business unit from the project.
    """
    instance = None
    id = request.POST.get(
        'businessunitID',
        '') if request.POST.get(
        'businessunitID',
        '') != '' else id
    if id:
        instance = get_object_or_404(ProjectType, id=id)
    if request.method == 'POST':
        form = BusinessUnitForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            data = [{'id': instance.pk, 'resource': instance.__unicode__()}]
        else:
            data = [{'error': form.errors}]
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(data),
                                content_type='application/json')
    else:
        form = BusinessUnitForm(instance=instance)
    return render(request, 'business_unit.html',
                  {'form': form, 'businessunitID': id})


def manage_project_group(request, id=None):
    """
        Create/Edit project group.
    """
    instance = None
    id = request.POST.get('project_group_id',
                          None) if request.method == 'POST' else id
    if id:
        instance = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        form = ProjectGroupForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            data = [{'id': instance.pk, 'name': instance.__unicode__()}]
        else:
            data = [{'error': form.errors}]
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(data),
                                content_type='application/json')
    else:
        form = ProjectGroupForm(instance=instance)
    return render(request, 'project_group.html',
                  {'form': form, 'project_group_id': id})


@login_required
@permission_required('users.add_userprofile')
def manage_project_initiation_request(request):
    """
        Create/Edit project Initiation request.
    """

    project = None
    user = request.user.id
    is_approved = ''
    ex_appr = ''
    is_rejected = ''
    msg = ''
    email_message = ''
    email_to_list = []
    email_request_list = []
    schedules = addressClient = None
    project_billing_form = None
    specific_dates_form = None
    time_based_form = None
    milestone_form = None
    FixedPriceForm = None
    TimeAndManagementForm = None
    SupportForm = None


    id = request.GET.get('id', None)
    user = ProjectInitiationRequestForm(user=request.user)
    project_category = ''

    MilestoneFormSet = init_milestone_formset(
        ("planned_days", "milestone", "from_date", "percentage"), True, extra_form(
            project, BILLING_CATEGORY['Milestone']))

    TimeBasedFormSet = init_milestone_formset(("from_date", "to_date", "category"), True, extra_form(project,
                                                                                           BILLING_CATEGORY['Time-Based']), max_num=TIME_BASED_MAX_FORM)
    SpecificDatesFormSet = init_milestone_formset(("from_date", "to_date"),
                                                  True, extra_form(project, BILLING_CATEGORY['Specific-Dates']))


    if id:
        project = get_object_or_404(Project, id=id)
        is_approved = project.is_approved
        schedules = project.schedules
        projectOwner = project.customer
        address_client = BusinessUnit.objects.filter(type__name='Customer')
        for each in address_client:
            if str(projectOwner) == each.name:
                addressClient = each.address

    MilestoneFormSet = init_milestone_formset(
        ("planned_days", "milestone", "from_date", "percentage"), True, extra_form(
            project, BILLING_CATEGORY['Milestone']))

    TimeBasedFormSet = init_milestone_formset(("from_date", "to_date", "category"), True, extra_form(project,
                                                                                           BILLING_CATEGORY['Time-Based']), max_num=TIME_BASED_MAX_FORM)
    SpecificDatesFormSet = init_milestone_formset(("from_date", "to_date"),
                                                  True, extra_form(project, BILLING_CATEGORY['Specific-Dates']))


    if request.method == 'POST':
        request_form = ProjectInitiationRequestForm(request.POST,instance=project, user=request.user)
        schedules_form = ProjectSchedulesRequestForm(request.POST,instance=schedules)
        project_billing_form = ProjectBillingDetailForm(request.POST)

        if request.user.has_perm('projects.add_project'):
            if id:

                milestone_form = MilestoneFormSet(request.POST, queryset=ProjectBillingDetails.objects.none(), prefix='milestone')
                
                time_based_form = TimeBasedFormSet(request.POST, queryset=ProjectBillingDetails.objects.none(), prefix='timebased')
                specific_dates_form = SpecificDatesFormSet(request.POST, queryset=ProjectBillingDetails.objects.none(),
                    prefix='specificdates')

                # import pdb;pdb.set_trace()
                if str(is_approved) == 'False' and str(ex_appr)=='':
                    billtype = request.POST['billed_type']
                    list_data=[]
                    if billtype == "FP":
                        for each in milestone_form:
                            planned_days = int(each['planned_days'].data) if each['planned_days'].data!='' else ''
                            percentage = int(each['percentage'].data) if each['percentage'].data!='' else ''

                            list_data.append({
                            'project_id': int(request.POST['project_no']),
                            'billing_category':request.POST['billed_type'],
                            'planned_days': planned_days,
                            'milestone': each['milestone'].data,
                            'from_date': datetime.datetime.strptime(each['from_date'].data, '%m-%d-%Y').strftime('%Y-%m-%d'),
                            'percentage': percentage
                            })

                        for each in list_data:
                            project_billing = ProjectBillingDetails.objects.create(project_id = each['project_id'],
                                                billing_category = each['billing_category'],
                                                planned_days = each['planned_days'],
                                                milestone = each['milestone'],
                                                from_date =each['from_date'],
                                                percentage = each['percentage'])                    
                            print project_billing

                    elif billtype == "TM":
                        for each in time_based_form:
                            list_data.append({
                            'project_id': int(request.POST['project_no']),
                            'billing_category':request.POST['billed_type'],
                            'from_date': datetime.datetime.strptime(each['from_date'].data, '%m-%d-%Y').strftime('%Y-%m-%d'),
                            'to_date': datetime.datetime.strptime(each['to_date'].data, '%m-%d-%Y').strftime('%Y-%m-%d'),
                            'category':each['category'].data,
                            })
                        for each in list_data:
                            project_billing = ProjectBillingDetails.objects.create(project_id = each['project_id'],
                                                billing_category = each['billing_category'],
                                                from_date =each['from_date'],
                                                to_date =each['to_date'],
                                                category = each['category'])                    
                            print project_billing

                    elif billtype == "SP":
                        for each in specific_dates_form:
                            list_data.append({
                            'project_id': int(request.POST['project_no']),
                            'billing_category':request.POST['billed_type'],
                            'from_date': datetime.datetime.strptime(each['from_date'].data, '%m-%d-%Y').strftime('%Y-%m-%d'),
                            'to_date': datetime.datetime.strptime(each['to_date'].data, '%m-%d-%Y').strftime('%Y-%m-%d'),
                            })
                        for each in list_data:
                            project_billing = ProjectBillingDetails.objects.create(project_id = each['project_id'],
                                                billing_category = each['billing_category'],
                                                from_date =each['from_date'],
                                                to_date =each['to_date'])                    
                            print project_billing
                    else:
                        print "END"



                if validate([milestone_form, time_based_form,
                             specific_dates_form]):

                    save_milestone_formset(milestone_form, project,
                                           InvoiceTerms.objects.get(name='Milestone'))
                    save_milestone_formset(time_based_form, project)
                    save_milestone_formset(specific_dates_form, project,
                                           InvoiceTerms.objects.get(name='Specific-Date'))

        # import pdb;pdb.set_trace()
        if request_form.is_valid() and schedules_form.is_valid():
            
            schedules = schedules_form.save()
            ex_appr = request.POST.get('ex_appr', 0)
            is_approved = request.POST.get('isapproved', 0)
            is_rejected = request.POST.get('isrejected', 0)
            pjtid = request_form.save(
                schedules=schedules,
                is_approved=is_approved,
                is_rejected=is_rejected,
                ex_approval=ex_appr)


            print "START APPROVE"
            if request.user.has_perm(
                    'projects.add_project') and id and is_approved != "":
                    print "Approve"

                    if str(is_approved) == '1':                                                                     #is approved
                        email_message = "Project " + \
                            str(request_form.cleaned_data['name']
                                ) + ' was approved by '
                        email_message += str(
                            request_form.cleaned_data['approved_by'])
                        if str(ex_appr) == '1':
                            email_message += ' upon customer approval'
                        else:
                            email_message += ' pending customer approval'
                        email_message += ' on ' + \
                            str(schedules_form.cleaned_data['approved_date'])
                        
                    else:
                        if str(is_rejected) == '1':
                            user = User.objects.get(username=request_form.cleaned_data['requested_by'])
                            recipients = user.email
                            email_to_list.append(recipients)
                            email_message = "Project " + str(
                                request_form.cleaned_data['name']) + ' was Rejected by ' + str(
                                request_form.cleaned_data['approved_by']) + ' on ' + str(
                                schedules_form.cleaned_data['approved_date']) + '</br></br>Rejection Reason :' + str(
                                request_form.cleaned_data['rejection_reason'])
                            alert_generate(
                                request,
                                'Project',
                                'alertdataconfig17',
                                id,
                                email_to_list)

                    print "TAKE VALUE"
                    user = User.objects.get(
                        username=request_form.cleaned_data['requested_by'])
                    recipients = user.email
                    email_to_list.append(recipients)

                    project_name = str(request.POST.get('name'))
                    user_name = str(
                        request_form.cleaned_data['requested_by'].username)
                    

                    bus_unit = str(request_form.cleaned_data['business_unit'].name)
                    project_category = str(request.POST.get('approval_type'))
                    project_type = str(request_form.cleaned_data['project_type'])

                    request_date = str(
                        schedules_form.cleaned_data['initiation_request_date'])
                    expected_start_date = str(
                        schedules_form.cleaned_data['expected_start_date'])
                    expected_end_date = str(
                        schedules_form.cleaned_data['expected_end_date'])
                    estimated_efforts = str(
                        request_form.cleaned_data['planned_effort'])
                    objective = str(request_form.cleaned_data['objective'])
                    rejected_reason = str(
                        request_form.cleaned_data['rejection_reason'])

                    email_message += "<table width='50%'><tr><td></br>Requested by</td><td>:</td><td>" + \
                        user_name + "</td></tr><tr><td></br>Requested on</td><td>:</td>"
                    email_message += "<td>" + request_date + \
                        "</td></tr><tr><td></br>Business Unit</td><td>:</td><td>"
                    email_message += bus_unit + "</td></tr><tr><td></br>Project Name</td><td>:</td><td>" + \
                        project_name + "</td></tr>"
                    email_message += "<tr><td></br>Project Category</td><td>:</td><td>" + project_category + \
                        "</td></tr><tr><td></br>Project Type</td><td>:</td><td>" + project_type + "</td></tr>"
                    email_message += "<tr><td></br>Expected Start Date</td><td>:</td><td>" + \
                        expected_start_date + "</td></tr>""<tr><td></br>Expected End Date</td><td>:</td>"
                    email_message += "<td>" + expected_end_date + \
                        "</td></tr><tr><td></br>Estimated Efforts(man-days)</td><td>:</td><td>" + \
                        estimated_efforts + "</td>"
                    email_message += "</tr><tr><td></br>Objectives</td><td>:</td><td>" + \
                        objective + "</td></tr></table></body></html>"
                    email_subject = 'Project Approval Status'

                    try:
                        if rejected_reason == '' and is_rejected != 1:
                            if str(ex_appr) == '1':
                                alert_generate(
                                    request, 'Project', 'alertdataconfig43', id, email_to_list)
                            else:
                                alert_generate(
                                    request, 'Project', 'alertdataconfig44', id, email_to_list)

                            if str(is_approved)=='1':
                                if project_category == 'internal':
                                    msg = 'project_Approve'
                                    budget_alert_mail(
                                        request, request.GET.get('id', None))
                                else:
                                    if str(ex_appr) == '1':
                                        msg = 'ext_project_Approve'
                                        budget_alert_mail(
                                            request, request.GET.get('id', None))
                                    else:
                                        msg = 'int_project_Approve'
                        else:
                            msg = 'project_Reject'
                        
                    except Exception:
                        errMessage = 'Email Sending failed \n %s' % (Exception)


        """Create project initiation request and mail content"""
        if (id is None) or (not request.user.has_perm('projects.add_project')
                            and request.user.has_perm('projects.change_project') and id):
            print "CREATE"

            email_subject = 'Project initiation request'

            if request_form.cleaned_data['project_type'].name == 'Others':
                project_type = str(
                    request_form.cleaned_data['other_project_type']) + '\r\n'
            else:
                project_type = str(
                    request_form.cleaned_data['project_type']) + '\r\n'

            # import pdb;pdb.set_trace()
            user = User.objects.get(                                                        #get name and email to approved by
                username=request_form.cleaned_data['approved_by'])

            recipients = user.email
            email_to_list.append(recipients)                                                #email_to_list

            user = User.objects.get(
                username=request_form.cleaned_data['requested_by'])
            recipients = user.email
            email_request_list.append(recipients)                                           #email_request_list                                 

            approved_by = str(                                                              #get approved by name
                request_form.cleaned_data['approved_by'].username)

            project_name = str(request.POST.get('name'))
            user_name = str(request.user.username)


            bus_unit = str(request_form.cleaned_data['business_unit'].name)
            project_category = str(request.POST.get('approval_type'))
            project_type = project_type
            expected_start_date = str(
                schedules_form.cleaned_data['expected_start_date'])
            expected_end_date = str(
                schedules_form.cleaned_data['expected_end_date'])
            # import pdb;pdb.set_trace()
            request_date = str(
                schedules_form.cleaned_data['initiation_request_date'])
            estimated_efforts = str(
                request_form.cleaned_data['planned_effort'])
            objective = str(request_form.cleaned_data['objective'])

            mail_content = " <html lang='en'><p><b>Dear " + approved_by + "<br/>&nbsp;&nbsp;&nbsp;Project " + \
                project_name + " has been initiated by " + \
                user_name + " on " + request_date + "</b></p>"
            mail_content += "<table width='50%'><tr><td>Requested by</td><td>:</td><td>" + \
                user_name + "</td></tr><tr><td>Requested on</td><td>:</td>"
            mail_content += "<td>" + request_date + \
                "</td></tr><tr><td>Business Unit</td><td>:</td><td>"
            mail_content += bus_unit + "</td></tr><tr><td>Project Name</td><td>:</td><td>" + \
                project_name + "</td></tr>"
            mail_content += "<td>Project Category</td><td>:</td><td>" + project_category + \
                "</td></tr><tr><td>Project Type</td><td>:</td><td>" + project_type + "</td></tr>"
            mail_content += "<tr><td>Expected Start Date</td><td>:</td><td>" + \
                expected_start_date + "</td><tr><td>Expected End Date</td><td>:</td>"
            mail_content += "<td>" + expected_end_date + \
                "</td></tr><tr><td>Estimated Efforts(man-days)</td><td>:</td><td>" + \
                estimated_efforts + "</td>"
            mail_content += "</tr><tr><td>Objectives</td><td>:</td><td>" + \
                objective + "</td></tr></table></body></html>"

            try:
                alert_generate(
                    request,
                    'Project',
                    'alertdataconfig41',
                    pjtid.id,
                    email_to_list)
                alert_generate(
                    request,
                    'Project',
                    'alertdataconfig42',
                    pjtid.id,
                    email_request_list)
                msg = 'project_initiated'
            except Exception:
                errMessage = 'Email Sending failed \n %s' % (Exception)
        

    else:
        request_form = ProjectInitiationRequestForm(instance=project,
                                                    user=request.user)
        schedules_form = ProjectSchedulesRequestForm(instance=schedules)

        milestone_form = MilestoneFormSet(queryset=ProjectBillingDetails.objects.none(), prefix='milestone')
        time_based_form = TimeBasedFormSet(queryset=ProjectBillingDetails.objects.none(), prefix='timebased')
        specific_dates_form = SpecificDatesFormSet(queryset=ProjectBillingDetails.objects.none(),prefix='specificdates')
    

    print '*********', is_approved
    return render(request, 'project_initiation_request.html',
                  {'request_form': request_form, 'schedules_form': schedules_form, 'msg': actionMsg[msg], 'is_approved': is_approved,
                    'user': request.user, 'approval_type': project_category,
                   'project': project, 'schedules': schedules,'addressClient': addressClient, 'milestone_form':milestone_form, 'time_based_form':time_based_form, 'specific_dates_form':specific_dates_form})




def ext_appr_cron(request):
    """
    Alert mail for External approval of a project though python cron job
    """
    alert_on = settings.ALERT_ON
    alert_reminder = settings.ALERT_REMINDER
    projects = Project.objects.filter(
        ex_approval=False,
        is_approved=True,
        is_active=True).exclude(
        cancel=True)
    projects = projects.filter(
        schedules__approved_date__lt=datetime.datetime.now().date() -
        relativedelta(
            days=alert_on))
    flag = False
    for pjt in projects:
        alerttime_details = ProjectAlertTime.objects.filter(record_id=pjt.id)
        if len(alerttime_details) > 0:
            last_alert_with_days = alerttime_details[0].raised_on + \
                relativedelta(days=alert_reminder)
            if datetime.datetime.now().date() >= last_alert_with_days:
                alerttime_details.update(
                    raised_on=datetime.datetime.now().date())
                flag = True
        else:
            alert_time = ProjectAlertTime(record_id=pjt.id,
                                          raised_on=datetime.datetime.now().date())
            alert_time.save()
            flag = True
        if flag:
            user = User.objects.get(id=pjt.approved_by.id)
            recipients = user.email
            approved_by = str(User.objects.get(id=pjt.approved_by.id).username)
            project_name = str(pjt.name)
            user_name = str(User.objects.get(id=pjt.requested_by.id).username)

            request_date = str(pjt.schedules.initiation_request_date)


            delay_days = str(
                (datetime.datetime.now().date() -
                 pjt.schedules.approved_date).days)
            print 'delay_days', delay_days
            email_subject = "Need customer approval for " + project_name + " project"
            mail_content = " <html lang='en'><p>Dear " + \
                approved_by + "<br/><br/>&nbsp;&nbsp;&nbsp;The project "
            mail_content += project_name + \
                " has not yet got customer approval and is active for past " + delay_days + " days."
            mail_content += "</p><br/>Thanks.</html>"

            try:
                Email().send_email(
                    email_subject,
                    mail_content,
                    [recipients],
                    CONTENT_TYPE)
                msg = ' Alert mail for project approval'
            except Exception:
                errMessage = 'Email Sending failed \n %s' % (Exception)


def project_request_list(request, page=1, msg=''):
    """
        list the project for the users.
    """

    query = Q(is_active=True) & (Q(ex_approval=0) | Q(is_approved=0) | Q(is_rejected=0)) 
    searchtext = request.GET.get('search', '')

    if searchtext:
        print "Hi...", searchtext
        if(searchtext == "Waiting for approval"):
            for term in searchtext.split():
                q = Q(name__icontains=term) | Q(is_approved=0)
            query = query & q
        elif(searchtext == "Waiting for customer approval"):
            for term in searchtext.split():
                q = Q(name__icontains=term) | (Q(is_approved=1) & Q(ex_approval=0))
            query = query & q

    if request.user.has_perm('projects.add_project'):
        project_set = Project.objects.filter(Q(apex_body_owner=request.user) |
                                             Q(owner=request.user) |
                                             Q(team=request.user) | Q(approved_by=request.user)).distinct().exclude(cancel=True)
    else:
        project_set = Project.objects.filter(Q(requested_by=request.user))

    callable = ProjectListView.as_view(
        queryset=project_set.filter(query).exclude(
            requested_by=None).order_by('-project_no'),
        template_name="Project_initiation_request_list.html",
        context_object_name="project_request_list",
        extra_context={'msg': actionMsg[msg], },
        paginate_by=20
    )
    return callable(request)


def print_project_details(request, id=None):

    form = Project.objects.get(id=id)
    it_admin_user = User.objects.filter(id=request.user.id,
                                        groups__name__icontains='IT Admin', is_active=True)
    return render(request, 'Approved_project_print.html',
                  {'project': form, 'it_admin_user': it_admin_user},
                  )

def print_project_billind_details(request, id=None):

    form = Project.objects.get(id=id)
    project = Project.objects.get(id=id)
    project_no = project.project_no
    billed_type = project.billed_type
    datas = ProjectBillingDetails.objects.filter(project_id=project_no, billing_category=billed_type)

    data_list=[]
    if len(datas)!=0:
        for each in datas:
            if each.billing_category == 'FP':
                data_list.append({
                    'project_name' : project,
                    'billing_category' : each.billing_category,
                    'planned_days' : each.planned_days,
                    'milestone' : each.milestone,
                    'from_date' : each.from_date,
                    'percentage' : each.percentage,
                })
            elif each.billing_category == "TM":
                    data_list.append({
                    'project_name' : project,
                    'billing_category':each.billing_category,
                    'from_date': each.from_date,
                    'to_date': each.to_date,
                    'category':each.category,
                    })
            elif each.billing_category == "SP":
                    data_list.append({
                    'project_name' : project,
                    'billing_category':each.billing_category,
                    'from_date': each.from_date,
                    'to_date': each.to_date,
                    })


    it_admin_user = User.objects.filter(id=request.user.id,
                                        groups__name__icontains='IT Admin', is_active=True)
    return render(request, 'Approved_project_billing_details.html',
                  {'project':project, 'billed_type':billed_type, 'datas_set':datas,}, 
                  )

@login_required
def project_delete(request):
    if request.method == 'POST':
        project_ids = request.POST.getlist('project_pk')
        queryset = Project.objects.filter(code__in=project_ids)
        queryset.delete()
        DELETE = "Project has been deleted"
        messages.success(request,(DELETE))
    # return render(request, '/projects/requestlist/')
    return HttpResponseRedirect("/projects/requestlist/")





















