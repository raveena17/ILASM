from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from django.utils import simplejson
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from project_management.conferenceroombooking.icalendar import createics

from project_management.templatecalendar import month_cal,  getToday,\
				__getTimes__,__getTimezone__, getEventTimes, adjust_datetime_to_timezone


from project_management.conferenceroombooking.models import ConferenceRoom, BookConference,MeetingAttendees
from project_management.conferenceroombooking.forms import ConferenceRoomForm, BookConferenceRoomForm
from project_management.Utility import Email

CONTENT_TYPE = 'html'
@login_required
def manage_room_creation(request, id = None):
    conference_room = None
    if id:
        conference_room = get_object_or_404(ConferenceRoom, pk = id)
        
    if request.method == 'POST':
        form = ConferenceRoomForm(request.POST, instance = conference_room)        
        if form.is_valid():            
            form.save()
            messages.success(request, _('Conference Room Saved Sucessfully'))
    else:
        form = ConferenceRoomForm(instance = conference_room)        
       
    return render_to_response('create_conference_room.html', {'form': form},
        context_instance = RequestContext(request))


    
@login_required
def manage_book_conference_room(request):
    book_conference_room = conference_id = conference_requesting_date =  FromTime = ToTime = None
    book_conf_id = 0
    id = request.GET.get('id', None)
    is_approved = requestingMember = None
    user_list = id_list =[]
    attendees_list = AssigneesInvited =  []
    
    
    if id:
        book_conference_room = get_object_or_404(BookConference, pk = id)
        conference_id = book_conference_room.id
        requestingMember = book_conference_room.requested_by
        FromTime = book_conference_room.from_time.strftime('%H:%M')
        ToTime = book_conference_room.to_time.strftime('%H:%M')
        attendees_list = MeetingAttendees.objects.filter(conference_name = book_conference_room.name_of_meeting)
        attendees_set = set([each.attendees_id for each in attendees_list])
        for each in attendees_set:
            list2 = User.objects.filter(id = each)
       
    user_list = User.objects.filter(is_active = 'True').exclude(username = 'superuser')
    
    if request.method == 'POST':
        form = BookConferenceRoomForm(data = request.POST, instance = book_conference_room, user = request.user)
        if form.is_valid():
            form.save()
            selected_MeetingTeam = set([User.objects.get(id = ID) for ID in request.POST.getlist('selectedmeetinginvitees')])
           
            existing_MeetingTeam = set([each.attendees  for each in MeetingAttendees.objects.filter(conference_name =  form.cleaned_data['name_of_meeting'])])
            insertAssignees = set (selected_MeetingTeam) - set(existing_MeetingTeam)
            deleteAssignees = set(existing_MeetingTeam) - set (selected_MeetingTeam)
            [MeetingAttendees.objects.filter(conference_name = form.cleaned_data['name_of_meeting'], attendees = each).delete() for each in deleteAssignees]
            [MeetingAttendees( conference_name = form.cleaned_data['name_of_meeting'] , attendees = each ).save() for each in insertAssignees]
            
            
            attendees_list = MeetingAttendees.objects.filter(conference_name = form.cleaned_data['name_of_meeting'])  
           
            if id:
                attendees_list = MeetingAttendees.objects.filter(conference_name = book_conference_room.name_of_meeting)
                  
            if id and book_conference_room.is_approved:
                
                attendees_list = MeetingAttendees.objects.filter(conference_name = book_conference_room.name_of_meeting)
                email_subject = "Meeting Attending Request"
                email_message = "You are invited for " + str(book_conference_room.name_of_meeting) + ' on ' + str(book_conference_room.meeting_date) + ' from ' + str(book_conference_room.from_time)  + ' to ' + str(book_conference_room.to_time)  + ' from ' + str(book_conference_room.requested_by)
                for each in User.objects.filter(is_active = 'True').exclude(username = 'superuser'):
                    for each1 in attendees_list:
                        if str(each1.attendees) == str(each.username):
                           Email().send_email(email_subject, email_message, [each.email], CONTENT_TYPE)
            
            is_approved = form.cleaned_data['is_approvedby']
            if id and is_approved != "":                
                if is_approved == 'Approve':
                    email_message = "Conference room booked on "  + str(form.cleaned_data['meeting_date']) + ' from ' + str(form.cleaned_data['from_time']) + 'to ' + str(form.cleaned_data['to_time']) + ' was approved by ' + str(form.cleaned_data['approved_by'])
                else:
                    email_message = "Conference room booked on " + str(form.cleaned_data['meeting_date']) + ' from ' + str(form.cleaned_data['from_time']) + 'to ' + str(form.cleaned_data['to_time']) + ' was rejected by ' + str(form.cleaned_data['approved_by'])
                email_subject = 'Conference room Approval Status'
                
                user = User.objects.get(username = form.cleaned_data['requested_by'])
                recipients = user.email                 
                #user1 = User.objects.filter(groups__name = 'Manager', is_active = True).exclude(username = form.cleaned_data['requested_by'])
                #for each in user1:
                #    recipents1 = each.email                    
                try:
                    Email().send_email(email_subject, email_message, [recipients], CONTENT_TYPE)
                    if is_approved:
                        messages.success(request, _('Conference room request - Approved'))
                    else:
                        messages.success(request, _('Conference room request - Rejected'))
                except Exception:
                    errMessage = 'Email Sending failed \n %s' % (Exception)
            if id == None:
                email_subject = 'Conference Room Booking'
                email_message = 'Conference Room ' +  str(form.cleaned_data['conference_room']) +   ' has been requested by ' +  str(form.cleaned_data['requested_by']) + ' on ' + str(form.cleaned_data['meeting_date']) + ' from ' + str(form.cleaned_data['from_time']) + 'to ' + str(form.cleaned_data['to_time'])
                
                user = User.objects.get(username = form.cleaned_data['approved_by'])
                recipients = user.email                
                try:
                    Email().send_email(email_subject, email_message, [recipients], CONTENT_TYPE)                
                except Exception:
                    errMessage = 'Email Sending failed \n %s' % (Exception)
                messages.success(request, _('Your conference room request has been sent for approval'))
    else:
        form = BookConferenceRoomForm(instance = book_conference_room, user = request.user)
        
    return render_to_response('book_conference_room.html', {'form': form, 'conference_id': conference_id,
                            'book_conference_room':book_conference_room, 'times':__getTimes__(),
                            'FromTime': FromTime, 'ToTime': ToTime,'requestingMember': requestingMember,
                            'user_list': user_list, 'attendees_list': attendees_list, 'id_list':id_list},
                            context_instance = RequestContext(request))    