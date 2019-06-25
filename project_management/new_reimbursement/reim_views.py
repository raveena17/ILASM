from .forms import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from django.views.decorators.http import require_http_methods
from project_management.client_visit_report.models import ClientVisitReport
from django.http import JsonResponse
from project_management.new_reimbursement.models import ReimbursementStatus, BudgetType, ReimbursementType, Allowance, Reimbursement_new
import datetime
from django.contrib import messages
from ast import literal_eval

today = datetime.date.today()

@require_http_methods(["GET"])
def get_type(request):
    report = {}
    if request.GET['type'] == 'Travel':
        queryset = ClientVisitReport.objects.all().values('client_name__name', 'id', 'from_date')
        json_type = list(queryset)
    return JsonResponse(json_type, safe=False)

@require_http_methods(["GET"])
def get_report(request):
    if request.GET['name'] == 'travel':
        queryset = ClientVisitReport.objects.filter(id=int(request.GET['type'])).values('prepared_by','client_name__name', 'id', 'visit_location','from_date','to_date','is_approved', 'is_rejected')
        json_type = list(queryset)
    return JsonResponse(json_type, safe=False)

@require_http_methods(["GET"])
def get_user_roles(request):
    groups = request.user.groups.all().values('name')
    user_roles = []
    for index in range(0, (len(groups)-1)):
        role = groups[index].values()[0]
        user_roles.append(role)
    return user_roles

def get_reimbursement_budjet(request):
    queryset = BudgetType.objects.all().values('id', 'budget')
    budgets = list(queryset)
    return JsonResponse(budgets, safe=False)
    

def admin_reimbursement_list(request):
    # import pdb;pdb.set_trace()
    reimbursements = None
    page = request.GET.get('page', 1)
    status_filter = Filter()
    for role in get_user_roles(request):
        if role == 'Corporate Admin':
            if 'status' in request.GET:
                reimbursement = Reimbursement_new.objects.filter(status__status=request.GET['status']).order_by('-created_on')
            else:
                reimbursement = Reimbursement_new.objects.all().order_by('-created_on')
            reimbursements = paginate_reimbursement(reimbursement, page)
            return render(request, 'reimbursement_records.html',{'reimbursements': reimbursements, 'status_filter':status_filter})
@csrf_exempt
@login_required
def reimbursement_approver_list(request):
    # import pdb;pdb.set_trace()
    status_filter = Filter()
    page = request.GET.get('page', 1)

    if 'Corporate Admin' not in get_user_roles(request):
        if 'status' in request.GET:
            reimbursement = Reimbursement_new.objects.filter(status__status=request.GET['status'], approver=request.user)
        else:
            reimbursement = Reimbursement_new.objects.filter(approver=request.user).order_by('-created_on')
        requests = paginate_reimbursement(reimbursement, page)
        
        return render(request, 'reimbursement_approver_list.html',
                    {
                    'requests':requests, 'status_filter':status_filter})
    else:
        # import pdb;pdb.set_trace()

        # if request.GET['status']
        if 'status' in request.GET:
            reimbursements = Reimbursement_new.objects.filter(status__status=request.GET['status'], approver=request.user)
            approved_reimbursements = Reimbursement_new.objects.filter(status__status__in=[request.GET['status']]).exclude(approver=request.user).order_by('-created_on')

        else:
            reimbursements = Reimbursement_new.objects.filter(approver=request.user).order_by('-created_on')#.exclude(status__status__in=['Approved','Processed'])
            approved_reimbursements = Reimbursement_new.objects.filter(status__status__in=['Approved','Processed', 'Verified']).exclude(approver=request.user).order_by('-created_on')
        reimbursement = list(chain(reimbursements, approved_reimbursements))
        requests = paginate_reimbursement(reimbursement, page)
        return render(request, 'reimbursement_approver_list.html',
                    {
                    'requests':requests, 'status_filter':status_filter})

@csrf_exempt
@login_required
def reimbursement_list(request):
    # import pdb;pdb.set_trace()
    user_reimbursement = None
    status_filter = Filter()
    page = request.GET.get('page', 1)
    if 'status' in request.GET:
        reimbursement = Reimbursement_new.objects.filter(name=request.user, status__status=request.GET['status']).order_by('-created_on')
    else:
        reimbursement = Reimbursement_new.objects.filter(name=request.user).order_by('-created_on')
    user_reimbursement = paginate_reimbursement(reimbursement, page)
    return render(request, 'reimbursement_list.html',
                {'user_reimbursement':user_reimbursement,
                'status_filter':status_filter})
    
    

def paginate_reimbursement(reimbursement, page): 
    paginator = Paginator(reimbursement, 5)
    try:
        reimbursements = paginator.page(page)
    except PageNotAnInteger:
        reimbursements = paginator.page(1)
    except EmptyPage:
        reimbursements = paginator.page(paginator.num_pages)
    return reimbursements

