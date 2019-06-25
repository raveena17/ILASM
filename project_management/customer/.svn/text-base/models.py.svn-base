"""
    Customer Models
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Customer(models.Model):
    """
        Represents a customer of a project.
    """

    name = models.CharField(_('name'), max_length = 120, unique = True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        ordering = ['name', ]

class CustomerContact(models.Model):
    """
        Represent contact detail of customer in a project
    """

    salutation_choices = [('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs')]
    customer = models.ForeignKey(Customer, verbose_name = 'customer',
        null=True)
    salutation = models.CharField(_('salutation'),
        choices = salutation_choices, max_length = 10, null = True)
    name = models.CharField(_('name of contact'), max_length = 120)
    designation = models.CharField(_('contact designation'),
        max_length = 120, null = True)
    address = models.TextField(_('contact address'), blank = True, null = True)
    telephone = models.CharField(_('contact telephone'), max_length = 20,
        null = True)
    fax = models.CharField(_('contact fax'), max_length = 20, null = True)
    email = models.EmailField(_('contact email'), null = True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('customer detail')
        verbose_name_plural = _('customer details')
        ordering = ['name', ]
