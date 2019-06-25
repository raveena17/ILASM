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
from django.views.generic import ListView


def report_details(request, page=1):

    if request.user.is_superuser:
        approvallist = ClientVisitReport.objects.filter(
            reporting_senior_name=request.user.id).filter(
            is_approved=False, is_rejected=False)
        requestlist = ClientVisitReport.objects.all()
    else:
        requestlist = ClientVisitReport.objects.filter(
            prepared_by=request.user.username)
        approvallist = ClientVisitReport.objects.filter(
            reporting_senior_name=request.user.id).filter(
            is_approved=False, is_rejected=False)
    return render(request, 'client_visit_report/cvr_list.html',
                  {'approvallist': approvallist, 'requestlist': requestlist})


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
            else:
                requestlist = ClientVisitReport.objects.all().exclude(
                    is_approved=True, is_rejected=True)
                approvallist = None
    return render(request, 'client_visit_report/cvr_list.html',
                  {'requestlist': requestlist, 'approvallist': approvallist})


def post_new(request, id=None):
    # import pdb;pdb.set_trace()

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
            cvr.client_name = UserProfile.objects.get(
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
        else:
            # import pdb;pdb.set_trace()
            form = CvrTableForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.prepared_by = request.user.username
                # instance = report.prepared_by
                report.save()
        return redirect('/clientvisitreports/')

    else:
        # import pdb;pdb.set_trace()
        form = CvrTableForm()
    project_name = Project.objects.all()
    client_name = UserProfile.objects.filter(type='CC')
    reporting_senior_name = User.objects.filter(
        groups__name='Manager', is_active=True).exclude(
        username=request.user.username)

    context = {
        'form': form,
        'project_names': project_name,
        'client_names': client_name,
        'reporting_senior_names': reporting_senior_name
    }
    return render(request, "client_visit_report/cvr_form.html",
                  context, {'some_flag': True})


@login_required
def view_cvr_report(request, id=None):
    client_visit_report = ClientVisitReport.objects.get(id=id)
    obj = model_to_dict(client_visit_report)
    form = CvrTableForm(request.POST, initial=obj)
    project_name = Project.objects.all()
    client_name = UserProfile.objects.filter(type='CC')
    reporting_senior_name = User.objects.filter(
        groups__name='Manager', is_active=True)
    print obj['reporting_senior_name']
    context = {
        'form': form,
        'object': obj,
        'project': obj['project_name'],
        'client': obj['client_name'],
        'approve': obj['reporting_senior_name'],
        'project_names': project_name,
        'client_names': client_name,
        'reporting_senior_names': reporting_senior_name,
    }
    return render(request, "client_visit_report/cvr_form.html", context)


def send_cvrreport_mail(sender, instance=None,
                        created=False, update_fields=None, **kwargs):
    # import pdb;pdb.set_trace()

    if update_fields:
        if 'is_approved' or 'is_rejected' in update_fields:
            pass
    else:

        user = User.objects.get(username=instance.prepared_by)
        # print '%s' % instance.prepared_by
        reporting_senior = User.objects.get(
            username=instance.reporting_senior_name.username)
        address = [i['addr'] for i in ifaddresses(
            'enp4s0').setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        recipient, _ = get_user_model().objects.get_or_create(email=reporting_senior.email, first_name=reporting_senior.first_name,
                                                              username=reporting_senior.username)  # http://127.0.0.1:8000/cvr/edit/id_num
        sender, _ = get_user_model().objects.get_or_create(
            email=user.email, first_name=user.first_name, username=user.username)
        subject = "Approve CVR form"
        template = get_template('client_visit_report/email/cvr_approval.txt')
        text_body = template.render({
            'client_visit_report': instance,
            'recipient': recipient,
            'reporting_senior_name': reporting_senior,
            'full_domain': "http://" + address[0] + ":8000/clientvisitreports/report/" + str(instance.id) + "/",
            'request_user': instance.prepared_by
        })
        global send
        status = send(recipient, sender, subject, text_body)


models.signals.post_save.connect(send_cvrreport_mail, sender=ClientVisitReport)


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
            message = "Dear {0}\n\nYour client visit report has been approved on {1}.\n\nRegrads\n{2}" .format(
                cvr, datetime.datetime.now(), request.user.username)
            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [
                    user1.email], fail_silently=False)
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
            message = "Dear {0}\n\nYour client visit report has been rejected on {1}.\n Reason : {2}.\n\nRegrads\n{3}" .format(
                cvr, datetime.datetime.now(), cvr.reason_for_reject, request.user.username)
            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [
                    user1.email], fail_silently=False)
            return JsonResponse("Rejected", safe=False)

    # else:
    #     return HttpResponse('Invalid HTTP method', status=302)


# show table
# def report_details(request):
#     if request.user.is_superuser:
#         requestlist = ClientVisitReport.objects.all()
#         approvallist = None
#     else:
#         # requestlist = ClientVisitReport.objects.filter(Q(prepared_by = request.user.username) | Q(reporting_senior_name = request.user.id)).filter(is_approved = False)
#         requestlist = ClientVisitReport.objects.filter(prepared_by = request.user.username)
#         approvallist = ClientVisitReport.objects.filter(reporting_senior_name = request.user.id).filter(is_approved = False, is_rejected = False)
# return render(request, 'client_visit_report/Cvr_Table2.html',
# {'requestlist': requestlist, 'approvallist':approvallist})