def get_details(request):
        details = {}
        details['preparedBy'] = request.POST['prepared_by']
        details['clientName'] = request.POST['client_name']
        details['visitLocation'] = request.POST['visit_location']
        details['fromDate'] = request.POST['from_date']
        details['toDate'] = request.POST['to_date']
        return details

@csrf_exempt
@login_required
def manage_reimbursement(request, id=None):
    row = None
    selectedValue = None
    if id:
        reimbursement = Reimbursement_new.objects.get(pk=id) 
        # reimbursement_form = ReimbursementModelForm(request.user, instance=reimbursement, row=row, initial={"approver":reimbursement.approver})
        # reimbursement_form = ReimbursementModelForm(request.user, instance=reimbursement, row=row)
    else: 
        reimbursement = Reimbursement_new()
        # reimbursement_form = ReimbursementModelForm(request.user, instance=reimbursement, row=row)
    request_copy = request.POST.copy()
    # reimbursement_form = ReimbursementModelForm(request.user, instance=reimbursement, row=row) # setup a form for the parent    
    type_form = Reimbursement_form()
    clientVisitReport_form = ClientVisitReport_Form()
    # formset = allowanceInlineFormSet(request.user, instance=reimbursement)
    if request.method == 'POST':   
        queryDict = request.POST
        if 'add-row' in queryDict.keys():
            request_copy['allowance_set-TOTAL_FORMS'] = int(request_copy['allowance_set-TOTAL_FORMS'])+ 1
            type = ReimbursementType.objects.get(id=int(request_copy['type']))
            if type.type == 'Travel':
                selectedValue = request_copy.get('report', False)
            reimbursement_form = ReimbursementModelForm(request.user, request_copy, request.FILES, instance=reimbursement, row=queryDict['add-row'])
            if id:
                reimbursement_form.data['name'] = reimbursement.name.id
            type_form = Reimbursement_form(request_copy)
            clientVisitReport_form = ClientVisitReport_Form(request.POST)
            formset = allowanceInlineFormSet(request.user, request_copy, request.FILES, instance=reimbursement) 

        elif 'verify' in queryDict.keys():
            # import pdb;pdb.set_trace()
            name = User.objects.get(id=reimbursement.name.id).id
            approver = User.objects.get(id=reimbursement.approver.id).id
            request_copy['name'] = name
            request_copy['status'] = ReimbursementStatus.objects.get(id=request.POST.getlist('status')[0]).id
            request_copy['type'] =  reimbursement.type.id
            request_copy['bill_location'] = request.FILES.get('bill_location')
            reimbursement_form = ReimbursementModelForm(request.user, request_copy, request.FILES, instance=reimbursement, row=row)
            if reimbursement_form.is_valid():
                created_reimbursement = reimbursement_form.save(commit=False)
                created_reimbursement.details = reimbursement.details
                created_reimbursement.created_on = reimbursement.created_on
                formset = allowanceInlineFormSet(request.user, request_copy, request.FILES, instance=created_reimbursement)
                if formset.is_valid():
                    # formset = save_formset(formset)
                    created_reimbursement.save() 

                    formset.save()
                    
                    messages.success(request,
                                     ('Reimbursement Updated Successfully'))
                    return HttpResponseRedirect('/reimbursement/approver/list/')
                    
        elif 'process' in queryDict.keys():
            name = User.objects.get(id=reimbursement.name.id).id
            request_copy['name'] = name
            status = ReimbursementStatus.objects.get(id=request.POST.getlist('status')[0])
            request_copy['status'] = status.id
            reimbursement_form = ReimbursementModelForm(request.user, request_copy, request.FILES, instance=reimbursement, row=row)
            if reimbursement_form.is_valid():
                created_reimbursement = reimbursement_form.save(commit=False)
                if status.status == 'Processed':
                    created_reimbursement.processed_on = today
                created_reimbursement.details = reimbursement.details
                created_reimbursement.created_on = reimbursement.created_on
                formset = allowanceInlineFormSet(request.user, request_copy, request.FILES, instance=created_reimbursement)
                if formset.is_valid():
                    created_reimbursement.save()
                    
                    formset.save()
                    messages.success(request,
                                     ('Reimbursement Updated Successfully'))
                    return HttpResponseRedirect('/reimbursement/approver/list/')


        else:     
            if not id or 'request-user' in queryDict.keys():
                type = ReimbursementType.objects.get(id=int(request_copy['type'])).type
                request_copy['name'] = request.user.id
                request_copy['status'] = ReimbursementStatus.objects.get(status='Pending').id              
                if type == 'Travel':
                    request_copy['client_visit_report'] = request_copy['report']
                else:
                    request_copy['client_visit_report'] = None    
            reimbursement_form = ReimbursementModelForm(request.user, request_copy, request.FILES, instance=reimbursement, row=row)
            type_form = Reimbursement_form(request_copy)
            clientVisitReport_form = ClientVisitReport_Form(request.POST)         
            if reimbursement_form.is_valid():
                formset = allowanceInlineFormSet(request.user, request_copy, request.FILES, instance=reimbursement) 
                is_budget = check_budget(formset)
                created_reimbursement = reimbursement_form.save(commit=False)
                created_reimbursement.created_on = today
                if is_budget == True:
                    created_reimbursement.special_approval = 0
                else:
                    created_reimbursement.special_approval = 1
                type = ReimbursementType.objects.get(id=int(request_copy['type'])).type
                created_reimbursement.details = get_details(request)
                if type == 'Travel':
                    created_reimbursement.details = get_details(request)
                else:
                    created_reimbursement.details = None
                formset = allowanceInlineFormSet(request.user, request_copy, request.FILES, instance=created_reimbursement)
                if formset.is_valid():
                    created_reimbursement, formset = validate_total_amount(created_reimbursement, formset)
                    created_reimbursement.save()
                    formset.save()
                    messages.success(request,
                                    ('Reimbursement created Successfully'))
                    return HttpResponseRedirect('/reimbursement/list/')
                else:
                    for error in formset.errors:
                        for key, value in error.iteritems():
                            messages.error(request, key + " " + str(value[0]))
                        
                    return HttpResponseRedirect('/reimbursement/list/')
            else:
                for error in reimbursement_form.errors:
                    if error == "total_amount":
                        messages.error(request, "Total amount" + " is required")
                # messages.error(request, reimbursement_form.errors)
                return HttpResponseRedirect('/reimbursement/list/')
    else:
        reimbursement_form = ReimbursementModelForm(request.user, instance=reimbursement, row=row)
        formset = allowanceInlineFormSet(request.user, instance=reimbursement)
    return render(request, 'reimbursement_form.html', {'reimbursementModelForm': reimbursement_form, 'type_form':type_form, 'clientVisitReport_form':clientVisitReport_form, 'formset':formset, 'selectedValue':selectedValue})

