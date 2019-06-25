# -*- coding: utf-8 -*-
""" Models for authentication and authorization. """
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from project_management.address.models import Address

class ObjectPermission(models.Model):
    """
        Model for object based permissions.
    """
    user = models.ForeignKey(User, verbose_name = _('user'),
                             related_name = '%s(class)s_user')
    can_view = models.BooleanField(_('can view'))
    can_edit = models.BooleanField(_('can edit'))
    can_delete = models.BooleanField(_('can delete'))
    content_type = models.ForeignKey(ContentType, verbose_name = _('type'),
                                     related_name = '%s(class)s_content_type')
    object_id = models.CharField(max_length = 36)

    class Meta:
        verbose_name = _('object permission')
        verbose_name_plural = _('object permissions')
        ordering = ['user']
        unique_together = (('user', 'content_type', 'object_id'),)

    def __unicode__(self):
        return u'%s | %s | %s' % (unicode(self.user), unicode(self.content_type),
                             unicode(self.object_id))

    def natural_key(self):
        return (self.user, self.object_id,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']

