"""
    cron that send email for approval of the project
"""
from django_cron import cronScheduler, Job
from project_management.Utility import Email
from project_management.conferenceroombooking.models import ConferenceRoom, BookConference,MeetingAttendees

import datetime

CONTENT_TYPE = 'html'

class MeetingRemainder(Job):
    """
        Cron Job that checks the lgr users mailbox and adds any approved senders' attachments to the db
    """

    # run every 43200 seconds (12 minutes)
    run_every = 60

    def job(self):
        # This will be executed every 1 minutes
        book_conference_room = BookConference.objects.all()
        meeting = MeetingAttendees.objects.filter(conference_room = book_conference_room.name_of_meeting )
        conference = BookConference.objects.filter(meeting_date = (datetime.date.today()))
        print datetime.date.today()
        email_subject = 'Remainder Mail'
        emailMessage = 'Today is the date for the meeting ' + str(book_onference_room.name_of_meeting) + '.'
        for each in User.objects.filter(is_active = 'True').exclude(username = 'superuser'):
            for each1 in meeting:
                if str(each1.attendees) == str(each.username):
                   Email().send_email(email_subject, message, [each.email], CONTENT_TYPE)
        

cronScheduler.register(MeetingRemainder)


