from django.test.client import Client
from django.test import TestCase

from project_management.business_unit.models import BusinessUnit, \
    BusinessUnitType
from project_management.business_unit.forms import BusinessUnitForm
from project_management.address.forms import AddressForm
from project_management.projectbudget.tests.logintest import LoginTest


class BusinessUnitTests(TestCase):
    client = Client()

    def setUp(self):
        '''
        Fixtures are loaded.so Business Unit Types  objects are created
        '''
        self.client = LoginTest('testlogin').testlogin()
        self.bunit_type_list = BusinessUnitType.objects.all()
        BusinessUnit.objects.create(
            name='5G INDIA', type=self.bunit_type_list[3])
        self.business_unit_list = BusinessUnit.objects.all()

    def test_add_business_unit(self):
        country = 'GBR'  # United Kingdom country code
        response = self.client.post('/businessunit/create/',
                                    {'name': '5G Europe',
                                     'type': self.bunit_type_list[7].id,
                                        'address_line1': 'e-volve Business Centre',
                                        'address_line2': 'Cygnet Way,Rainton',
                                        'city': 'Tyne & Wear',
                                        'state': '',
                                        'pin': 'DH4 5QY',
                                        'country': country,
                                        'url': 'http://twitter.com/5GEurope',
                                     })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(self.business_unit_list), 2)

    def test_update_business_unit(self):
        country = 'IND'  # India  country code
        response = self.client.post('/businessunit/update/'
                                    + str(self.business_unit_list[0].id) + '/',
                                    {
                                        'name': '5G Europe',
                                        'type': self.bunit_type_list[3].id,
                                        'address_line1':
                                        'RR Tower IV,Ground Floor',
                                        'address_line2':
                                        'TVK Industrial Estate,Guindy',
                                        'city': 'Chennai',
                                        'state': 'Tamil Nadu',
                                        'pin': '600032',
                                        'country': country,
                                    })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.business_unit_list[0].address.city, 'Chennai')

    def test_business_unit_list(self):
        response = self.client.post('/businessunit/list/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.business_unit_list), 1)
        # search text in list
        response = self.client.post('/businessunit/list/?search=5G INDIA')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(self.business_unit_list), 1)

    def test_delete_unit_list(self):
        response = self.client.post('/businessunit/delete/',
                                    {
                                        'businessunit_pk': ['1']
                                    })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(self.business_unit_list), 0)
