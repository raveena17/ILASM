from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from project_management.users.models import UserProfile
from project_management.reimbursement.models import *
from project_management.projectbudget.models import SaveRecordStatus
from project_management.projectbudget.tests.logintest import LoginTest


class ReimbursementTest(TestCase):
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

    def test_manage_reimbursement(self):
        mail.outbox = []
        response = self.client.post(reverse('reimbursement:list'))
        reimbursement_list = Reimbursement.objects.all()
        self.assertEquals(len(reimbursement_list), 0)
        # Create local conveyance
        response = self.client.post(reverse('reimbursement:create'))
        self.assertEquals(response.status_code, 200)
        # Save Reimbursement
        response = self.client.post(reverse('reimbursement:save'),
                                    {'reimburs_name': 'Reimbursement1',
                                     'requested_by': self.user_list[0].username,
                                     'request_to': self.user_list[1].username,
                                     'final_approver': self.user_list[2].id,
                                     'applied_date': '03-04-2012',
                                     'reimbus_status': self.status_record[0].id,
                                     'total_exp': 100,
                                     'expenditure_len': 2,
                                     'expenditure1': 'sample expenditure',
                                     'exp_amount1': 100,
                                     'delete_expenditure': ''
                                     })
        self.assertEquals(response.status_code, 302)
        reimbursement_list = Reimbursement.objects.all()
        self.assertEquals(len(reimbursement_list), 1)
        all_reimbur_expend = Expenditure_Reimburs.objects.all()
        self.assertEquals(len(all_reimbur_expend), 1)

        # Submit Reimbursement
        response = self.client.post(reverse('reimbursement:save'),
                                    {'reimbus_id': reimbursement_list[0].id,
                                     'reimburs_name': 'Reimbursement1',
                                     'requested_by': self.user_list[0].username,
                                     'request_to': self.user_list[1].username,
                                     'final_approver': self.user_list[2].id,
                                     'applied_date': '03-04-2012',
                                     'reimbus_status': self.status_record[1].id,
                                     'total_exp': 100,
                                     'reimbursement_id': reimbursement_list[0].id,
                                     'expenditure_len': 2,
                                     'expenditure1': 'sample expenditure',
                                     'exp_amount1': 100,
                                     'delete_expenditure': ''
                                     })
        test_reimbursement = Reimbursement.objects.get(name='Reimbursement1')
        self.assertEquals(response.status_code, 302)
        reimbursement_list = Reimbursement.objects.all()
        self.assertEquals(len(reimbursement_list), 1)
        self.assertEquals(test_reimbursement.status_id, 'RS2')

    def test_approve_reimbursement(self):
        # First level approvel
        self.test_manage_reimbursement()
        reimbursement_list = Reimbursement.objects.all()
        first_level_approvel = self.client.post(reverse('reimbursement:save'),
                                                {
            'reimbus_id': reimbursement_list[0].id,
            'reimburs_name': 'Reimbursement1',
            'requested_by': self.user_list[0].username,
            'request_to': self.user_list[1].username,
            'final_approver': self.user_list[2].id,
            'applied_date': '03-04-2012',
            'reimbus_status': self.status_record[2].id,
            'total_exp': 100,
            'reimbursement_id': reimbursement_list[0].id,
            'expenditure_len': 2,
            'expenditure1': 'sample expenditure',
            'exp_amount1': 100,
            'delete_expenditure': ''
        })
        test_reimbursement = Reimbursement.objects.get(name='Reimbursement1')
        self.assertEquals(first_level_approvel.status_code, 302)
        reimbursement_list = Reimbursement.objects.all()
        self.assertEquals(len(reimbursement_list), 1)
        self.assertEquals(test_reimbursement.status_id, 'RS3')

        # Second level approvel
        final_level_approvel = self.client.post(reverse('reimbursement:save'),
                                                {
            'reimbus_id': reimbursement_list[0].id,
            'reimburs_name': 'Reimbursement1',
            'requested_by': self.user_list[0].username,
            'request_to': self.user_list[1].username,
            'final_approver': self.user_list[2].id,
            'applied_date': '03-04-2012',
            'reimbus_status': self.status_record[3].id,
            'total_exp': 100,
            'reimbursement_id': reimbursement_list[0].id,
            'expenditure_len': 2,
            'expenditure1': 'sample expenditure',
            'exp_amount1': 100,
            'delete_expenditure': '',
        })
        test_reimbursement = Reimbursement.objects.get(name='Reimbursement1')
        self.assertEquals(final_level_approvel.status_code, 302)
        reimbursement_list = Reimbursement.objects.all()
        self.assertEquals(len(reimbursement_list), 1)
        self.assertEquals(test_reimbursement.status_id, 'RS4')

    def test_list_reimbursement(self):
        self.test_manage_reimbursement()
        response = self.client.post(reverse('reimbursement:list'))
        self.assertEquals(response.status_code, 200)
        reimbursement_list = Reimbursement.objects.all()
        self.assertEquals(len(reimbursement_list), 1)