def save_formset(formset):
    count = 0
    while(count < (len(formset)-1)):
        bill_checking = "allowance_set-"+ str(count) +"-bill_checking"
        formset[count].data[bill_checking] = formset[count].data[bill_checking]
        count +=1
    return formset
        


def validate_total_amount(created_reimbursement, formset):
    count = 0
    while(count < len(formset)):
        delete = "allowance_set-"+ str(count) +"-DELETE"
        if delete in formset[count].data:
            is_delete = formset[count].data["allowance_set-"+ str(count) +"-DELETE"]
            if is_delete == 'on':
                expenditure = formset[count].data["allowance_set-"+ str(count) +"-expenditure"]
                expenditure = formset[count].data["allowance_set-"+ str(count) +"-expenditure"]
                if expenditure != '':
                    created_reimbursement.total_amount = float(created_reimbursement.total_amount) - float(expenditure)
        count += 1
    return created_reimbursement, formset

def check_budget(formset):
    count = 0
    while(count < len(formset)):
        is_budget = True
        expenditure = formset[count].data["allowance_set-"+ str(count) +"-expenditure"]
        category = formset[count].data["allowance_set-"+ str(count) +"-category"]
        if category != '':
            budget = BudgetType.objects.get(id=int(category)).budget
            if expenditure != '':
                if expenditure.isdigit():
                    if(budget >= int(expenditure)):
                        is_budget = True
                        count += 1
                    else:
                        is_budget = False
                        break
                else:
                    if(budget >= float(expenditure)):
                        is_budget = True
                        count += 1
                    else:
                        is_budget = False
                        break
            else:
                break
            
        else:
            break
    return is_budget

@csrf_exempt
@login_required
def Approve(request, id=None):    
    reimbursement = Reimbursement_new.objects.get(pk=id)
    reimbursement.status = ReimbursementStatus.objects.get(status='Approved')
    reimbursement.approved_on = today
    reimbursement.save();
    messages.success(request,
                                 ('Reimbursement Approved Successfully'))
    return HttpResponseRedirect('/reimbursement/approver/list/')

@csrf_exempt
@login_required
def Reject(request, id=None):    
    reimbursement = Reimbursement_new.objects.get(pk=id)
    reimbursement.status = ReimbursementStatus.objects.get(status='Rejected')
    reimbursement.save()
    messages.success(request,
                                 ('Reimbursement Rejected Successfully'))
    return HttpResponseRedirect('/reimbursement/approver/list/')

def cancel(request):
    # import pdb;pdb.set_trace()

    if len(request.POST.getlist('reimbursement_pk')) == 1:
        for pk in request.POST.getlist('reimbursement_pk'):
            reimbursement = Reimbursement_new.objects.get(id=int(pk))
            if reimbursement.status.status == 'Pending':
                reimbursement.status = ReimbursementStatus.objects.get(status='Cancelled')
                reimbursement.save()
                messages.success(request,
                                 ('Reimbursements Cancelled Successfully'))
            else:
                messages.error(request,
                                 ('Delete only pending record'))
    elif len(request.POST.getlist('reimbursement_pk')) == 0:
        messages.error(request,
                                 ('Select record to cancel'))
    else:
        messages.error(request,
                                 ("Can't cancel more than one record"))
    return HttpResponseRedirect('/reimbursement/list/')






            

    
