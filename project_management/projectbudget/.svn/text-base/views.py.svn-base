# Create your views here.
import datetime
import os

import cStringIO as StringIO
import ho.pisa as pisa
from django.db.models import Q
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count
from django.template import RequestContext, Context
from django.template.loader import get_template
from dateutil.relativedelta import relativedelta
from django.conf import settings

from project_management.projects.models import Project
from project_management.projectbudget.models import *
from project_management.users.models import UserProfile
from project_management.alert.views import alert_generate
from project_management.alert.models import AlertDataConfiguration

DISPLAY_MSG = {
                'RS1': 'Project budget saved successfully',
                'RS2': 'Project budget submitted successfully',
                'RS3': 'Project budget approved successfully',
                'RS4': 'Project budget approved successfully',
                'RS5': 'Project budget rejected successfully',
                }


@login_required
def list(request):
    '''
    Project Budget List.
    '''
    projects = ProjectBudget.objects.filter(project__is_active=1, \
        project__ex_approval=1, project__is_approved=1, status__in=['RS2', \
        'RS3']).order_by('-modified_on')
    projects = projects.filter(Q(business_head__id=request.user.id) | \
    Q(pjt_owner__id=request.user.id))
    searchtext = request.GET.get('search', '')
    if searchtext:
        for term in searchtext.split():
            query = Q(project__name__icontains=term)
        projects = projects.filter(query)
    return render_to_response('projectbudget_list.html', {'projects': \
        projects}, context_instance=RequestContext(request))


def tmp_list(request):
    '''
    Project Budget List.
    '''
    projectbudjets = ProjectBudget.objects.all().values('project')
    projects = Project.objects.all().exclude(id__in=projectbudjets)
    for each in projects:
        ProjectBudget(status_id='RS1', project=each, budget_updated=0, \
            version=1, modified_on=datetime.datetime.now(), \
            planned_start_date=each.schedules.planned_start_date, \
            org_end_date=each.schedules.planned_end_date, \
            revised_start_date=each.schedules.planned_start_date, \
            revised_end_date=each.schedules.planned_end_date).save()


@login_required
def create(request):
    '''
    Create Project budget
    '''
    tmp_list(request)
    pjt_id = request.GET.get('pjt_id', '')
    selected_version = request.GET.get('version', '')
    print 'selected_version', selected_version
    bud_version = ProjectBudget.objects.filter(project__id=pjt_id).aggregate(\
        Max('version')).get('version__max')
    if selected_version == '' or selected_version == None:
        selected_version = bud_version
    pjt_bud = ProjectBudget.objects.filter(project__id=pjt_id, \
        version=selected_version)[0]
    efforts = ProjectBudgetEfforts.objects.filter(project_budget=pjt_bud.id)
    bud_costs = ProjectBudgetCost.objects.filter(project_budget=pjt_bud.id)
    pjt_owners = User.objects.filter(\
            groups__name__icontains='Corporate Admin', is_active=True)
    business_head = User.objects.filter(\
            groups__name__icontains='Manager',is_active=True, \
            is_staff=False).exclude(id__in=pjt_owners.values('id'))
    phases = BudgetPhase.objects.filter(is_active=True)
    locations = BudgetLocation.objects.all()
    costs = BudgetCost.objects.filter(is_active=True)

    # Threshold Calculation
    prev_version = ProjectBudget.objects.filter(\
        project__id=pjt_bud.project.id, version=int(pjt_bud.version) - 1)

    threshold_effort = 0
    threshold_cost = 0
    deviation_duration = 0
    tot_duration = 0
    if pjt_bud.revised_end_date != None and \
            pjt_bud.planned_start_date != None:
        end_date = pjt_bud.revised_end_date - pjt_bud.planned_start_date
        tot_duration = end_date.days + 1
    if len(prev_version) > 0:
        dev_effort = 0
        dev_cost = 0
        if pjt_bud.total_effort and prev_version[0].total_effort:
            dev_effort = pjt_bud.total_effort - \
                float(prev_version[0].total_effort)
        if pjt_bud.total_cost and prev_version[0].total_cost:
            dev_cost = pjt_bud.total_cost - float(prev_version[0].total_cost)
        if prev_version[0].total_effort != None and \
            float(prev_version[0].total_effort) > 0:
            threshold_effort = \
                (float(dev_effort) / float(prev_version[0].total_effort)) * 100
        if prev_version[0].total_cost != None and prev_version[0].total_cost \
            > 0:
            threshold_cost = \
                (float(dev_cost) / float(prev_version[0].total_cost)) * 100
        if prev_version[0].revised_end_date != None and \
                prev_version[0].planned_start_date != None:
            start_date = prev_version[0].revised_end_date - \
                prev_version[0].planned_start_date
        if start_date.days != None and end_date.days != None:
            deviation_duration = (float(((end_date.days+1) - \
                (start_date.days+1))) / (start_date.days+1)) * 100

    #Give edit permission
    is_editable = 1
    edit_permission = ProjectBudget.objects.filter(project__id=pjt_id,\
            version=selected_version).filter(project__is_active=1, \
            project__ex_approval=1, project__is_approved=1).filter(\
            Q(project__requested_by__id=request.user.id) | \
            Q(business_head__id=request.user.id) | \
            Q(pjt_owner__id=request.user.id))
    if str(selected_version) != str(bud_version) or pjt_bud.project.is_active \
            == 0 or len(edit_permission) == 0:
        is_editable = 0
    print is_editable

    pagedata = {
                'pjt_bud': pjt_bud,
                'phases': phases,
                'locations': locations,
                'costs': costs,
                'efforts': efforts,
                'bud_costs': bud_costs,
                'business_head': business_head,
                'pjt_owners': pjt_owners,
                'threshold_effort': "%.2f" % threshold_effort,
                'threshold_cost': "%.2f" % threshold_cost,
                'version_range': range(1, int(bud_version) + 1),
                'is_editable': is_editable,
                'project': pjt_bud.project,
                'msg': request.GET.get('display_msg', ''),
                'tot_duration':tot_duration,
                'deviation_duration': "%.2f" % deviation_duration}
    return render_to_response('projectbudget.html', pagedata, \
        context_instance=RequestContext(request))


