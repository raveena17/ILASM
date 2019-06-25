from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from project_management.users.models import UserProfile
from project_management.travel.models import *
from project_management.projectbudget.models import SaveRecordStatus
from project_management.projectbudget.tests.logintest import LoginTest


class LocalConveyanceTest(TestCase):
    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()
        User.objects.create(username='admin3',
                            first_name='admin3',
                            email='ashok@5gindia.net',
                            is_staff='1',
                            is_active='1',
                            last_login='2012-09-24 05:16:45',
                            date_joined='2012-09-24 05:16:45')
        User.objects.create(username='ashok',
                            first_name='kumar',
                            email='ashok@5gindia.net',
                            is_staff='1',
                            is_active='1')
        self.user_list = User.objects.all()
        Group.objects.create(name='Corporate Admin')
        self.group_list = Group.objects.all()
        # Adding the user to Corparate Admin Group
        self.user_list[1].groups.add(self.group_list[0])
        UserProfile.objects.create(user_id=self.user_list[0].id,
                                   code='E003',
                                   is_confirmed=1,
                                   confirmation_status='CONFIRMED',
                                   reporting_senior=self.user_list[2].username)
        SaveRecordStatus.objects.create(id='RS1', code='RS1', status='Saved')
        SaveRecordStatus.objects.create(
            id='RS2', code='RS2', status='Submitted')
        SaveRecordStatus.objects.create(
            id='RS3', code='RS3', status='Approved')
        SaveRecordStatus.objects.create(
            id='RS4', code='RS4', status='Approved')
        SaveRecordStatus.objects.create(
            id='RS5', code='RS5', status='Rejected')
        self.status_record = SaveRecordStatus.objects.all()
        ClaimAmount.objects.create(vehicle='two_wheeler', amount=2)
        ClaimAmount.objects.create(vehicle='four_wheeler', amount=4)

    def test_manage_lconveyance(self):
        # clear the mail outbox
        mail.outbox = []
        response = self.client.post(reverse('travel:list'))
        travel_list = Travel.objects.all()
        self.assertEquals(len(travel_list), 0)
        # Create local conveyance
        response = self.client.post(reverse('travel:create'))
        self.assertEquals(response.status_code, 200)
        # Save the Reimbursement
        response = self.client.post(reverse('travel:save'),
                                    {'travel_name': 'Travel Conveyance',
                                     'requested_by': self.user_list[0].username,
                                     'request_to': self.user_list[1].username,
                                     'final_approver': self.user_list[2].id,
                                     'claim_to_date': '03-04-2012',
                                     'claim_from_date': '03-04-2012',
                                     'vehicle': 'two_wheeler',
                                     'applied_date': '03-08-2012',
                                     'travel_status': self.status_record[0].id,
                                     'total_km': 100,
                                     'total_rs': 200,
                                     'expenditure_len': 2,
                                     'delete_expenditure': '',
                                     'expend_date1': '03-04-2012',
                                     'client_name1': 'Airlines',
                                     'destination1': 'Chennai-23',
                                     'km1': 100})
        self.assertEquals(response.status_code, 302)
        travel_list = Travel.objects.all()
        self.assertEquals(len(travel_list), 1)
        self.assertEquals(travel_list[0].status_id, 'RS1')

        # Submit the Local Conveyance
        submit_travel = Travel.objects.all()
        response = self.client.post(reverse('travel:save'),
                                    {'travel_id': submit_travel[0].id,
                                     'travel_name': 'Travel Conveyance',
                                     'requested_by': self.user_list[0].username,
                                     'request_to': self.user_list[1].username,
                                     'final_approver': self.user_list[2].id,
                                     'claim_to_date': '03-04-2012',
                                     'claim_from_date': '03-04-2012',
                                     'vehicle': 'two_wheeler',
                                     'applied_date': '03-08-2012',
                                     'travel_status': self.status_record[1].id,
                                     'total_km': 100,
                                     'total_rs': 200,
                                     'expenditure_len': 2,
                                     'delete_expenditure': '',
                                     'expend_date1': '03-04-2012',
                                     'client_name1': 'Airlines',
                                     'destination1': 'Chennai-23',
                                     'km1': 100})
        self.assertEquals(response.status_code, 302)
        travel_list = Travel.objects.all()
        self.assertEquals(len(travel_list), 1)
        self.assertEquals(travel_list[0].status_id, 'RS2')

    def test_approve_lconveyance(self):
        # First level of approvel
        self.test_manage_lconveyance()
        approve_travel = Travel.objects.all()
        first_level_approval = self.client.post(reverse('travel:save'),
                                                {'travel_id': approve_travel[0].id,
                                                 'travel_name': 'Travel Conveyance',
                                                 'requested_by': self.user_list[0].username,
                                                 'request_to': self.user_list[1].username,
                                                 'final_approver': self.user_list[2].id,
                                                 'claim_to_date': '03-04-2012',
                                                 'claim_from_date': '03-04-2012',
                                                 'vehicle': 'two_wheeler',
                                                 'applied_date': '03-08-2012',
                                                 'travel_status': self.status_record[2].id,
                                                 'total_km': 100,
                                                 'total_rs': 200,
                                                 'expenditure_len': 2,
                                                 'delete_expenditure': '',
                                                 'expend_date1': '03-04-2012',
                                                 'client_name1': 'Airlines',
                                                 'destination1': 'Chennai-23',
                                                 'km1': 100})
        self.assertEquals(first_level_approval.status_code, 302)
        travel_list = Travel.objects.all()
        self.assertEquals(len(travel_list), 1)
        self.assertEquals(travel_list[0].status_id, 'RS3')

        # Second Level of approvel
        approve_travel = Travel.objects.all()
        final_level_approval = self.client.post(reverse('travel:save'),
                                                {'travel_id': approve_travel[0].id,
                                                 'travel_name': 'Travel Conveyance',
                                                 'requested_by': self.user_list[0].username,
                                                 'request_to': self.user_list[1].username,
                                                 'final_approver': self.user_list[2].id,
                                                 'claim_to_date': '03-04-2012',
                                                 'claim_from_date': '03-04-2012',
                                                 'vehicle': 'two_wheeler',
                                                 'applied_date': '03-08-2012',
                                                 'travel_status': self.status_record[3].id,
                                                 'total_km': 100,
                                                 'total_rs': 200,
                                                 'expenditure_len': 2,
                                                 'delete_expenditure': '',
                                                 'expend_date1': '03-04-2012',
                                                 'client_name1': 'Airlines',
                                                 'destination1': 'Chennai-23',
                                                 'km1': 100})
        self.assertEquals(final_level_approval.status_code, 302)
        travel_list = Travel.objects.all()
        self.assertEquals(len(travel_list), 1)
        self.assertEquals(travel_list[0].status_id, 'RS4')

    def test_list_lconveyance(self):
        self.test_manage_lconveyance()
        response = self.client.post(reverse('travel:list'))
        self.assertEquals(response.status_code, 200)
        travel_list = Travel.objects.all()
        self.assertEquals(len(travel_list), 1)
