from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader
from django.db import IntegrityError
from django.shortcuts import redirect
from django_tables2 import RequestConfig
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CvrTableForm
from .tables import CVRTable
from .models import ClientVisitReport
from project_management.projects.models import *
from project_management.users.models import *
from django.contrib.auth.models import User, Group
from django.views.generic.edit import FormView
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
# from django.db.models import Q
import datetime
import settings
from helpers import get_full_domain
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from netifaces import interfaces, ifaddresses, AF_INET
from django.template.loader import get_template
from emailmanager import send
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib import messages


class SubListView(ListView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(SubListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


def list(request, page=1):
        # return render(request, 'sample.html')

    if request.user.is_superuser:
        approvallist = ClientVisitReport.objects.filter(
            reporting_senior_name=request.user.id).filter(
            is_approved=False, is_rejected=False).order_by('-id')
        requestlist = ClientVisitReport.objects.all().order_by('-id')
    else:
        requestlist = ClientVisitReport.objects.filter(
            prepared_by=request.user.username).order_by('-id')
        approvallist = ClientVisitReport.objects.filter(
            reporting_senior_name=request.user.id).filter(
            is_approved=False, is_rejected=False).order_by('-id')
    paginator1 = Paginator(approvallist, 10)
    paginator2 = Paginator(requestlist, 10)
    request_page = request.GET.get('request_page', 1)
    approve_page = request.GET.get('approve_page', 1)
    approvallist = paginator1.page(approve_page)
    requestlist = paginator2.page(request_page)

    return render(request, 'cvr_list.html', {
                  'approvallist': approvallist, 'requestlist': requestlist})


def reports(request, status, page=1):

    if request.user.is_superuser:
        if request.method == 'GET':
            if status == 'approve':
                requestlist = ClientVisitReport.objects.filter(
                    is_approved=True)
                approvallist = None
            elif status == 'reject':
                requestlist = ClientVisitReport.objects.filter(
                    is_rejected=True)
                approvallist = None
    callable = SubListView.as_view(
        queryset='',
        template_name="cvr_list.html",
        extra_context={
            'approvallist': approvallist,
            'requestlist': requestlist,
            'status': status},
        paginate_by=20
    )
    return callable(request)


def create(request, id=None):
    client_visit_report = None
    if id:
        client_visit_report = get_object_or_404(ClientVisitReport, id=id)
    postlist = ClientVisitReport.objects.all()

    if request.POST:
        if request.POST['object']:

            cvr = get_object_or_404(
                ClientVisitReport,
                id=request.POST['object'])
            cvr.project_name = Project.objects.get(
                id=int(request.POST['project_name']))
            cvr.client_name = BusinessUnit.objects.get(
                id=request.POST['client_name'])
            cvr.visit_location = request.POST['visit_location']
            try:
                cvr.from_date = datetime.datetime.strptime(
                    request.POST['from_date'], '%m-%d-%Y')
                cvr.from_date = datetime.date.strftime(
                    cvr.from_date, "%Y-%m-%d")
                cvr.to_date = datetime.datetime.strptime(
                    request.POST['to_date'], '%m-%d-%Y')
                cvr.to_date = datetime.date.strftime(cvr.to_date, "%Y-%m-%d")
            except ValueError:
                cvr.from_date = datetime.datetime.strptime(
                    request.POST['from_date'], '%m/%d/%Y')
                cvr.from_date = datetime.date.strftime(
                    cvr.from_date, "%Y-%m-%d")
                cvr.to_date = datetime.datetime.strptime(
                    request.POST['to_date'], '%m/%d/%Y')
                cvr.to_date = datetime.date.strftime(cvr.to_date, "%Y-%m-%d")

            cvr.reason_for_visit = request.POST['reason_for_visit']
            cvr.actions_taken_during_the_visit = request.POST['actions_taken_during_the_visit']
            cvr.next_plan_of_action = request.POST['next_plan_of_action']
            cvr.comments = request.POST['comments']
            cvr.reporting_senior_name = User.objects.get(
                id=request.POST['reporting_senior_name'])
            cvr.is_rejected = False
            cvr.is_approved = False
            cvr.save()
            messages.success(request,
                             ('Client Visit Report updated Successfully'))

        else:
            form = CvrTableForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.prepared_by = request.user.username
                report.save()
                messages.success(request,
                                 ('Client Visit Report created Successfully'))
        return redirect('/clientvisitreports/')

    else:
        form = CvrTableForm()
    project_name = Project.objects.all()
    client_name = BusinessUnit.objects.filter(type__name='Customer')
    reporting_senior_name = User.objects.filter(
        groups__name='Manager', is_active=True).exclude(
        username=request.user.username)

    context = {
        'form': form,
        'project_names': project_name,
        'client_names': client_name,
        'reporting_senior_names': reporting_senior_name
    }
    return render(request, "sample.html", context, {'some_flag': True})


@login_required
def view_cvr_report(request, id=None):
    client_visit_report = ClientVisitReport.objects.get(id=id)
    obj = model_to_dict(client_visit_report)
    form = CvrTableForm(request.POST, initial=obj)
    project_name = Project.objects.all()
    client_name = BusinessUnit.objects.filter(type__name='Customer')
    reporting_senior_name = User.objects.filter(
        groups__name='Manager', is_active=True)
    context = {
        'form': form,
        'object': obj,
        'project': obj['project_name'],
        'client': obj['client_name'],
        'approve': obj['reporting_senior_name'],
        'project_names': project_name,
        'client_names': client_name,
        'reporting_senior_names': reporting_senior_name,
        'prepared_by': obj['prepared_by'],
        'login_user': request.user.username,
    }
    return render(request, "sample.html", context)


def cvr_approval(request, id, status):

    try:
        cvr = ClientVisitReport.objects.get(id=int(id))
    except ClientVisitReport.DoesNotExist:
        return HttpResponse('Not Found', status=404)

    user1 = User.objects.get(username=cvr.prepared_by)
    if request.method == 'GET':
        if status == 'approve':
            cvr.is_approved = True
            cvr.date_of_approval = datetime.datetime.now()
            cvr.save(update_fields=['is_approved', 'date_of_approval'])
            subject = 'Approved CVR'
            message = "Dear {0},\n\nYour ClientVisitReport has been approved successfully on {1}.\n\nRegrads,\n{2}" .format(
                cvr, datetime.datetime.now(), request.user.username)
            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [
                    user1.email], fail_silently=False)
            messages.success(request,
                             ('Client Visit Report - Approved Successfully'))
            return redirect("/clientvisitreports/")

    else:
        if status == 'reject':
            cvr.is_rejected = True
            cvr.reason_for_reject = request.POST.get('reason')
            cvr.date_of_approval = datetime.datetime.now()
            cvr.save(
                update_fields=[
                    'is_rejected',
                    'reason_for_reject',
                    'date_of_approval'])
            subject = 'Approve Rejected to clent visit report'
            message = "Dear {0},\n\nYour ClientVisitReport has been rejected on {1}.\n\nReason : {2}.\n\n\nRegrads,\n{3}" .format(
                cvr, datetime.datetime.now(), cvr.reason_for_reject, request.user.username)
            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [
                    user1.email], fail_silently=False)
            messages.error(request,
                           ('Client Visit Report has been Rejected'))
            return JsonResponse("Rejected", safe=False)
