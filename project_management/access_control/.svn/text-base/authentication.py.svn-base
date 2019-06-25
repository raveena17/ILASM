"""
    LDAP authentication backend.
"""
import ldap
from django.contrib.auth.models import User
from project_management.settings import LDAP_SERVER


class LDAPBackend(object):
    """
        Provides methods to authenticate against LDAP
        and get_user from the Auth plug-in.
    """
    def authenticate(self, username = None, password = None):
        """
            Authenticate against the LDAP server provided by settings.LDAP_SERVER.
            The LDAP server is assumed to listen to port 389.
        """
        try:
            con = ldap.open(LDAP_SERVER, 389)
            con.simple_bind_s(username, password)
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = None # New users may be added (created) here. (enhancement)
        except ldap.LDAPError:
            user = None
        return user

    def get_user(self, user_id):
        """
            Get user object from Auth.User.
        """
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None

