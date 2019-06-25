from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.template import RequestContext
#from django.views.generic import list_detail

from project_management.AMC_Report.models import *
from project_management.AMC_Report.forms import *
from django.views.generic import RedirectView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime 
import dateutil.relativedelta
from django.utils import timezone
today = datetime.date.today()
from project_management.business_unit.models import BusinessUnit
from django.views.decorators.csrf import csrf_exempt





class SubListView(ListView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(SubListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


def update_amc(request,id=None):
    template_name = 'amc_report_form.html'
    amc = None

    if id:
        amc = get_object_or_404(ReportAMC1, pk=id)
        if request.method == 'POST':

            amc_1 = get_object_or_404(ReportAMC1,pk=id)
            amc_1.project = Project.objects.get(id=request.POST['project'])
            amc_1.client_name = BusinessUnit.objects.get(id=request.POST['client_name'])
            amc_1.description = request.POST['description']
            amc_1.amc_start_date = request.POST['amc_start_date']
            amc_1.amc_end_date = request.POST['amc_end_date']
            amc_1.frequency = request.POST['frequency']
            amc_1.is_active = True
            try:
                amc_1.document = request.POST['document']
            except:
                amc_1.document = request.FILES['document']
                
            if amc_1.document == '':
                amc_1.document = ReportAMC1.objects.get(id=id).document
            amc_1.save()
            messages.success(request, _('AMC Updated Sucessfully'))
            return HttpResponseRedirect('/AMC/list/')
        else:
            Amc_form = AMCForm(instance=amc)
            amc_id = ReportAMC1.objects.get(id=id)
            end_date = amc_id.amc_end_date
            end_date1 = str(end_date)
            date1 = datetime.datetime.strptime(end_date1,"%Y-%m-%d").date()
            renew_date = date1 - dateutil.relativedelta.relativedelta(months=1)
        return render(
            request, template_name, {
                'Amc_form': Amc_form, 'renew_date':renew_date,'today':today,'amc_id':amc_id.id, 'data':id})



@login_required
def manage_AMC_Report(request, id=None):
    AMC_Report = None
    if id:
        data = id
        Amc_form = get_object_or_404(ReportAMC1, pk=id)
    else: 
        if request.method == 'POST':
            request_copy = request.POST.copy()
            try:
                request_copy['document'] = request.FILES['document']
            except:
                request_copy['document'] = request.POST['document']
            Amc_form = AMCForm(request.POST, request.FILES, AMC_Report)
            
            if Amc_form.is_valid():
                Amc_form.amc_created_date = datetime.date.today()
                Amc_form.is_active = True
                Amc_form.save(request)
                messages.success(request, _('AMC Created Sucessfully'))
            return HttpResponseRedirect('/AMC/list/')
        else:
            data = id
            Amc_form = AMCForm(data=request.POST,instance=AMC_Report)

    return render(request, 'amc_report_form.html', {
                  'Amc_form': Amc_form, 'data':data})



@login_required
def AMC_Report_list(request, page=1, msg=''):
    show_inactive = 0
    query = Q(is_active=True)
    searchtext = request.GET.get('search', '')
    if request.GET.get('is_active'):
        global show_inactive
        show_inactive = request.GET.get('is_active')

    if searchtext:
        for term in searchtext.split():
            q = Q(amc__icontains=term)
        query = query & q

    if int(show_inactive):
        query = Q(is_active=False)

    amc_list = ReportAMC1.objects.filter(query).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(amc_list, 20)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    return render(request, 'amc_report_list.html', {'amcList': reports, 'show_inactive': int(show_inactive)})


@csrf_exempt
@login_required
def renew_amc(request,id=None):
    template_name = 'amc_report_form.html'
    amc = None
    if id:
        "History Table"

        Amc_form = get_object_or_404(ReportAMC1, pk=id)
        reportamc = AmcHistory.objects.create(
            amc_id=Amc_form.id,
            client_name =Amc_form.client_name,
            project = Amc_form.project,
            description = Amc_form.description,
            amc_start_date = Amc_form.amc_start_date,
            frequency =  Amc_form.frequency,
            amc_end_date = Amc_form.amc_end_date,
            file_document = Amc_form.document,
            is_active = Amc_form.is_active,
            amc_renewal_date = datetime.date.today())

        Amc_form.project = Amc_form.project
        Amc_form.client_name = Amc_form.client_name
        Amc_form.description = Amc_form.description
        Amc_form.is_active = Amc_form.is_active
        Amc_form.document = Amc_form.document
        Amc_form.amc_start_date = Amc_form.amc_end_date
        frequency = Amc_form.frequency
        Amc_form.amc_end_date = (Amc_form.amc_start_date +dateutil.relativedelta.relativedelta(months=int(frequency)))
        Amc_form.save()

        messages.success(request, _('AMC Renewed Sucessfully'))
    return HttpResponseRedirect('/AMC/list/')


@login_required
def manage_user_status(request, status=None):
    """
        Activate/Deactivate the users.
    """
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        data_list = request.POST.getlist('amc_pk') #name
        try:
            for data in data_list:
                amc = ReportAMC1.objects.get(pk=data)
                amc.is_active = status
                amc.save()
            messages.success(
                request, _('AMC status changed successfully.'))
        except Exception:
            messages.error(request, _('AMC status change Failed'))
    return HttpResponseRedirect('/AMC/list/')



