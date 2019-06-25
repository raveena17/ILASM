from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.utils.translation import ugettext as _
from project_management.notifications.models import Event
from project_management.notifications.forms import EventForm
from django.views.generic import RedirectView
from django.views.generic import ListView
import eventviews


class SubListView(ListView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(SubListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


def event_list(request):
    query = Q()
    searchtext = request.GET.get('search', '')
    if searchtext:
        for term in searchtext.split():
            q = Q(name__icontains=term)
        query = query & q
    event_set = Event.objects.filter(query)
    callable = SubListView.as_view(
        queryset=event_set,
        template_name="event_list.html",
        context_object_name="event_list",
        paginate_by=20
    )
    return callable(request)


def manage_event(request, id=None, RedirectView=event_list):
    event = None
    if id:
        event = get_object_or_404(Event, pk=id)
    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save(user=request.user)
            messages.success(request, _('Event saved successfully.'))
            return HttpResponseRedirect(reverse(RedirectView))
    else:
        event_form = EventForm(instance=event)
    return render(request, 'event.html', {'event_form': event_form},
                  )


def delete_event(request):
    if request.method == 'POST':
        business_unit_ids = request.POST.getlist('event_pk')
        Event.objects.filter(pk__in=business_unit_ids).delete()
        messages.success(request, _('Event(s) deleted sucessfully'))
    return HttpResponseRedirect(reverse(event_list))