@login_required
def save(request):
    '''
    Save project Budget, Efforts  and Costs
    '''
    req_data = request.POST
    pjt_bud = ProjectBudget.objects.get(id=req_data.get('bud_id'))
    status = req_data.get('status')
    # Version Control
    if pjt_bud.status.id == 'RS4':
        bud_id = ''
        version = int(pjt_bud.version) + 1
    else:
        bud_id = req_data.get('bud_id')
        version = pjt_bud.version

    # Save Project Budject
    budget_dict = ({
                    'id': bud_id,
                    'project': pjt_bud.project,
                    'planned_start_date': datetime.datetime.strptime(\
                        req_data.get('planned_start_date'), '%m-%d-%Y'),
                    'org_end_date': datetime.datetime.strptime(\
                        req_data.get('org_end_date'), '%m-%d-%Y'),
                    'revised_start_date': datetime.datetime.strptime(\
                        req_data.get('revised_start_date'), '%m-%d-%Y'),
                    'revised_end_date': datetime.datetime.strptime(\
                        req_data.get('revised_end_date'), '%m-%d-%Y'),
                    'execution_mode': req_data.get('execution_mode'),
                    'remarks': req_data.get('remarks'),
                    'version': version,
                    'status_id': 'RS3' \
                        if status == 'RS4' and \
                        str(request.user.id) == str(req_data.get('bus_head')) \
                        else status,  # Maintain 1st and 2nd level approval
                    'budget_updated': 1 if pjt_bud.budget_updated == 0 and \
                        status == 'RS2'  else pjt_bud.budget_updated,
                    'business_head_id': req_data.get('bus_head'),
                    'pjt_owner_id': req_data.get('pjt_owner'),
                    'other1_description': req_data.get('other1_desc'),
                    'other2_description': req_data.get('other2_desc'),
                    })
    if status == 'RS5':
        budget_dict.update({'rejection_reason': req_data.get('rjt_reason', \
            '')})

    project_budget = ProjectBudget(**budget_dict)
    project_budget.save()

    # Save  Activity table
    tot_effort = 0
    activity_tbl_len = req_data.get('activity_len')
    delete_effort = req_data.get("delete_effort")
    delete_effort_ids = delete_effort.split(',')
    delete_effort_details = \
            ProjectBudgetEfforts.objects.filter(id__in=delete_effort_ids)
    delete_effort_details.delete()
    if activity_tbl_len != '' and int(activity_tbl_len) > 0:
        for row in range(1, int(activity_tbl_len)):
            if req_data.get('location' + str(row)) == '' or req_data.get( \
                    'location' + str(row)) == None:
                continue
            activity_dict = ({
                            'id': '' if bud_id == '' else req_data.get( \
                                'effort_id' + str(row)),
                            'project_budget': project_budget,
                            'activity_type': req_data.get('activity_type'),
                            'phase_id': req_data.get('phase' + str(row)),
                            'module': req_data.get('module' + str(row)),
                            'location_id': req_data.get('location' + str(row)),
                            'duration_days': req_data.get('duration_days' + \
                                str(row)) if req_data.get('pm_effort' + \
                                str(row), '0') != '' else '0',
                            'pm_effort': req_data.get('pm_effort' + \
                                str(row), '0') if req_data.get('pm_effort' + \
                                str(row), '0') != '' else '0',
                            'lead_effort': req_data.get('lead_effort' + \
                                str(row), '0') if req_data.get('lead_effort' \
                                + str(row), '0') != '' else '0',
                            'developpper_effort': req_data.get('dev_effort' + \
                                str(row), '0') if req_data.get('dev_effort' + \
                                str(row), '0') != '' else '0',
                            'tester_effort': req_data.get('test_effort' + \
                                str(row), '0') if req_data.get('test_effort' \
                                + str(row), '0') != '' else '0',
                            'other1': req_data.get('oth1_effort' + str(row), \
                                '0') if req_data.get('oth1_effort' + \
                                str(row), '0') != '' else '0',
                            'other2': req_data.get('oth2_effort' + str(row), \
                                '0') if req_data.get('oth2_effort' + \
                                str(row), '0') != '' else '0',
                            })
            if status == 'RS4' or req_data.get('effort_approved' + str(row), \
                    '0') == '1':
                activity_dict.update({'effort_approved': 1})
            else:
                activity_dict.update({'effort_approved': 0})
            efforts = ProjectBudgetEfforts(**activity_dict)
            efforts.save()
            tot_effort += float(efforts.pm_effort) + float(\
                efforts.lead_effort) + float(efforts.developpper_effort) + \
                float(efforts.tester_effort) + float(efforts.other1) + \
                float(efforts.other2)

    #Save Cost table
    tot_cost = 0
    cost_tbl_len = req_data.get('cost_len')
    delete_cost = req_data.get("delete_cost")
    delete_cost_ids = delete_cost.split(',')
    delete_cost_details = \
            ProjectBudgetCost.objects.filter(id__in=delete_cost_ids)
    delete_cost_details.delete()
    if cost_tbl_len != '' and int(cost_tbl_len) > 0:
        for row in range(1, int(cost_tbl_len)):
            if req_data.get('cost' + str(row)) == '' or req_data.get('cost' + \
                    str(row)) == None:
                continue
            cost_dict = ({
                            'id': '' if bud_id == '' else req_data.get(\
                                'cost_id' + str(row)),
                            'project_budget': project_budget,
                            'cost_type_id': req_data.get('cost_type' + \
                                str(row)),
                            'cost': req_data.get('cost' + str(row))})
            if status == 'RS4' or req_data.get('cost_approved' + str(row), \
                    '0') == '1':
                cost_dict.update({'cost_approved': 1})
            else:
                cost_dict.update({'cost_approved': 0})
            ProjectBudgetCost(**cost_dict).save()
            tot_cost += float(req_data.get('cost' + str(row)))
    project_budget.total_effort = "%.2f" % tot_effort
    project_budget.total_cost = "%.2f" % tot_cost
    project_budget.save()

    # Thrershold Calculation
    prev_version = ProjectBudget.objects.filter(project__id=project_budget.\
                project.id, version=int(project_budget.version) - 1)
    dev_effort = 0
    dev_cost = 0
    threshold_effort = 0
    threshold_cost = 0
    if len(prev_version) > 0:
        dev_effort = tot_effort - float(prev_version[0].total_effort)
        dev_cost = tot_cost - float(prev_version[0].total_cost)
        if prev_version[0].total_effort > 0:
            threshold_effort = (float(dev_effort) / \
                prev_version[0].total_effort) * 100
        if prev_version[0].total_cost > 0:
            threshold_cost = (float(dev_cost) / prev_version[0].total_cost) * \
                100

    # Threshold deviation mail sending
    thresh_msg = ''
    if threshold_effort > 25 or threshold_effort < -25:
        thresh_msg += 'Efforts deviation with previous version :' + \
            str("%.2f" % threshold_effort) + ' %'
    if threshold_cost > 25 or threshold_cost < -25:
        thresh_msg += '<BR>Cost deviation with previous version :' + \
            str("%.2f" % threshold_cost) + ' %'
    thresh_msg += '<BR><BR>Best Regards,<BR>Admin<BR>'\
            'This is a system generated alert. We request you not to '\
            'reply to this message.'
    if ((threshold_effort > 25) or (threshold_cost > 25)) and status == 'RS2':
        to_mailid = [str(project_budget.pjt_owner.email)]
        cc_ids = [str(project_budget.project.requested_by.email)]
        if str(project_budget.project.requested_by.id) != \
                str(project_budget.business_head.id):
            to_mailid.append(str(project_budget.business_head.email))
        alert_generate(request, 'ProjectBudget', 'alertdataconfig6', \
                project_budget.id, to_mailid, cc_ids, thresh_msg)

    # Workflow - Send Mail to requester, Bus head or pjt owner
    requster_id = str(project_budget.project.requested_by.email)
    bus_head_id = str(project_budget.business_head.email)
    pjt_own_id = str(project_budget.pjt_owner.email)
    if status == 'RS2':
        cc_ids = [requster_id]
        if str(project_budget.project.requested_by.id) == \
                str(project_budget.business_head.id):
            to_ids = [pjt_own_id]
            alert_generate(request, 'ProjectBudget', 'alertdataconfig2', \
                    project_budget.id, to_ids, cc_ids)
        else:
            to_ids = [bus_head_id]
            cc_ids.append(pjt_own_id)
            alert_generate(request, 'ProjectBudget', 'alertdataconfig1', \
                project_budget.id, to_ids, cc_ids)
    if status == 'RS4':
        to_ids = [requster_id]
        cc_ids = [pjt_own_id]
        if str(request.user.id) == str(project_budget.business_head.id):
            cc_ids.append(bus_head_id)
            alert_generate(request, 'ProjectBudget', 'alertdataconfig2', \
                project_budget.id, to_ids, cc_ids)
        elif str(request.user.id) == str(project_budget.pjt_owner.id):
            if str(project_budget.project.requested_by.id) != str(\
                    project_budget.business_head.id):
                cc_ids.append(bus_head_id)
            alert_generate(request, 'ProjectBudget', 'alertdataconfig4', \
                project_budget.id, to_ids, cc_ids)
    if status == 'RS5':        
        to_ids = [requster_id]
        cc_ids = [pjt_own_id]
        if str(request.user.id) == str(project_budget.business_head.id):
            cc_ids.append(bus_head_id)
            alert_generate(request, 'ProjectBudget', 'alertdataconfig5', \
                project_budget.id, to_ids, cc_ids)
        elif str(request.user.id) == str(project_budget.pjt_owner.id):
            if str(project_budget.project.requested_by.id) != str(\
                    project_budget.business_head.id):
                cc_ids.append(bus_head_id)
            alert_generate(request, 'ProjectBudget', 'alertdataconfig5', \
                project_budget.id, to_ids, cc_ids)
    return HttpResponseRedirect("/projectbudget/create/?pjt_id=" + \
            str(project_budget.project.id) + '&display_msg=' + \
                DISPLAY_MSG[status])


