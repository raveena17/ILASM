# Create your views here.
import datetime
import os

from django.db.models import Q
# from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count
from django.template import RequestContext, Context
from django.template.loader import get_template
from dateutil.relativedelta import relativedelta
from django.conf import settings

from project_management.reimbursement.models import *
from project_management.users.models import UserProfile
from project_management.alert.views import alert_generate
from project_management.alert.models import AlertDataConfiguration


DISPLAY_MSG = {
    'RS1': 'Reimbursement saved successfully',
    'RS2': 'Reimbursement submitted successfully',
    'RS3': 'Reimbursement approved successfully',
    'RS4': 'Reimbursement approved successfully',
    'RS5': 'Reimbursement rejected successfully',
}


@login_required
def list(request):
    '''
     Reimbursement List.
    '''
    corporate_admin = User.objects.filter(id=request.user.id,
                                          groups__name__icontains='Corporate Admin', is_active=True)
    if len(corporate_admin) > 0:
        reimbursement = Reimbursement.objects.filter(
            status__in=['RS2', 'RS3', 'RS4']).order_by('-modified_on')
    else:
        reimbursement = Reimbursement.objects.all().order_by('-modified_on')

    reimbursement = reimbursement.filter(Q(requested_by=request.user, status__in=['RS1', 'RS2', 'RS3', 'RS4', 'RS5']) |
                                         Q(approved_by=request.user, status__in=['RS2', 'RS3', 'RS4']) | Q(final_approver=request.user))
    searchtext = request.GET.get('search', '')
    if searchtext:
        for term in searchtext.split():
            query = Q(expenditure__expenditure_name__icontains=term)
        reimbursement = reimbursement.filter(query)
    return render(request, 'reimbursement_list.html', {'reimbursement':
                                                       reimbursement},)


@login_required
def create(request):
    '''
    Create Reimbursement
    '''
    reimbus_status = 'open'
    expenditure = ''
    final_approver_data = ''
    requested_to_data = ''
    reimbursement = ''
    requested_data = ''
    expend_count = ''
    requested_by = request.user
    final_approver = User.objects.filter(
        groups__name__icontains='Corporate Admin', is_active=True)
    requested_to = UserProfile.objects.filter(user__id=request.user.id)[0]
    requested_to = requested_to.reporting_senior
    id = request.GET.get('id')
    if id is not None:
        reimbursement_id = request.GET.get('id')
        reimbursement = Reimbursement.objects.filter(id=reimbursement_id)[0]
        expenditure = Expenditure_Reimburs.objects.filter(
            reimbursement__id=reimbursement_id)
        expend_count = expenditure.count()
        requested_data = reimbursement.requested_by
        final_approver_data = reimbursement.final_approver
        requested_to = reimbursement.approved_by
        requested_by = reimbursement.requested_by
        reimbus_status = reimbursement.status.id

    pagedata = {
        'final_approver': final_approver,
        'requested_to': requested_to,
        'requested_by': requested_by,
        'reimbus_status': reimbus_status,
        'expenditure': expenditure,
        'reimbursement': reimbursement,
        'final_approver_data': final_approver_data,
        'requested_to_data': requested_to_data,
        'expend_count': expend_count,
    }
    print reimbus_status
    return render(request, 'reimbursement.html', pagedata,
                  )


@login_required
def save(request):
    '''
    Save the Reimbursement Form
    '''
    to_ids = []
    req_data = request.POST
    req_usr = User.objects.filter(username=req_data.get('requested_by'))[0]
    req_to_usr = User.objects.filter(username=req_data.get('request_to'))[0]
    save_dict = ({
        'id': req_data.get('reimbus_id', ''),
        'name': req_data.get('reimburs_name'),
        'requested_by_id': req_usr.pk,
        'approved_by_id': req_to_usr.pk,
        'final_approver_id': req_data.get('final_approver'),
        #                'requested_date':datetime.datetime.strptime(\
        # req_data.get('reimbursement_date'), '%m-%d-%Y'),
        'applied_date': datetime.datetime.strptime(\
            req_data.get('applied_date'), '%m-%d-%Y'),
        'status_id': req_data.get('reimbus_status'),
        'is_int_approved': 1 if req_data.get('reimbus_status') == 'RS3' or \
        req_data.get('reimbus_status') == 'RS4' else 0,
        'is_ext_approved': 1 if req_data.get('reimbus_status') == 'RS4' else 0,
        'total_expenditure': req_data.get('total_exp')\
        if req_data.get('total_exp', '') != '' else 0,
        'rejection_reason': req_data.get('reject_reason')\
        if req_data.get('reimbus_status') == 'RS5' else '',
    })
    reimbursement = Reimbursement(**save_dict)
    reimbursement.save()
    '''
    Save Expenditure data
    '''
    total_amt = 0
    expenditure_len = req_data.get('expenditure_len')
    delete_expenditure = req_data.get("delete_expenditure")
    delete_expenditure_ids = delete_expenditure.split(',')
    delete_expenditure_details = \
        Expenditure_Reimburs.objects.filter(id__in=delete_expenditure_ids)
    delete_expenditure_details.delete()
    if expenditure_len > 0:
        for row in range(1, int(expenditure_len)):
            expend_name = req_data.get('expenditure' + str(row))
            expend_amount = req_data.get('exp_amount' + str(row))
            if expend_name != ' ' and expend_amount != ' ':
                exp_dict = ({
                    'id': req_data.get('expenditure_id' + str(row), ''),
                            'reimbursement_id': reimbursement.id,
                            'expenditure_name': req_data.get('expenditure' + str(row)),
                            'amount': req_data.get('exp_amount' + str(row)),

                            })
                total_amt += float(req_data.get('exp_amount' + str(row)))
                Expenditure_Reimburs(**exp_dict).save()
    reimbursement.total_expenditure = "%.2f" % total_amt
    reimbursement.save()
    msg = req_data.get('reimbus_status')
    final_approver = User.objects.filter(id=req_data.get('final_approver'))[0]
    to_ids.append(req_usr.email)
    to_ids.append(req_to_usr.email)
    to_ids.append(final_approver.email)
    if msg == "RS2":
        alert_generate(request, 'Reimbursement', 'alertdataconfig18',
                       reimbursement.id, to_ids)
    if msg == "RS3":
        alert_generate(request, 'Reimbursement', 'alertdataconfig19',
                       reimbursement.id, to_ids)
    if msg == "RS4":
        alert_generate(request, 'Reimbursement', 'alertdataconfig20',
                       reimbursement.id, to_ids)
    if msg == "RS5":
        alert_generate(request, 'Reimbursement', 'alertdataconfig21',
                       reimbursement.id, to_ids)
    return HttpResponseRedirect("/reimbursement/create/?id=" +
                                str(reimbursement.id) + '&display_msg=' +
                                DISPLAY_MSG[msg])
