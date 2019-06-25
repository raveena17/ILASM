from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.views.generic import list_detail

from project_management.business_unit.models import BusinessUnit
from project_management.business_unit.forms import BusinessUnitForm
from project_management.address.forms import AddressForm

@login_required
def business_unit_list(request):
    query = Q()
    searchtext = request.GET.get('search', '')
    if searchtext:
        for term in searchtext.split():
            q = Q(name__icontains = term)
        query = query & q
    businessunit_set = BusinessUnit.objects.filter(query).exclude(type__name = 'Customer')
    return list_detail.object_list(
        request,
        queryset = businessunit_set,
        template_name = "businessunit_list.html",
        template_object_name = "businessunit",
        )
@login_required
def manage_business_unit(request, id = None, redirect_to = business_unit_list):
    business_unit = None
    address = None
    if id:
        business_unit = get_object_or_404(BusinessUnit, pk = id)
        address = business_unit.address

    if request.method == 'POST':
        form = BusinessUnitForm(request.POST, instance = business_unit)
        address_form = AddressForm(request.POST, instance = address)
        if form.is_valid() and address_form.is_valid():
            address = address_form.save()
            form.save(address = address)
            messages.success(request, _('Business Unit Saved Sucessfully'))
            return HttpResponseRedirect(reverse(redirect_to))
          
    else:
        form = BusinessUnitForm(instance = business_unit)
        address_form = AddressForm(instance = address)
       
    return render_to_response('manage_business_unit.html', {'form': form,
        'address_form': address_form},
        context_instance = RequestContext(request))

@login_required
def delete_business_unit(request):
    if request.method == 'POST':
        business_unit_ids = request.POST.getlist('businessunit_pk')
        BusinessUnit.objects.filter(pk__in = business_unit_ids).delete()
        messages.success(request, _('Business Unit(s) deleted sucessfully'))
    return HttpResponseRedirect(reverse(business_unit_list))
    