def budget_reminder_alertmail(request):
    '''
    Budget remainder mail to  project initiator
    '''
    today_date = datetime.datetime.now().date()
    bus_head_alertdays = AlertDataConfiguration.objects.get( \
            id='alertdataconfig8').days
    pjt_owner_alertdays = AlertDataConfiguration.objects.get( \
            id='alertdataconfig9').days
    budgets = ProjectBudget.objects.filter(project__is_active=True, \
            project__is_approved=True, project__ex_approval=True, \
            budget_updated=False)
    bus_head_budgets = budgets.filter( \
            project__schedules__approved_date__lte=today_date - \
            relativedelta(days=bus_head_alertdays))
    pjt_owner_budgets = budgets.filter(\
            project__schedules__approved_date__lte=today_date - \
            relativedelta(days=pjt_owner_alertdays)).values('id')
    for project_budget in bus_head_budgets:
        mail_ids = [str(project_budget.project.requested_by.email)]
        cc_mail_ids = []
        if project_budget.business_head and \
                project_budget.project.requested_by.id != project_budget.business_head.id:
            cc_mail_ids.append(str(project_budget.business_head.email))
        
        if project_budget.id in pjt_owner_budgets and project_budget.pjt_owner:
            cc_mail_ids.append([str(project_budget.pjt_owner.email)])
        alert_generate(request, 'ProjectBudget', 'alertdataconfig8', \
            project_budget.id, mail_ids, cc_mail_ids)

