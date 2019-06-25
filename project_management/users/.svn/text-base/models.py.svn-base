"""
    Models for users application
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from project_management.address.models import Address
from project_management.business_unit.models import BusinessUnit


class userType(models.Model):
    """
        Model which represent the type of user.
    """
    userType = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 120)

    def __unicode__(self):
        """
            returns model data stored in your database as unicode.
        """
        return self.name

class DocumentCheckList(models.Model):
    id =   models.AutoField(primary_key = True)
    list_name = models.CharField(max_length = 40)

    def __unicode__(self):
        """
            returns model data stored in your database as unicode.
        """
        return self.list_name

class UserProfile(models.Model):
    """
        Model that extends the auth.user model.
        This model is intended to be used for employee and customer alike.
        #TODO: Move some of the fields to an appropriate HR model.
    """
    PROBATION_PERIOD = (('1',_('1 Month')), ('2',_('2 Months')), ('3',_('3 Months')),
        ('4',_('4 Months')),('5',_('5 Months')),('6',_('6 Months')),('7',_('7 Months')),
        ('8',_('8 Months')),('9',_('9 Months')),('10',_('10 Months')),('11',_('11 Months')),
        ('12',_('12 Months')))
    EMPLOYEE_TYPES = (('E', _('Permanent')), ('C', _('Contract')),
                        ('T', _('Trainee')), ('TP', _('Temporary')))
    CUSTOMER_TYPES = (('CC', _('Customer contact')),)
    BLOOD_GROUPS = (('O+', _('O+')), ('O-', _('O-')),
                    ('A+', _('A+')), ('A-', _('A-')),
                    ('B+', _('B+')), ('B-', _('B-')),('A1+', _('A1+')),
                    ('AB+', _('AB+')), ('AB-', _('AB-')),)
    GENDERS = (('M', _('Male')), ('F', _('Female')))
    TITLE = (('Mr', _('Mr')), ('Ms', _('Ms')),
                ('Mrs', _('Mrs')), ('Dr', _('Dr')) )
    CONFIRMATION_STATUS = (('CONFIRMED', _('Confirmed')), ('ONPROBATION', _('On Probation')))
    DIVISION = (('TECHNICAL',_('Technical')), ('ADMINISTRATION',_('Administration')))

    salutation = models.CharField(_('salutation'), max_length = 3, null=True,
                                                                choices=TITLE)
    user = models.ForeignKey(User, verbose_name = _('user'),
                             related_name = '%s(class)s_user')
    fathers_name = models.CharField(_('Father''s Name'), blank=True, max_length = 56, null = True )
    email_address_official = models.EmailField(_('Email Address (Personal)'),blank=True, max_length = 56,null = True)
    code = models.CharField(_('code'), max_length = 8, null = True, blank=True)
    type = models.CharField(_('type'), max_length = 2, null = True,
            blank = True, choices = EMPLOYEE_TYPES + CUSTOMER_TYPES)
    division = models.CharField(_('Division'), choices = DIVISION,
                        max_length = 20, blank = True, null = True)
    designation = models.CharField(_('designation'),
                        max_length = 128, blank = True, null = True)
    business_unit = models.ManyToManyField(BusinessUnit,
                                verbose_name = _('business unit'))

    gender = models.CharField(_('gender'), choices = GENDERS,
                        max_length = 1, blank = True, null = True)
    confirmation_status = models.CharField(_('confirmation status'), choices = CONFIRMATION_STATUS,
                        max_length = 15)
    date_of_confirmation = models.DateField(_('date of confirmation'), null = True,
                                            blank = True)
    probation_period = models.CharField(_('probation period(in Months)'), choices = PROBATION_PERIOD,
                                        max_length = 10, null = True, blank = True )
    probation_end_date = models.CharField(_('probation end date'),max_length = 11, null = True,
                                           blank = True)
    blood_group = models.CharField(_('blood group'), choices = BLOOD_GROUPS,
                        max_length = 3, blank = True, null = True)
    date_of_birth = models.DateField(_('date of birth'), null = True,
                                                    blank=True)
    date_of_joining = models.DateField(_('date of joining'), null = True,
                                                    blank=True)
    document_check_list = models.ManyToManyField(DocumentCheckList, verbose_name = _('document check list'),
                                                 null = True, blank = True)
    date_of_resignation = models.DateField(_('Date of resignation'), null = True, blank = True)

    date_of_relieving = models.DateField(_('Date of relieving'), null = True, blank = True)

    phone_office = models.CharField(_('office telephone number'),
                        max_length = 20, blank=True, null = True)
    phone_office_extension = models.IntegerField(
                    _('office telephone extension'), null = True, blank=True)
    phone_mobile = models.CharField(_('mobile number'),
                        max_length = 20, blank = True, null = True)
    phone_residence = models.CharField(_('residence phone number'),
                        max_length = 20, blank = True, null = True)
    emergency_contact = models.CharField('emergency contact',
                        blank=True, max_length = 56, null = True)

    phone_emergency1 = models.CharField(_('emergency telephone number 1'),
                        max_length = 20, blank = True, null = True)
    phone_emergency2 = models.CharField(_('emergency telephone number 2'),
                        max_length = 20, blank = True, null = True)
    address_contact = models.ForeignKey(Address,
                    related_name = '%s(class)s_contact_address',
                    verbose_name = _('contact address'), null = True)
    address_permanent = models.ForeignKey(Address,
                    related_name = '%s(class)s_permanent_address',
                    verbose_name = _('permanent address'), null = True)

    bank_name = models.CharField(_('Bank Name / Branch'),
                                 null = True, blank = True, max_length = 40)
    bank_acc_no = models.CharField(_('Bank account number'),
                                   max_length = 24, blank = True, null = True)
    pan_no = models.CharField(_('PAN number'), max_length = 16,
                                                    blank = True, null = True)
    pf_no = models.CharField(_('PF number'), max_length = 16,
                                                    blank = True, null = True)
    passport_no = models.CharField(_('Passport number'),
                                max_length = 16, blank = True, null = True)
    passport_validity = models.DateField(_('passport validity'), null=True,
                                                            blank = True)
    hide_phone_number = models.BooleanField(
                _('Dont Show phone number in Address Book'), default = False,
                help_text = _('Your personal phone number will not be listed.'))

    comments = models.TextField(blank=True, null=True, max_length = 10)
    is_confirmed = models.BooleanField(default = False)
    document_check_list_others = models.CharField(null = True, blank = True, max_length = 100)
    users_image = models.ImageField(upload_to = "user_images/", max_length = 300, null = True, blank = True)
    customer_code = models.CharField(_('customer_code'), max_length = 8, null = True, blank=True)
    reporting_senior = models.CharField(_('Reporting_senior'), max_length = 8, null = True, blank=True)
    reporting_senior_name = models.ForeignKey(User, blank=True, null=True, verbose_name = _('reporting_senior_name'), related_name = '%s(class)s_reporting_senior_name')

    def __unicode__(self):
        """
            returns model data stored in your database as unicode.
        """
        return self.user.username


    class Meta:
        """
            Defines metadata for the model.
        """
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
