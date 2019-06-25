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

from project_management.travel.models import *
from project_management.users.models import UserProfile
from project_management.business_unit.models import BusinessUnit
from project_management.alert.views import alert_generate
from project_management.alert.models import AlertDataConfiguration


DISPLAY_MSG = {
    'RS1': 'Travel request saved successfully',
    'RS2': 'Travel request submitted successfully',
    'RS3': 'Travel request approved successfully',
    'RS4': 'Travel request approved successfully',
    'RS5': 'Travel request rejected successfully',
}


@login_required
def list(request):
    '''
     Reimbursement List.
    '''
    corporate_admin = User.objects.filter(id=request.user.id,
                                          groups__name__icontains='Corporate Admin', is_active=True)
    if len(corporate_admin) > 0:
        travel = Travel.objects.filter(
            status__in=[
                'RS2',
                'RS3',
                'RS4']).order_by('-modified_on')
    else:
        travel = Travel.objects.all().order_by('-modified_on')

    travel = travel.filter(Q(requested_by=request.user, status__in=['RS1', 'RS2',
                                                                    'RS3', 'RS4', 'RS5']) |
                           Q(approved_by=request.user, status__in=['RS2', 'RS3', 'RS4']) | Q(final_approver=request.user))
    searchtext = request.GET.get('search', '')
    #import pdb;pdb.set_trace()
    if searchtext:
        for term in searchtext.split():
            query = Q(travel__travel_name__icontains=term)
        travel = travel.filter(query)
    return render(request, 'travel_request_list.html', {'travel':
                                                        travel},)


@login_required
def create(request):
    '''
    Create Travel Request
    '''
    travel_status = 'open'
    expenditure = ''
    final_approver_data = ''
    requested_to_data = ''
    travel = ''
    requested_data = ''
    expend_count = ''
    requested_by = request.user
    final_approver = User.objects.filter(
        groups__name__icontains='Corporate Admin', is_active=True)
    claim_amount = ClaimAmount.objects.all()
    requested_to = UserProfile.objects.filter(user__id=request.user.id)[0]
    requested_to = requested_to.reporting_senior
    id = request.GET.get('id')
    if id is not None:
        travel_id = request.GET.get('id')
        travel = Travel.objects.filter(id=travel_id)[0]
        expenditure = Expenditure.objects.filter(travel__id=travel_id)
        expend_count = expenditure.count()
        requested_data = travel.requested_by
        final_approver_data = travel.final_approver
        requested_to = travel.approved_by
        requested_by = travel.requested_by
        travel_status = travel.status.id

    pagedata = {
        'final_approver': final_approver,
        'requested_to': requested_to,
        'requested_by': requested_by,
        'travel_status': travel_status,
        'expenditure': expenditure,
        'travel': travel,
        'final_approver_data': final_approver_data,
        'requested_to_data': requested_to_data,
        'expend_count': expend_count,
        'claim_amount': claim_amount,
    }
    return render(request, 'travel_request.html', pagedata,
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
        'id': req_data.get('travel_id', ''),
        'name': req_data.get('travel_name'),
        'requested_by_id': req_usr.pk,
        'approved_by_id': req_to_usr.pk,
        'final_approver_id': req_data.get('final_approver'),
        'claim_to_date': datetime.datetime.strptime(
            req_data.get('claim_to_date'), '%m-%d-%Y'),
        'claim_from_date': datetime.datetime.strptime(
            req_data.get('claim_from_date'), '%m-%d-%Y'),
        'vehicle': req_data.get('vehicle'),
        'applied_date': datetime.datetime.strptime(
            req_data.get('applied_date'), '%m-%d-%Y'),
        'status_id': req_data.get('travel_status'),
        'is_int_approved': 1 if req_data.get('travel_status') == 'RS3' or
        req_data.get('travel_status') == 'RS4' else 0,
        'is_ext_approved': 1 if req_data.get('travel_status') == 'RS4' else 0,
        'total_km': req_data.get('total_km')
        if req_data.get('total_km', '') != '' else 0,
        'total_rs': req_data.get('total_rs')
        if req_data.get('total_rs', '') != '' else 0,
        'rejection_reason': req_data.get('reject_reason')
        if req_data.get('travel_status') == 'RS5' else '',
    })
    travel = Travel(**save_dict)
    travel.save()
    '''
    Save Expenditure data
    '''
    total_km = 0
    expenditure_len = req_data.get('expenditure_len')
    delete_expenditure = req_data.get("delete_expenditure")
    delete_expenditure_ids = delete_expenditure.split(',')
    delete_expenditure_details = \
        Expenditure.objects.filter(id__in=delete_expenditure_ids)
    delete_expenditure_details.delete()
    if expenditure_len > 0:
        for row in range(1, int(expenditure_len)):
            expend_name = req_data.get('client_name' + str(row))
            expend_amount = req_data.get('destination' + str(row))
            if expend_name != ' ' and expend_amount != ' ':
                exp_dict = ({
                    'id': req_data.get('expenditure_id' + str(row), ''),
                            'travel_id': travel.id,
                            'expend_date': datetime.datetime.strptime(
                        req_data.get('expend_date' + str(row)), '%m-%d-%Y'),
                    'client_name': req_data.get('client_name' + str(row)),
                    'destination': req_data.get('destination' + str(row)),
                    'km': req_data.get('km' + str(row)),

                })
                total_km += int(req_data.get('km' + str(row)))
                Expenditure(**exp_dict).save()
    msg = req_data.get('travel_status')
    final_approver = User.objects.filter(id=req_data.get('final_approver'))[0]
    to_ids.append(req_usr.email)
    to_ids.append(req_to_usr.email)
    to_ids.append(final_approver.email)
    if msg == "RS2":
        alert_generate(request, 'Travel', 'alertdataconfig22',
                       travel.id, to_ids)
    if msg == "RS3":
        alert_generate(request, 'Travel', 'alertdataconfig23',
                       travel.id, to_ids)
    if msg == "RS4":
        alert_generate(request, 'Travel', 'alertdataconfig24',
                       travel.id, to_ids)
    if msg == "RS5":
        alert_generate(request, 'Travel', 'alertdataconfig25',
                       travel.id, to_ids)
    return HttpResponseRedirect("/travel/create/?id=" +
                                str(travel.id) + '&display_msg=' +
                                DISPLAY_MSG[msg])
