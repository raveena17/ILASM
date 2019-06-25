# from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseRedirect
from django.template import RequestContext
#from django.views.generic import list_detail
from django.contrib.auth.models import User
from django.db.models import Q
from project_management.Utility import Email
from django.template.loader import get_template
from django.template import Context
from project_management.users.models import UserProfile
from announcements.models import Announcement




actionMsg = {
    '': '',
    'CREATED': 'Announcement saved successfully.',
    'DELETED': 'Announcement deleted successfully.',
    'APPROVED': 'Announcement was approved successfully'
    }

announcement_list = {
    "queryset" : Announcement.objects.all(),
    "template_name" : "Announcement_List.html",
    }
CONTENT_TYPE = 'html'
@login_required
def announcement_list(request, msg = ''):
    from datetime import timedelta
    from datetime import datetime
    login_user = request.user
    datevalue = Announcement.objects.all()
    query = Q()
    searchtext = request.GET.get('search', '')
    if searchtext:
        for term in searchtext.split():
            q = Q(title__icontains = term)
        query = query & q
    announcementList = Announcement.objects.filter(query).order_by('-creation_date')
    for each in announcementList:
        each.__dict__.update({'display_image': 'Show' if (each.creation_date + timedelta(days = 2) > datetime.now()) else 'Hide' })    
    for each in announcementList:
        print each.__dict__
        #print  '%s - %s = %s' % (each.title , each.creation_date , each.display_image)
    return list_detail.object_list(
        request,
        queryset = announcementList ,
        template_name = "Announcement_List.html",
        template_object_name = "announcement",
        extra_context = {'msg': actionMsg[msg], 'login_user' : login_user, 'datevalue': datevalue}
        )


@login_required
def GetAnnouncementDetail(request):
    
    announcement = Announcement(
        pk = request.POST.get('announcementID', None),
        title = request.POST.get('announcementname', ''),
        content = request.POST.get('announcementcontent', ''),
        approved_by_id= request.POST.get('id_approved_by', ''),
        requested_by_id = request.POST.get('hdn_id_requested_by', ''),
        )
    
    if not announcement.pk:
        announcement.pk = None
       
    return announcement

@login_required
def SaveAnnouncement(request):
    #approved_by = User.objects.filter(groups__name = 'Corporate Admin')
    #requested_by = request.user
    msg = ''
    recipients = ''
    user = ''
    login_user = request.user
    announcement = GetAnnouncementDetail(request)
    if request.method == 'POST':
        if request.POST.get('mode', '') == 'update':
            announcement.creation_date = request.POST.get('announcementdate', '')

        announcement.save()


        email_subject = 'New Announcement for approval'
                #for each in User.objects.filter(groups__name = 'Corporate Admin'):
                #    recipients = each.email

        user = User.objects.get(username = announcement.approved_by)
        recipients = user.email
        #template = get_template('Announcement_Mail.html')
        #data = {'Requested_by' : str(announcement.requested_by),
        #        'Title' : str(announcement.title),
        #        'Content' : str(announcement.content),
        #        'Created_on' : str(announcement.creation_date),
        #        'approved_by' : str(announcement.approved_by)
        #        }
        #email_message = template.render(Context(data))
        email_message = 'A new announcement ' +  str(announcement.title) + ' has been created by ' + str(announcement.requested_by)
        try:
            Email().send_email(email_subject, email_message, [recipients], CONTENT_TYPE)
            msg = 'CREATED'
        except Exception:
            errMessage = 'Email Sending failed \n %s' % (Exception)
    return render(request, 'CreateAnnouncement.html',
        {'msg': actionMsg[msg], 'login_user': login_user},
        )

@login_required
def UpdateAnnouncement(request):
    toUpdate = request.GET.get('ids', '')
    login_user = request.user
    announcement = Announcement.objects.filter(pk = toUpdate) if toUpdate != '' else ''    
    announcement = announcement[0] if announcement else announcement
    approved_by = User.objects.filter(groups__name = 'Corporate Admin').filter(is_active = '1')
    
    
    return render(request, 'CreateAnnouncement.html',
        {'announcement':announcement, 'mode':'update','approved_by':approved_by, 'login_user': login_user},
        )

