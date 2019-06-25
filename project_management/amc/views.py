from __future__ import unicode_literals
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from amc.forms import ReportAmcForm, ReportServiceForm
from .models import AmcReport, Project, Service, Status
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.views.generic import ListView
from datetime import datetime, timedelta
from django.contrib import messages
import datetime 
import dateutil.relativedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.response import Response
today = datetime.date.today()
from django.views.decorators.csrf import csrf_exempt


def get_service(request):
    import pdb
    pdb.set_trace()
    if request.method == 'GET':
        service_periods = Service.objects.all()
        service_periods_list = list(service_periods)
        return JsonResponse(service_periods_list, safe=False)


@login_required
def amc_list(request):

    amc_list = AmcReport.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(amc_list, 20)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    return render(request, 'amc_list.html', {'amcList': reports})

@csrf_exempt
@login_required
def manage_amc(request, RedirectView=amc_list, id=None):
    template_name = 'amc_form.html'
    amc = None

    if id:
        amc = get_object_or_404(AmcReport, pk=id)
        if request.method == 'POST':
            Amc_form = ReportAmcForm(request.POST, instance=amc)
            if Amc_form.is_valid():
                amc_form = Amc_form.save(commit=False)
            amc_form.updated_by = get_user(request)
            amc_form.updated_on = timezone.now()
            amc_form.save()
            messages.success(request, _('AMC Saved Sucessfully'))
            return HttpResponseRedirect(reverse(RedirectView))
        else:
            Amc_form = ReportAmcForm(instance=amc)
        return render(
            request, template_name, {
                'Amc_form': Amc_form}, )
    else:
        if request.method == 'POST':
            request_copy = request.POST.copy()
            Amc_form = ReportAmcForm(request_copy, instance=amc)
            service_form = ReportServiceForm(request_copy)
            due_date, AMC_end_date = validate_dateFormat(
                request_copy["Due_date"], request_copy["AMC_end_date"])
            days = request_copy["notification"]
            if "repeat" in request_copy.keys():
                if request_copy["frequency"]:
                    while due_date <= AMC_end_date:
                        alert_date = validate_notification_date(due_date, days)
                        request_copy["notification"] = alert_date
                        if Amc_form.is_valid() and service_form.is_valid():
                            frequency = service_form.cleaned_data['frequency']
                            request_copy["Due_date"] = due_date
                            Amc_form = ReportAmcForm(
                                request_copy, instance=amc)
                            service_form = ReportServiceForm(request_copy)
                            amc_form = Amc_form.save(commit=False)
                            amc_form.created_by = get_user(request)
                            amc_form.created_on = timezone.now()
                            amc_form.status = get_status()
                            amc_form.save()
                            Amc_form.save_m2m()
                            due_date = service_entry(
                                due_date, frequency)
                messages.success(request, _(
                                'AMC Saved Sucessfully'))
                return HttpResponseRedirect(reverse(RedirectView))
            else:
                Amc_form = ReportAmcForm(request_copy, instance=amc)
                service_form = ReportServiceForm(request.POST)
                request_copy["Due_date"] = due_date
                request_copy["AMC_end_date"] = AMC_end_date
                request_copy["notification"] = validate_notification_date(
                    due_date, request_copy["notification"])
                if Amc_form.is_valid():
                    amc_form = Amc_form.save(commit=False)
                    amc_form.created_by = get_user(request)
                    amc_form.created_on = timezone.now()
                    amc_form.status = get_status()
                    amc_form.save()
                    Amc_form.save_m2m()
                    messages.success(request, _('AMC Saved Sucessfully'))
                    return HttpResponseRedirect(reverse(RedirectView))
        else:
            Amc_form = ReportAmcForm(instance=amc)
            service_form = ReportServiceForm()
        return render(
            request, template_name, {
                'Amc_form': Amc_form, 'service_form': service_form}, )


def validate_dateFormat(due_date, amc_end_date):
    due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d')
    AMC_end_date = datetime.datetime.strptime(amc_end_date, '%Y-%m-%d')
    return due_date, AMC_end_date


def service_entry(due_date, frequency):
    split_list = str(frequency).split(' ')
    if str(split_list[1]) == 'year':
        date = due_date + \
            dateutil.relativedelta.relativedelta(years=int(split_list[0]))
    else:
        date = due_date + \
            dateutil.relativedelta.relativedelta(months=int(split_list[0]))
    return date


def get_user(request):
    if request.user.is_authenticated():
        return str(request.user)


def validate_notification_date(due_date, days):
    notification = due_date - timedelta(days=int(days))
    return notification


def get_status():
    status = Status.objects.filter(status="Pending")
    if status:
        for status in status:
            return status
