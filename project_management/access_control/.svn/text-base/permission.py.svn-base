"""
    Object based permission back-end.
"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings

class ObjectPermission(object):
    """
        Back end capable of permission checks.
    """
    supports_object_permission = True
    support_anonymous_user = True

    def authenticate(self, username, password):
        """ L D A P and A U T H back ends already defines it. """
        return None

    def has_perm(self, user, perm, obj=None):
        """ Permission check for object. """
        if not user.is_authenticated():
            return False

        if obj is None:
            return False

        content_type = ContentType.objects.get_for_model(obj)
        try:
            # perm is usually of the form 'model.delete_model'.
            perm = perm.split('.')[-1].split('_')[0]
        except IndexError:
            return False

        perm = ObjectPermission.objects.filter(content_type = content_type,
                                               object_id = obj.id, user = user)

        return perm.filter(**{'can_%s' % perm: True}).exists()