@login_required
def ViewAnnouncement(request):
    msg=''
    login_user = request.user
    toView = request.GET.get('ids', '')
    announcement = Announcement.objects.filter(pk = toView) if toView != '' else ''
    announcement = announcement[0] if announcement else announcement
   
    return render(request, 'AnnouncementView.html',
        {'announcement':announcement, 'login_user' : login_user, 'msg' : msg},
        )

@login_required
def DeleteAnnouncement(request):
    msg = ''
    toDelete = request.GET.get('ids', '')
    if toDelete != '':
        Announcement.objects.filter(pk = toDelete).delete()
        msg = 'DELETED'
    return announcement_list(request, msg)
    
def ShowApprovedBy(request):
    approved_by = User.objects.filter(groups__name = 'Corporate Admin').filter(is_active = '1')
    requested_by = request.user
    requested_by_id = request.user.pk
    return render(request, 'CreateAnnouncement.html',{'approved_by' : approved_by, 'requested_by' : requested_by, 'requested_by_id' : requested_by_id},)


        

def ApproveAnnouncement(request):
    msg =''
    toApprove = request.GET.get('ids', '')
    login_user = request.user
    
    announcement = Announcement.objects.filter(pk = toApprove) if toApprove != '' else ''    
    announcement = announcement[0] if announcement else announcement
    approve = request.POST.get('Approve', '')
    reject = request.POST.get('Reject','')
    title = request.POST.get('announcementname','')
    content = request.POST.get('announcementcontent','')
    created_date = request.POST.get('announcementdate','')
    
    if approve == "Approve":
        announcement.is_approved = "1"
        announcement.title = title
        announcement.content = content
        announcement.creation_date = created_date
        announcement.save()
        
        email_subject = 'New Announcement Approval Status'
        email_subject1 = 'New Announcement - ' + str(announcement.title)
                    #for each in User.objects.filter(groups__name = 'Corporate Admin'):
                    #    recipients = each.email
        
           
        #user = User.objects.get(username = announcement.requested_by)
        #recipients = user.email
        
            #template = get_template('Announcement_Mail.html')
            #data = {'Requested_by' : str(announcement.requested_by),
            #        'Title' : str(announcement.title),
            #        'Content' : str(announcement.content),
            #        'Created_on' : str(announcement.creation_date),
            #        'approved_by' : str(announcement.approved_by)
            #        }
            #email_message = template.render(Context(data))
        Title = str(announcement.title)
        email_message = 'Announcement ' +  str(announcement.title) +  ' was approved by ' + str(announcement.approved_by)
        template = get_template('Approved_Announcement_Mail.html')
        data = {'Title' : Title }
        email_message1 = template.render(Context(data))
        try:
            #Email().send_email(email_subject, email_message, [recipients], CONTENT_TYPE)
            ommission = "@example.com"
            for each in UserProfile.objects.filter(code__startswith="E"):
                if(each.user.is_active == True):
                    if(each.user.email.endswith(ommission) != True):
                        Email().send_email(email_subject1, email_message1, [each.user.email], CONTENT_TYPE)
            msg = 'APPROVED'
        except Exception:
            errMessage = 'Email Sending failed \n %s' % (Exception)
            
    elif reject == "Reject":
        user = User.objects.get(username = announcement.requested_by)
        recipients2 = user.email
        email_message = 'Your request to a new announcement was rejected by ' + str(announcement.approved_by)
#        Email().send_email('Announcement Approval Status', email_message, [recipients2], CONTENT_TYPE)
    
    return render(request, 'CreateAnnouncement.html',
        {'announcement':announcement, 'mode':'update',  'login_user': login_user, 'msg': msg},
        )       
