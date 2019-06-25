from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User, Group

from project_management.users.models import UserProfile
from project_management.business_unit.models import BusinessUnit
from project_management.announcements.models import Announcement
from project_management.projectbudget.tests.logintest import LoginTest


class AnnouncementTest(TestCase):
    client = Client()

    def setUp(self):
        self.client = LoginTest('testlogin').testlogin()
        User.objects.create(
            username='admin3',
            first_name='admin3',
            email='ashok@5gindia.net',
            is_staff='1',
            is_active='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')
        User.objects.create(
            username='ashok',
            first_name='kumar',
            email='ashok@5gindia.net',
            is_staff='1',
            is_active='1')
        self.user_list = User.objects.all()
        Group.objects.create(name='Corporate Admin')
        self.group_list = Group.objects.all()
        '''
        Adding Corparate Admin Group to the user.
        '''
        self.user_list[1].groups.add(self.group_list[0])
        UserProfile.objects.create(
            user_id=self.user_list[2].id,
            code='E003',
            is_confirmed=1,
            confirmation_status='CONFIRMED')

    def test_create_announcement(self):
        # clearing the mail outbox
        mail.outbox = []
        response = self.client.post('/announcements/create/')
        self.assertEquals(response.status_code, 200)
        response = self.client.post('/announcements/save/',
                                    {'announcementname': 'sample test',
                                     'announcementcontent': 'sample content',
                                     'id_approved_by': self.user_list[1].id,
                                     'hdn_id_requested_by': self.user_list[0].id,
                                     })
        self.assertEquals(response.status_code, 200)
        all_announcement = Announcement.objects.all()
        self.assertEquals(len(all_announcement), 1)

    def test_update_announcement(self):
        self.test_create_announcement()
        update_announcement = Announcement.objects.get(pk=1)
        response = self.client.post('/announcements/update/?ids='
                                    + str(update_announcement.pk) + '')
        self.assertEquals(response.status_code, 200)

    def _login_as_approver(self):
        '''
        Login as approver to approve announcement
        '''
        approve_user = User.objects.get(pk=2)
        approve_user.set_password('admin')
        approve_user.save()
        response = self.client.post('/login/', {
                                    'username': 'admin3',
                                    'password': 'admin',
                                    })
        self.assertEquals(response.status_code, 302)
        return response.client

    def test_approve_announcement(self):
        # clearing the mail outbox
        mail.outbox = []
        self.test_create_announcement()
        self.client = self._login_as_approver()
        approve_announcement = Announcement.objects.get(pk=1)
        response = self.client.post('/announcements/approve/?ids='
                                    + str(approve_announcement.pk) + '',
                                    {
                                        'Approve': 'Approve',
                                        'announcementname': 'sample test',
                                        'announcementcontent': 'sample content'
                                    })
        self.assertEquals(response.status_code, 200)
        approved_announcement = Announcement.objects.get(pk=1)
        self.assertEquals(approved_announcement.is_approved, True)

    def test_reject_announcement(self):
        # clearing the mail outbox
        mail.outbox = []
        self.test_create_announcement()
        self.client = self._login_as_approver()
        approve_announcement = Announcement.objects.get(pk=1)
        response = self.client.post('/announcements/approve/?ids='
                                    + str(approve_announcement.pk) + '',
                                    {
                                        'Reject': 'Reject',
                                        'announcementname': 'sample test',
                                        'announcementcontent': 'sample content'
                                    })
        self.assertEquals(response.status_code, 200)
        approved_announcement = Announcement.objects.get(pk=1)
        self.assertEquals(approved_announcement.is_approved, False)

    def test_delete_announcement(self):
        self.test_create_announcement()
        delete_announcement = Announcement.objects.get(pk=1)
        self.assertEquals(len(Announcement.objects.all()), 1)
        response = self.client.post('/announcements/delete/?msg=''&ids='
                                    + str(delete_announcement.pk) + '')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(Announcement.objects.all()), 0)

    def test_announcement_list(self):
        self.test_approve_announcement()
        response = self.client.post('/announcements/list/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['datevalue']), 1)
        # search text in list
        response = self.client.post('/announcements/list/?search=sample')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['datevalue']), 1)

    def _test_user_view_alogin(self):
        normal_user = User.objects.get(pk=3)
        normal_user.set_password('admin')
        normal_user.save()
        response = self.client.post('/login/', {
                                    'username': 'ashok',
                                    'password': 'admin',
                                    })
        self.assertEquals(response.status_code, 302)
        return response.client

    def test_view_announcement(self):
        self.test_approve_announcement()
        self.client = self._test_user_view_alogin()
        all_announcement = Announcement.objects.all()
        response = self.client.get('/announcements/view/?ids='
                                   + str(all_announcement[0].pk) + '')
        self.assertEquals(response.status_code, 200)
