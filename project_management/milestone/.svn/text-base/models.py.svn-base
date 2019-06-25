"""
    Milestone Models
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

class InvoiceTerms(models.Model):
    """
        Represents the invoice terms of the project
    """
    name = models.CharField(max_length = 120)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Invoice Term')
        verbose_name_plural = _('Invoice Terms')

class Milestone(models.Model):
    """
        Represents the milestones related to the project
    """
    INVOICE = 'invoice'
    ENGINEERING = 'engineering'
    category_choices = ((INVOICE, 'invoice'), (ENGINEERING, 'engineering'))
    name = models.CharField(max_length = 120, verbose_name = _('milestone'))
    percentage = models.CharField(max_length= 10, null = True,
                    blank = True, verbose_name = _('percentage'))
    start_date = models.DateField(_('Invoice Start Date'), null = True,
                    blank = True)# Just start date.
    end_date = models.DateField(_('Invoice End Date'), null = True,
                    blank = True)
    invoice_terms = models.ForeignKey(InvoiceTerms, blank = True, null = True,
                                      verbose_name = _('Invoice Terms'))
    category = models.CharField(max_length = 16, choices = category_choices,
                                default = category_choices[0][0]) #TODO Replace with invoice.
    notes = models.TextField(null = True, blank = True, verbose_name=_('Notes'))
    cancel = models.BooleanField(default = False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Milestone')
        verbose_name_plural = _('Milestones')
