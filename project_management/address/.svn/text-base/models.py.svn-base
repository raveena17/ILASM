from django.db import models
from django.utils.translation import ugettext_lazy as _
from project_management.fields.country_field import CountryField

class Address(models.Model):
    """
        A generic international address format.
    """
    address_line1 = models.CharField(_('address line 1'), max_length = 200,
                help_text = _('Street address, P.O. box, company name, c/o'),
                null = True,  blank = True)
    address_line2 = models.CharField(_('address line 2'), max_length = 200,
                help_text = _('Apartment, building, floor, suite, unit, etc.'),
                null = True,  blank = True)
    city = models.CharField(_('city'), max_length = 80, null=True, blank=True,
                            help_text = _('City or town'))
    state = models.CharField(_('State / Province / Region'), max_length = 120,
                             null=True, blank=True)
    pin = models.CharField(_('ZIP / Postal Code'), max_length = 16,
                           null = True, blank = True)
    country = CountryField(_('Country'), null=True, blank=True)

    def __unicode__(self):
        return '%s\n%s\n%s\n%s\n%s\n%s' % (
                self.address_line1,
                self.address_line2,
                self.city,
                self.state,
                self.pin,
                self.country
        )

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
