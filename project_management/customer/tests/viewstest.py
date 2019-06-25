from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User

from project_management.users.models import UserProfile
from project_management.customer.models import *
from project_management.business_unit.models import BusinessUnit, \
    BusinessUnitType
from project_management.projectbudget.tests.logintest import LoginTest


class CustomerTest(TestCase):
    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()
        '''
        Fixtures are loaded.so Business Unit Types  objects are created
        '''
        self.bunit_type_list = BusinessUnitType.objects.all()

    def test_add_client_details(self):
        country = 'GBR'  # United Kingdom country code
        response = self.client.post('/customer/create/',
                                    {
                                        'name': 'Alcatel Lucent Ltd.',
                                        'firstname': 'Alcatel',
                                        'type': self.bunit_type_list[4].id,
                                        'address_line1':
                                        'e-volve Business Centre',
                                        'address_line2':
                                        'Cygnet Way, Rainton Bridge',
                                        'city': 'Tyne & Wear',
                                        'state': '',
                                        'pin': 'DH4 5QY',
                                        'country': country,
                                    })
        self.assertEquals(response.status_code, 200)
        self.business_unit_list = BusinessUnit.objects.all()
        self.assertEquals(len(self.business_unit_list), 1)

    def test_exists_client_check(self):
        self.test_add_client_details()
        country = 'GBR'  # United Kingdom country code
        response = self.client.post('/customer/create/',
                                    {
                                        'name': 'Alcatel Lucent Ltd.',
                                        'firstname': 'Alcatel',
                                        'type': self.bunit_type_list[4].id,
                                        'address_line1':
                                        'e-volve Business Centre',
                                        'address_line2':
                                        'Cygnet Way, Rainton Bridge',
                                        'city': 'Tyne & Wear',
                                        'state': '',
                                        'pin': 'DH4 5QY',
                                        'country': country,
                                    })
        self.assertEquals(response.status_code, 200)
        messages = response.context['messages']
        errors = [message for message in messages]
        self.assertEquals(
            errors[0].message.title(),
            u'Client Name Already Exists')

    def test_update_customer_contact(self):
        self.test_add_client_details()
        edit_business_unit = BusinessUnit.objects.get(pk=1)
        country = 'GBR'  # United Kingdom country code
        response = self.client.post('/customer/update/' +
                                    str(edit_business_unit.id) + '/',
                                    {
                                        'name': 'Lucent Ltd.',
                                        'firstname': 'Alcatel',
                                        'type': self.bunit_type_list[4].id,
                                        'address_line1':
                                        'e-volve Business Centre',
                                        'address_line2':
                                        'Cygnet Way, Rainton Bridge',
                                        'city': 'Tyne & Wear',
                                        'state': '',
                                        'pin': 'DH4 5QY',
                                        'country': country,
                                    })
        self.assertEquals(response.status_code, 200)
        edit_business_unit = BusinessUnit.objects.get(pk=1)
        self.assertEquals(edit_business_unit.name, 'Lucent Ltd.')

    def test_list_customer_contact(self):
        self.test_add_client_details()
        response = self.client.post('/customer/list/')
        self.assertEquals(response.status_code, 200)
        business_unit_list = BusinessUnit.objects.all()
        self.assertEquals(len(business_unit_list), 1)
        # Search Text in  list
        response = self.client.post('/customer/list/?search=Lucent')
        self.assertEquals(response.status_code, 200)
        business_unit_list = BusinessUnit.objects.all()
        self.assertEquals(len(business_unit_list), 1)

    def test_manage_client_status(self):
        '''
        To Deactivate the client status
        '''
        self.test_add_client_details()
        response = self.client.post(
            '/customer/deactivate/', {'client_pk': ['1']})
        edit_business_unit = BusinessUnit.objects.get(pk=1)
        self.assertEquals(edit_business_unit.is_active, False)

    def test_add_customer_from_project(self):
        self.test_add_client_details()
        client_list = BusinessUnit.objects.get(pk=1)
        country = 'GBR'  # United Kingdom country code
        response = self.client.post('/customer/contact/create/',
                                    {
                                        'salutation': 'Mr',
                                        'first_name': 'Manoj',
                                        'last_name': 'Kumar',
                                        'email': 'manoj@alcatel.net',
                                        'business_unit': client_list.id,
                                        'address_line1':
                                        'e-volve Business Centre',
                                        'address_line2':
                                        'Cygnet Way, Rainton Bridge',
                                        'city': 'Tyne & Wear',
                                        'pin': 'DH4 5QY',
                                        'country': country
                                    })
        self.assertEquals(response.status_code, 200)
        user_customer = User.objects.get(pk=2)
        self.assertEquals(user_customer.first_name, 'Manoj')

    def test_update_customer_from_project(self):
        self.test_add_customer_from_project()
        user_customer = UserProfile.objects.get(pk=1)
        client_list = BusinessUnit.objects.get(pk=1)
        country = 'GBR'  # United Kingdom country code
        response = self.client.post(
            '/customer/contact/update/' + str(
                user_customer.id) + '/',
            {
                'contact_profile_id': str(
                    user_customer.id),
                'salutation': 'Mrs',
                'first_name': 'Manoj',
                'last_name': 'Kumar',
                'email': 'manoj@alcatel.net',
                'business_unit': client_list.id,
                'address_line1': 'e-volve Business Centre',
                'address_line2': 'Cygnet Way, Rainton Bridge',
                'city': 'Tyne & Wear',
                'pin': 'DH4 5QY',
                'country': country})
        self.assertEquals(response.status_code, 200)
        user_customer = UserProfile.objects.get(pk=1)
        self.assertEquals(user_customer.salutation, 'Mrs')
