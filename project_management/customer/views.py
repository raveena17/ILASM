"""
    views for customer.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import ListView

#from django.views.generic import list_detail
# from django.utils import simplejson
try:
    import django.utils.simplejson
except BaseException:
    import json as simplejson

from django.db.models import Q
from django.db import IntegrityError

from project_management.address.forms import AddressForm
from project_management.business_unit.models import BusinessUnit
from project_management.customer.forms import CustomerForm, \
    CustomerContactForm, CustomerContactProfileForm, ClientForm
from project_management.customer.models import Customer
from project_management.users.models import UserProfile
from project_management.business_unit.forms import BusinessUnitForm
from project_management.projects.models import Project
from project_management.business_unit.models import *


class SubListView(ListView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(SubListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


@login_required
def list_customer(request):
    callable = SubListView.as_view(
        queryset=BusinessUnit.objects.filter(type='Customer'),
        template_name="customer_list.html",
        template_object_name="customer"
        # paginate_by = 20
    )
    return callable(request)


@login_required
def manage_customer_from_project(request, id=None):
    """
        Add/Modify the customer in project
    """
    customer = address = None
    if request.method == 'POST':
        id = request.POST.get('customer_id', None)
    if id:
        customer = get_object_or_404(BusinessUnit, pk=id)
        address = customer.address
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, instance=customer)
        address_form = AddressForm(request.POST, instance=address)
        if customer_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            customer = customer_form.save(address=address)
        if request.is_ajax():
            if customer_form.is_valid() and address_form.is_valid():
                data = [{'id': customer.pk, 'name': customer.__unicode__()}]
            else:
                data = [{'error': customer_form.errors}]
            return HttpResponse(simplejson.dumps(data),
                                mimetype='application/json')
    else:
        customer_form = CustomerForm(instance=customer)
        address_form = AddressForm(instance=address)
    return render(request,
                  'customer_from_project.html',
                  {'customer_form': customer_form,
                   'address_form': address_form,
                   'customer_id': id},
                  )


@login_required
def manage_customer_contact_from_project(request, id=None):
    """
        Add/Modify customer contact in project
    """
    contact = address_contact = contact_profile = None
    customer_id = ''
    if request.method == 'POST':
        id = request.POST.get('contact_profile_id', '')
    if id:
        contact_profile = get_object_or_404(UserProfile, pk=id)
        address_contact = contact_profile.address_contact
        contact = contact_profile.user
        customer_id = contact_profile.business_unit.all()[0].pk
    if request.method == 'POST':
        contact_form = CustomerContactForm(request.POST, instance=contact)
        address_contact_form = AddressForm(request.POST,
                                           instance=address_contact)
        contact_profile_form = CustomerContactProfileForm(
            request.POST, instance=contact_profile)
        if contact_form.is_valid() and address_contact_form.is_valid() \
                and contact_profile_form.is_valid():
            contact = contact_form.save()
            address_contact = address_contact_form.save()
            contact_profile = contact_profile_form.save(
                contact=contact, address=address_contact)
            data = [{'id': contact_profile.pk,
                     'name': contact_profile.user.first_name}]
        else:
            data = [{'error': contact_profile_form.errors}]
        return HttpResponse(simplejson.dumps(data),
                            mimetype='application/json')
    else:
        contact_form = CustomerContactForm(instance=contact)
        address_contact_form = AddressForm(instance=address_contact)
        contact_profile_form = CustomerContactProfileForm(
            instance=contact_profile)
    return render(request, 'customer_contact_from_project.html', {
        'contact_profile': contact_profile, 'contact_form': contact_form,
        'address_contact_form': address_contact_form,
        'contact_profile_form': contact_profile_form, 'customer_id': customer_id})


@login_required
def clientlist(request, page=1):
    # def clientlist(request):
    """
        list the customer contact list.
    """
    query = Q(is_active=True)
    searchtext = request.GET.get('search', '')
    show_inactive = request.GET.get('is_active', '0')
    if searchtext:
        for term in searchtext.split():
            q = Q(name__icontains=term)
        query = query & q
    if int(show_inactive):
        query = query | Q(is_active=False)
    callable = SubListView.as_view(
        queryset=BusinessUnit.objects.filter(
            query,
            type__name='Customer').order_by(
            'is_active',
            '-customer_code'),
        template_name="ClientList.html",
        context_object_name="client_list",
        extra_context={
            'show_inactive': int(show_inactive)},
        paginate_by=20)
    return callable(request)


@login_required
def manage_client(request, id=None):
    business_unit = None
    address = project = None
    task_id = ''
    project_id = request.GET.get('id', '')
    project_is_approve = request.GET.get('approve', '')
    if project_id:
        project = Project.objects.get(code=project_id)
    if id:
        business_unit = get_object_or_404(BusinessUnit, pk=id)
        address = business_unit.address

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=business_unit)
        address_form = AddressForm(request.POST, instance=address)
        Name = request.POST.get('name')
        print "Name ", Name
        Client = BusinessUnit.objects.filter(name=Name)
        print "Hello", len(Client)
        if(len(Client) > 0):
            messages.error(request, _('Client Name Already Exists'))
        else:
            if form.is_valid() and address_form.is_valid():
                address = address_form.save()
                task = form.save(address=address)
                task_id = task.id
                messages.success(request, _('Client Saved Successfully'))
                print task_id

    else:
        form = ClientForm(instance=business_unit)
        address_form = AddressForm(instance=address)
#    print request
    return render(request, 'client_create.html', {'form': form,
                                                  'address_form': address_form,
                                                  'project': project,
                                                  'task_id': task_id
                                                  })


@login_required
def manage_client_status(request, is_active=True):
    """
        Change project status
    """
    if request.method == 'POST':
        ids = request.POST.getlist('client_pk')
        try:
            for client_id in ids:
                client = BusinessUnit.objects.get(id=client_id)
                client.is_active = is_active
                client.save()
            messages.success(request, _('Client(s) status saved sucessfully'))
        except Exception as e:
            messages.error(request, _('Client(s) status change failed'))
    return HttpResponseRedirect(reverse(clientlist))
