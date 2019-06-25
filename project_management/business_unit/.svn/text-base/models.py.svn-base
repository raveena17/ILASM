from django.db import models
from django.utils.translation import ugettext_lazy as _

from project_management.address.models import Address

class BusinessUnitType(models.Model):
    name =  models.CharField(_('Name'), max_length = 120 )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Business Unit Type')
        verbose_name_plural = _('Business Unit Types')
        ordering = ['name']

class BusinessUnit(models.Model):
    name = models.CharField(_('Name'), max_length = 120)
    firstname = models.CharField(_('FirstName'), max_length = 50)
    lastname =  models.CharField(_('LastName'), max_length = 50, null = True, blank = True)
    type = models.ForeignKey(BusinessUnitType, verbose_name = _('Type'))
    address = models.ForeignKey(Address, verbose_name = _('Address'),
                                                null=True, blank=True)
    related_to = models.ForeignKey('self', null = True,  blank = True,
                                                verbose_name = _('Business Unit'))
    url = models.CharField( _('Url'), max_length = 120, null = True,  blank = True)
    cancel = models.BooleanField(_('Cancel'), default = False)
    customer_code = models.CharField(_('Code'), max_length = 20 , null = True, blank = True)
    contact_email = models.EmailField(_('Email'), null = True, blank = True)
    notes = models.TextField(_('Notes'), null = True,  blank = True )
    is_active = models.BooleanField(default = True)
    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            if BusinessUnit.objects.aggregate( models.Max('id'))['id__max'] != None:
                self.customer_code = BusinessUnit.objects.aggregate(
                        models.Max('id'))['id__max']+1
            else:
                self.customer_code = 1
            print  self.customer_code
            self.customer_code = 'C00' + str(self.customer_code)
            print self.customer_code
            
        super(BusinessUnit, self).save(**kwargs)
        
    class Meta:
        verbose_name = _('Business Unit')
        verbose_name_plural = _('Business Units')
        ordering = ['name']
        
    