def budget_alert_mail(request, pjt_id):
    project = Project.objects.get(id=pjt_id)
    project_budget = ProjectBudget.objects.filter(project__id=pjt_id)
    if len(project_budget) == 0:
        project_budget = ProjectBudget(status_id='RS1', project=project, \
                budget_updated=0, version=1, \
                modified_on=datetime.datetime.now(), \
                planned_start_date=project.schedules.planned_start_date, \
                org_end_date=project.schedules.planned_end_date, \
                revised_start_date=project.schedules.planned_start_date, \
                revised_end_date=project.schedules.planned_end_date)
        project_budget.save()
    alert_generate(request, 'ProjectBudget', 'alertdataconfig7', \
        project_budget.id, [str(project_budget.project.requested_by.email)])


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, \
            ""))
    return path

def threshold(request, pjt_bud):
    # Threshold Calculation
    prev_version = ProjectBudget.objects.filter(\
        project__id=pjt_bud.project.id, version=int(pjt_bud.version) - 1)
    threshold_effort = 0
    threshold_cost = 0
    deviation_duration = 0
    tot_duration = 0
    end_date = None
    if pjt_bud.revised_end_date != None and \
            pjt_bud.planned_start_date != None:
        end_date = pjt_bud.revised_end_date - pjt_bud.planned_start_date
        tot_duration = end_date.days + 1
    if len(prev_version) > 0:
        dev_effort = 0
        dev_cost = 0
        if pjt_bud.total_effort and prev_version[0].total_effort:
            dev_effort = pjt_bud.total_effort - \
                float(prev_version[0].total_effort)
        if pjt_bud.total_cost and prev_version[0].total_cost:
            dev_cost = pjt_bud.total_cost - float(prev_version[0].total_cost)
        if prev_version[0].total_effort != None and \
            float(prev_version[0].total_effort) > 0:
            threshold_effort = \
                (float(dev_effort) / float(prev_version[0].total_effort)) * 100
        if prev_version[0].total_cost != None and prev_version[0].total_cost \
            > 0:
            threshold_cost = \
                (float(dev_cost) / float(prev_version[0].total_cost)) * 100
        if prev_version[0].revised_end_date != None and \
                prev_version[0].planned_start_date != None:
            start_date = prev_version[0].revised_end_date - \
                prev_version[0].planned_start_date        
        if start_date.days != None and end_date.days != None:
            deviation_duration = (float(((end_date.days+1) - \
                (start_date.days+1))) / (start_date.days+1)) * 100

