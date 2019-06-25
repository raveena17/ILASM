from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User, Group

from project_management.users.models import UserProfile
from project_management.users.forms import UserProfileForm, UserForm,\
    MyProfileForm
from project_management.business_unit.models import BusinessUnit
from project_management.projectbudget.tests.logintest import LoginTest


class UsersTest(TestCase):

    client = Client()

    def setUp(self):
        '''
        setUp is a default method.It will run before the execution of every
        test method.
        '''
        self.client = LoginTest('testlogin').testlogin()
        User.objects.create(
            id='46',
            username='admin3',
            first_name='admin3',
            last_name='',
            email='ashok@5gindia.net',
            is_staff='1',
            is_active='1',
            last_login='2012-09-24 05:16:45',
            date_joined='2012-09-24 05:16:45')
        user_object = User.objects.get(pk=46)
        user_object.set_password('admin')
        user_object.save()
        self.user_list = User.objects.all()
        Group.objects.create(name='Manager')
        self.group_list = Group.objects.all()
        # Adding the user to Manager Group
        self.user_list[1].groups.add(self.group_list[0])
        response = BusinessUnit.objects.create(
            name="5G-PSG", firstname="india", type_id="1",
            contact_email="5gpsg@gmail.com")
        collections = BusinessUnit.objects.all()
        self.id_buss_unit = collections[0].id

    def test_add_user(self):
        # clear the mail outbox
        mail.outbox = []
        response = self.client.post('/user/create/',
                                    {
                                        'first_name': 'ashok',
                                        'last_name': 'kumar',
                                        'email': 'admin@5gindia.net',
                                        'username': 'ashok',
                                        'fathers_name': 'dhanavel',
                                        'email_address_official':
                                                    'admin@gmail.com',
                                        'type': 'E',
                                        'division': 'TECHNICAL',
                                        'designation': 'Software Engineering',
                                        'gender': 'M',
                                        'blood_group': 'B+',
                                        'date_of_birth': '08-05-1987',
                                        'pan_no': 'BETPA6070E',
                                        'passport_no': 'PK908S',
                                        'passport_validity': '09-07-2025',
                                        'phone_office': 299405,
                                        'phone_office_extension': 5248,
                                        'phone_mobile': 9003766032,
                                        'phone_residence': 299405,
                                        'address_line1':
                                        '8/7 v.o.c nagar,abatharanapuram',
                                        'address_line2': 'vadalur',
                                        'city': 'cuddalore',
                                        'state': 'Tamilnadu',
                                        'pin': '607303',
                                        'country': 'India',
                                        'confirmation_status': 'CONFIRMED',
                                        'date_of_joining': '02-01-2012',
                                        'salutation': 'Mr',
                                        'is_confirmed': 1,
                                        'reporting_senior_name':
                                            self.user_list[1].id,
                                        'business_unit': self.id_buss_unit,
                                    })
        self.assertEquals(response.status_code, 302)
        user_profile = UserProfile.objects.all()
        self.assertEquals(len(user_profile), 1)
        self.assertEquals(user_profile[0].user.username, 'ashok')

    def test_update_user(self):
        '''
        Calling the test_add_user funciton  to create user profile
        '''
        self.test_add_user()
        user_profile_list = UserProfile.objects.all()
        response = self.client.post('/user/update/' + str(user_profile_list[0].id) + '/',
                                    {
                                    'first_name': 'Ashok Kumar',
                                    'last_name': 'Dhanavel',
                                    'username': 'ashok',
                                    'email': 'admin@5gindia.net',
                                    'username': 'ashok',
                                    'fathers_name': 'dhanavel',
                                    'email_address_official':
                                                'admin@gmail.com',
                                    'type': 'E',
                                    'division': 'TECHNICAL',
                                    'designation': 'Software Engineering',
                                    'gender': 'M',
                                    'blood_group': 'B+',
                                    'date_of_birth': '08-05-1987',
                                    'pan_no': 'BETPA6070E',
                                    'passport_no': 'PK908S',
                                    'passport_validity': '09-07-2025',
                                    'phone_office': 299405,
                                    'phone_office_extension': 5248,
                                    'phone_mobile': 9003766032,
                                    'phone_residence': 299405,
                                    'address_line1':
                                        '8/7 v.o.c nagar,abatharanapuram',
                                    'address_line2': 'vadalur',
                                    'city': 'cuddalore',
                                    'state': 'Tamilnadu',
                                    'pin': '607303',
                                    'country': 'India',
                                    'confirmation_status': 'CONFIRMED',
                                    'date_of_joining': '02-01-2012',
                                    'salutation': 'Mr',
                                    'is_confirmed': 1,
                                    'reporting_senior_name':
                                        self.user_list[1].id,
                                    'business_unit': self.id_buss_unit,
                                    })

        user_after_edit = UserProfile.objects.get(pk=1)
        self.assertEquals(user_after_edit.user.first_name, 'Ashok Kumar')
        self.assertEquals(response.status_code, 302)

    def test_list_user(self):
        self.test_add_user()
        response = self.client.post('/user/list/')
        self.assertEquals(response.status_code, 200)
        user_profile = UserProfile.objects.all()
        self.assertEquals(len(user_profile), 1)

    def _test_userprofile_login(self):
        '''
        To manage own profile the user has to login
        '''
        self.test_add_user()
        user_profile = UserProfile.objects.get(pk=1)
        user_profile.user.set_password('admin')
        user_profile.user.save()
        response = self.client.post('/login/', {
                                    'username': 'ashok',
                                    'password': 'admin',
                                    }
                                    )
        self.assertEquals(response.status_code, 302)
        return response.client

    def test_view_myprofile(self):
        self.client = self._test_userprofile_login()
        response = self.client.post('/user/myprofile/')
        self.assertEquals(response.status_code, 200)
        user_profile = UserProfile.objects.all()
        self.assertEquals(len(user_profile), 1)

    def test_edit_myprofile(self):
        self.client = self._test_userprofile_login()
        response = self.client.post('/user/myprofile/',
                                    {
                                        'first_name': 'Ashok',
                                        'last_name': 'Kumar',
                                        'username': 'ashok',
                                        'email': 'admin@5gindia.net',
                                        'username': 'ashok',
                                        'fathers_name': 'Kumar',
                                        'email_address_official':
                                        'ashok@5gindia.net',
                                        'division': 'TECHNICAL',
                                        'designation': 'Software Engineering',
                                        'gender': 'M',
                                        'blood_group': 'B+',
                                        'date_of_birth': '08-05-1987',
                                        'pan_no': 'BETPA6070E',
                                        'passport_no': 'PK908S',
                                        'passport_validity': '09-07-2025',
                                        'phone_office': 299405,
                                        'phone_office_extension': 5248,
                                        'phone_mobile': 9003766032,
                                        'phone_residence': 299405,
                                        'address_line1':
                                        '8/7 v.o.c nagar,abatharanapuram',
                                        'address_line2': 'vadalur',
                                        'city': 'cuddalore',
                                        'state': 'Tamilnadu',
                                        'pin': '607303',
                                        'country': 'India',
                                        'reporting_senior_name':
                                        self.user_list[1].id,
                                        'business_unit': self.id_buss_unit, })
        user_after_edit = UserProfile.objects.get(pk=1)
        self.assertEquals(user_after_edit.email_address_official,
                          'ashok@5gindia.net')
        self.assertEquals(response.status_code, 200)

    def test_manage_user_status(self):
        '''
        Deactivate the user profile
        '''
        self.test_add_user()
        user_profile = UserProfile.objects.get(pk=1)
        response = self.client.post('/user/deactivate/', {'user_pk': ['1']})
        user_after_edit = UserProfile.objects.get(pk=1)
        self.assertEquals(user_after_edit.user.is_active, False)
        self.assertEquals(response.status_code, 302)

    def test_deactivate_user_login(self):
        self.test_manage_user_status()
        user_profile = UserProfile.objects.get(pk=1)
        user_profile.user.set_password('admin')
        user_profile.user.save()
        response = self.client.post('/login/', {
                                    'username': 'ashok',
                                    'password': 'admin',
                                    })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(str(response.context['form'].errors.values()),
                          "[[u'This account is inactive.']]")