#    import pdb;pdb.set_trace()
    threshold_effort = "%.2f" % threshold_effort
    threshold_cost = "%.2f" % threshold_cost
    deviation_duration = "%.2f" % deviation_duration        
    return threshold_effort, threshold_cost, deviation_duration, tot_duration

def export_budget(request):
    template = get_template('budget_pdf.html')
    pjt_id = request.GET.get('pjt_id')
    version = request.GET.get('version')
    projectbudget = ProjectBudget.objects.filter(project__id=pjt_id, \
            version=version)[0]
    projectbudgetcost = ProjectBudgetCost.objects.filter(\
            project_budget=projectbudget)
    projectbudgetefforts = ProjectBudgetEfforts.objects.filter(\
            project_budget=projectbudget)
    threshold_effort, threshold_cost, deviation_duration, tot_duration = threshold(request, projectbudget)
    pagedata = ({
                'projectbudget': projectbudget,
                'projectbudgetcost': projectbudgetcost,
                'projectbudgetefforts': projectbudgetefforts,
                'threshold_effort': threshold_effort, 
                'threshold_cost': threshold_cost, 
                'deviation_duration': deviation_duration,
                'tot_duration' : tot_duration ,
                'rejection_reason': '1' if str(projectbudget.status.id) == 'RS5' else '0',
                'activity_type': 'Phase' \
                    if projectbudgetefforts[0].activity_type == '1' else 'Module',
                })
    context = Context(pagedata)
    html = template.render(context)
    result = StringIO.StringIO()
    pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, \
            link_callback=fetch_resources)
    result.seek(0)
    filename = str(projectbudget.project.name) + '_version' + str(\
            projectbudget.version) + '.pdf'
    folder = 'budgetpdf'
    currentdir = settings.MEDIA_ROOT
    currentosdir = currentdir + '/' + folder
    currentdir = os.listdir(currentdir)
    check = 0
    for each in currentdir:
        if each == folder:
            check = 1
    if(check != 1):
        os.mkdir(currentosdir)
    fd = open('%s/%s' % (currentosdir, filename), 'wb')
    fd.write(result.getvalue())
    fd.close()
    response = HttpResponse(result.getvalue(), mimetype='application/pdf')
    filename = filename.replace(' ', '')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
